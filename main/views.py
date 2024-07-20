from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.services import editar_user_sin_password
from django.contrib.auth.decorators import user_passes_test
from main.models import Inmueble, Region, Comuna
from main.services import crear_inmueble as crear_inmueble_service
# Create your views here.

def calcular_clase(tipo_mensaje):
  if tipo_mensaje == 'error':
    return 'danger'
  return tipo_mensaje

@login_required
def home(req):
  return render(req, 'home.html')

@login_required
def profile(req):
  return render(req, 'profile.html')

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
  messages.success(req, "Ha actualizado sus datos con éxito")
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
  messages.success(req, "Ha cambiado su contraseña con éxito")
  return redirect('/accounts/profile')

# pendientes para trabajar con grupos

def solo_arrendadores(user):
  if user.user_profile.rol == 'arrendador' or user.is_staff ==True:
    return True
  else:
    messages.error(req, '')
    return False
  
  @user_passes_test(solo_arrendadores)
  def nuevo_inmueble(req):
    return render(req, 'nuevo_inmueble.html')

def solo_arrendatarios(req):
  return HttpResponse('sólo arrendatarios')

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

#vamos a crear un test que solo pasan los 'arrendadores'

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