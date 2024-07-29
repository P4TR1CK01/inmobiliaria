from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from main.services import crear_user, editar_user_sin_password, eliminar_user, cambiar_contraseña, crear_inmueble as crear_inmueble_service, eliminar_inmueble as eliminar_inmueble_service
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

@login_required
def profile(req):
  usuario = req.user
  inmuebles = Inmueble.objects.filter(propietario = usuario)
  context = {
    'inmuebles': inmuebles
  }
  if req.method == 'POST':
    if req.POST['telefono'].strip() != '':
      username = req.POST['username']
      first_name = req.POST['first_name']
      last_name = req.POST['last_name']
      email = req.POST['email']
      direccion = req.POST['direccion']
      telefono = req.POST['telefono']
      rol = req.POST['rol']
    else:
      username = req.user
      first_name = req.user.first_name
      last_name = req.POST['last_name']
      email = req.POST['email']
      direccion = req.POST['direccion']
      rol = req.POST['rol']
      messages.success(req, 'Datos actualizados correctamente')
      return redirect('/accounts/profile')
  return render(req, 'registration/profile.html', context)

@login_required
def edit_user(req):

  if req.method == 'POST':
    try:
      if req.POST['telefono'].strip() != '':
        # trailing whitespaces .strip()
          username = req.user
          first_name = req.POST['first_name']
          last_name = req.POST['last_name']
          email = req.POST['email']
          direccion = req.POST['direccion']
          rol = req.POST['rol']
          telefono = req.POST['telefono']
          editar_user_sin_password(username, first_name, last_name, email, direccion, rol, telefono)
          messages.success(req,'Datos actualizados')
          return redirect('/accounts/profile')

      else:
        username = req.user
        first_name = req.POST['first_name']
        last_name = req.POST['last_name']
        email = req.POST['email']
        direccion = req.POST['direccion']
        rol = req.POST['rol']
        editar_user_sin_password(username, first_name, last_name, email, direccion, rol)
        messages.success(req,'Datos actualizados')
        return redirect('/accounts/profile')

    except Exception as e:
      messages.error(req, "Error al actualizar tus datos: {}".format(e))
    return redirect('/')
  else:
    return render(req, 'profile.html')

@login_required
def delete_user(req):
  rut = req.user.username
  print (rut)
  eliminar_user(rut)
  messages.success(req, 'Usuario eliminado')
  return redirect('/accounts/profile')

def change_password(req):
  # Recibo los datos del formulrio
  password = req.POST['password']
  pass_repeat = req.POST['pass_repeat']
  cambiar_contraseña(req, password, pass_repeat)
  return redirect('/accounts/profile')

def solo_arrendadores(user):
    # Comprueba si el usuario es un arrendador
    if user.groups.filter(name='arrendadores').exists():
        return True
    return False

def solo_arrendatarios(user):
  if user.groups.filter(name='arrendatarios').exist():
    return True
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
  messages.success( 'Propiedad Creada')
  return redirect('/')

@user_passes_test(solo_arrendadores)
def editar_inmueble(req, id):
  if req.method == 'GET':
    # Obtengo el inmueble a editar
    inmueble = Inmueble.objects.get(id=id)
    # Obtengo las regiones y comunas
    regiones = Region.objects.all()
    comunas = Comuna.objects.all()
    # Obtengo el código de la region
    cod_region_actual = inmueble.comuna.region.cod
    # Creo el 'context' con toda la info que requiere el template
    context = {
      'inmueble': inmueble,
      'regiones': regiones,
      'comunas': comunas,
      'cod_region': cod_region,
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
    return redirect('/')

@user_passes_test(solo_arrendadores)
def eliminar_inmueble(req, id):
  eliminar_inmueble_service(id)
  messages.error(req, 'Inmueble eliminado')
  return redirect('/accounts/profile/')

@login_required
def detalle_inmueble(req, id):
  id = int(id)
  inmueble_encontrado = Inmueble.objects.get(id=id)
  context = {
    'inmueble': inmueble_encontrado,
  }
  return render(req, 'detalle_inmueble.html')

def bodegas(req):
    return render(req, 'bodegas.html')
  
def casas(req):
    return render(req, 'casas.html')
  
def departamentos(req):
    return render(req, 'departamentos.html')
  
def parcelas(req):
    return render(req, 'parcelas.html')

def about(req):
    return render(req, 'about.html')
