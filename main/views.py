from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.services import editar_user_sin_password
from django.contrib.auth.decorators import user_passes_test
from main.models import Inmueble, Region, Comuna
from main.services import crear_inmueble as crear_inmueble_service, eliminar_inmueble as eliminar_inmueble_service
#from inmueble.forms import InmuebleForm
from django.db.models import Q
# Create your views here.

def register(req):
  return render(req, 'register.html')

def calcular_clase(tipo_mensaje):
  if tipo_mensaje == 'error':
    return 'danger'
  return tipo_mensaje



@login_required
def profile(req):
  usuario = req.user
  inmuebles = Inmueble.objects.filter(propietario = usuario)
  context = {
    'inmuebles': inmuebles
  }
  return render(req, 'profile.html', context)

@login_required
def edit_user(req):
  # 1. Obtengo el usuario actual
  current_user = req.user
  # llamo a la función para editar el usuario
  if req.POST['telefono'] != '':
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
  #1. Recibo los datos del formulrio
  password = req.POST['password']
  pass_repeat = req.POST['pass_repeat']
  #2. Valido que ambas contraseñas coincidan
  if password != pass_repeat:
    messages.danger(req, 'Las contraseñas no coinciden')
    return redirect('/accounts/profile')
  #3. Actualizamos la contraseña
  req.user.set_password(password)
  req.user.save()
  #4. Le avisamos al usuario que el cambio fue exitoso
  messages.success(req, "Contraseña actualizada")
  return redirect('/accounts/profile')


#vamos a crear un test que solo pasan los 'arrendadores'
def solo_arrendadores(user):
  if user.usuario.rol == 'arrendador' or user.is_staff ==True:
    return True
  else:
    return False


def solo_arrendatarios(req):
  return HttpResponse('sólo arrendatarios')

### Inmuebles -->

@user_passes_test(solo_arrendadores)
def nuevo_inmueble(req):
  #nos traemos la informacion de las comunas y las regiones
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
  # obtener el rut del usuario
  print(req.POST)
  #validar metraje (construidos vs totales)
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
  return redirect('/accounts/profile/')
    
    
@user_passes_test(solo_arrendadores)
def editar_inmueble(req, id):
  if req.method == 'GET':
    #1. Obtengo el inmueble a editar
    inmueble = Inmueble.objects.get(id=id)
    # 2. Obtengo las regiones y comunas
    regiones = Region.objects.all()
    comunas = Comuna.objects.all()
    # 2.5 Obtengo el código de la region
    # cod_region = inmueble.comuna.region.cod
    cod_region_actual = inmueble.comuna_id[0:2]
    # 3. Creo el 'context' con toda la info que requiere el template
    context = {
      'inmueble': inmueble,
      'regiones': regiones,
      'comunas': comunas, 
      'cod_region': cod_region_actual,
    }
    return render(req, 'editar_inmueble.html', context)
  else:
    return HttpResponse('es un POST')
  
@user_passes_test(solo_arrendadores)
def eliminar_inmueble(req, id):
  eliminar_inmueble_service(id)
  messages.error(req, 'Inmueble ha sido eliminado')
  return redirect('/account/profile/')

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

# Filtros -->

def filtrar_inmuebles(region_cod, comuna_cod, palabra):
  # # Caso 1 : comuna_cod != ''abs
  # if comuna_cod != '':
  #   comuna = Comuna.objects.get(cod = comuna_cod)
  #   return Inmueble.objects.filter(comuna = comuna)
  
  # # Caso 2: comuna_cod == '' and region_cod != ''
  # elif comuna_cod == '' and region_cod != '':
  #   region = Region.objects.get(cod = region_cod)
  #   comunas = Comuna.objects.filter(region = region)
  #   return Inmueble.objects.filter(comuna__in = comunas, nombre__icontains = palabra)
  
  # # Caso 3: comuna_cod == '' and region_cod == ''
  # else:
  #   return Inmueble.objects.filter(nombre__icontains = palabra)
  
  # inmuebles = Inmueble.objects.all()
  # return inmuebles
  
  # Caso 2
  filtro_palabra = None 
  if palabra != '':
    filtro_palabra = Q(nombre__icontains=palabra) | Q(descripcion__icontains=palabra)
  
  filtro_ubicacion = None
  if comuna_cod != '':
    comuna = Comuna.objects.get(cod = comuna_cod)
    filtro_ubicacion = Q(comuna=comuna)
    
  elif region_cod != '':
    region = Region.objects.get(cod = region_cod)
    comunas_region = region.comunas.all()
    filtro_ubicacion = Q(comuna__in = comunas_region)
  
    # Caso 2.1-2-3
  if filtro_ubicacion is None and filtro_palabra is None:
    return Inmueble.objects.all()
  elif filtro_ubicacion is not None and filtro_palabra is None:
    return Inmueble.objects.filter(filtro_ubicacion)
  elif filtro_ubicacion is None and filtro_palabra is not None:
    return Inmueble.objects.filter(filtro_palabra)
  elif filtro_ubicacion is not None and filtro_palabra is not None:
    return Inmueble.objects.filter(filtro_palabra & filtro_ubicacion)
  