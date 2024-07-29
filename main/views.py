from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.db.models import Q
from main.services import crear_user, editar_user, editar_user_sin_password, eliminar_user, cambiar_contraseña, crear_inmueble as crear_inmueble_service, eliminar_inmueble as eliminar_inmueble_service, crear_inmueble, editar_inmueble, eliminar_inmueble
from main.models import Inmueble, Region, Comuna
#from main.forms import InmuebleForm

# Create your views here.

@login_required
def home(req):
  datos = req.GET
  region_cod = datos.get('region_cod', '')
  comuna_cod = datos.get('comuna_cod', '')
  palabra = datos.get('palabra', '')
  inmuebles = filtrar_inmuebles(region_cod, comuna_cod, palabra)
  comunas = Comuna.objects.all()
  regiones = Region.objects.all()
  context = {
    'comunas': comunas, 
    'regiones': regiones,
    'inmuebles': inmuebles
  }
  return render(req, 'home.html', context)

# Filtros de busqueda en pagina de inicio-->
def filtrar_inmuebles(region_cod, comuna_cod, palabra):
  # Filtra inmuebles según la región, comuna y palabra clave
  filtro_palabra = None 
  if palabra != '':
    filtro_palabra = Q(nombre__icontains=palabra) | Q(descripcion__icontains=palabra)
  
  filtro_ubicacion = None
  if comuna_cod != '':
    comuna = Comuna.objects.get(cod=comuna_cod)
    filtro_ubicacion = Q(comuna=comuna)
  elif region_cod != '':
    region = Region.objects.get(cod=region_cod)
    comunas_region = region.comunas.all()
    filtro_ubicacion = Q(comuna__in=comunas_region)
  if filtro_ubicacion is None and filtro_palabra is None:
    return Inmueble.objects.all()
  elif filtro_ubicacion is not None and filtro_palabra is None:
    return Inmueble.objects.filter(filtro_ubicacion)
  elif filtro_ubicacion is None and filtro_palabra is not None:
    return Inmueble.objects.filter(filtro_palabra)
  elif filtro_ubicacion is not None and filtro_palabra is not None:
    return Inmueble.objects.filter(filtro_palabra & filtro_ubicacion)

def register(req):
  if req.method == 'POST':
    username = req.POST['username']
    first_name = req.POST['first_name']
    last_name = req.POST['last_name']
    email = req.POST['email']
    direccion = req.POST['direccion']
    telefono = req.POST['telefono']
    rol = req.POST['rol']
    password = req.POST['password']
    password_confirm = req.POST['password_confirm']
    crear_user(req, username, first_name, last_name, email, password, password_confirm, direccion, rol, telefono=None)
    return redirect('login')
  else:
    return render(req, 'registration/register.html')

def about(req):
    return render(req, 'about.html')

@login_required
def profile(req):
  usuario = req.user
  inmuebles = Inmueble.objects.filter(propietario = usuario)
  context = {
    'inmuebles': inmuebles
  }
  return render(req, 'registration/profile.html', context)

@login_required
def edit_user(req):
  # Obtengo el usuario actual
  current_user = req.user
  # llamo a la función para editar el usuario
  if req.POST['telefono'].strip() != '':
    # trailing whitespaces .strip()
    editar_user_sin_password(
      current_user.username,
      req.POST['first_name'],
      req.POST['last_name'],
      req.POST['email'],
      req.POST['direccion'],
      req.POST['rol'],
      req.POST['telefono'])
  else:
    editar_user_sin_password(
      current_user.username,
      req.POST['first_name'],
      req.POST['last_name'],
      req.POST['email'],
      req.POST['direccion'],
      req.POST['rol'])
  messages.success(req, "Sus datos han sido actualizados")
  return redirect('/')

def change_password(req):
  # Recibo los datos del formulrio
  password = req.POST['password']
  pass_repeat = req.POST['pass_repeat']
  # Valido que ambas contraseñas coincidan
  if password != pass_repeat:
    messages.danger(req, 'Las contraseñas no coinciden')
    return redirect('/accounts/profile')
  # Actualizamos la contraseña
  req.user.set_password(password)
  req.user.save()
  # Le avisamos al usuario que el cambio fue exitoso
  messages.success(req, "Contraseña actualizada")
  return redirect('/accounts/profile')

def solo_arrendadores(user):
    # Comprueba si el usuario es un arrendador
    if user.groups.filter(name='arrendadores').exists():
        return True
    return False

def solo_arrendatarios(req):
  return HttpResponse('solo arrendatarios')

# Inmuebles -->

@login_required
def nuevo_inmueble(req):
  # Nos traemos la informacion de las comunas y las regiones
  regiones = Region.objects.all()
  comunas = Comuna.objects.all()
  # pasar los datos requeridos por el formulario
  context = {
    'tipos_inmueble': Inmueble.inmuebles,
    'regiones': regiones,
    'comunas': comunas
  }
  return render(req, 'nuevo_inmueble.html', context)


@user_passes_test(solo_arrendadores)
def crear_inmueble(req):
  # Obtener el rut del usuario
  propietario_rut = req.user.username
  # Agregamos el inmueble a la DataBase
  crear_inmueble_service(
    req.POST['nombre'],
    req.POST['descripcion'],
    int(req.POST['m2_construidos']),
    int(req.POST['m2_totales']),
    int(req.POST['num_estacionamientos']),
    int(req.POST['num_habitaciones']),
    int(req.POST['num_baños']),
    req.POST['direccion'],
    req.POST['tipo_inmueble'],
    int(req.POST['precio']),
    req.POST['comuna_cod'],
    propietario_rut
  )
  messages.success(req, 'Propiedad Creada')
  return redirect('/accounts/nuevo_inmueble/')

@user_passes_test(solo_arrendadores)
def editar_inmueble(req, id):
    if req.method == 'GET':
        # Obtengo el inmueble a editar
        inmueble = Inmueble.objects.get(id=id)
        # Obtengo las regiones y comunas
        regiones = Region.objects.all()
        comunas = Comuna.objects.all()
        # Obtengo el código de la region
        cod_region_actual = inmueble.comuna_id[0:2]
        # Creo el 'context' con toda la info que requiere el template
        context = {
            'inmueble': inmueble,
            'regiones': regiones,
            'comunas': comunas,
            'cod_region': cod_region_actual,
        }
        return render(req, 'editar_inmueble.html', context)
    else:
        propietario_rut = req.user.username
        editar_inmueble_service(
            id,
            req.POST.get('nombre'),
            req.POST.get('descripcion'),
            int(req.POST.get('m2_construidos')),
            int(req.POST.get('m2_totales')),
            int(req.POST.get('num_estacionamientos')),
            int(req.POST.get('num_habitaciones')),
            int(req.POST.get('num_baños')),
            req.POST.get('direccion'),
            req.POST.get('tipo_inmueble'),
            int(req.POST.get('precio')),
            req.POST.get('comuna_cod'),
            propietario_rut
        )
        messages.success(req, 'Cambios guardados')
        return redirect('/accounts/profile/')

@user_passes_test(solo_arrendadores)
def eliminar_inmueble(req, id):
  eliminar_inmueble_service(id)
  messages.error(req, 'Inmueble eliminado')
  return redirect('/accounts/profile/')

