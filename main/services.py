from django.contrib.auth.models import User
from main.models import UserProfile, Inmueble, Comuna, Region
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db.models import Q
from django.db import connection

def crear_inmueble(nombre, descripcion, m2_construidos, m2_totales, num_estacionamientos, num_habitaciones, num_baños, direccion, tipo_inmueble, precio_mensual, comuna_cod, propietario_rut):
  comuna = Comuna.objects.get(cod=comuna_cod)
  propietario = User.objects.get(username=propietario_rut)
  Inmueble.objects.create(
    nombre = nombre,
    descripcion = descripcion,
    m2_construidos = m2_construidos,
    m2_totales = m2_totales,
    num_estacionamientos = num_estacionamientos,
    num_habitaciones = num_habitaciones,
    num_baños = num_baños,
    direccion = direccion,
    tipo_inmueble = tipo_inmueble,
    precio_mensual = precio_mensual,
    comuna = comuna,
    propietario = propietario
  )

def editar_inmueble(inmueble_id, nombre, descripcion, m2_construidos, m2_totales, num_estacionamientos, num_habitaciones, num_baños, direccion, tipo_inmueble, precio_mensual, comuna, propietario_rut):
    inmueble = Inmueble.objects.get(id=inmueble_id)
    comuna = Comuna.objects.get(nombre=comuna)
    inmueble.nombre = nombre
    inmueble.descripcion = descripcion 
    inmueble.m2_construidos = m2_construidos
    inmueble.m2_totales = m2_totales
    inmueble.num_estacionamientos = num_estacionamientos
    inmueble.num_habitaciones = num_habitaciones
    inmueble.num_baños = num_baños
    inmueble.direccion = direccion 
    inmueble.tipo_inmueble = tipo_inmueble
    inmueble.precio = precio_mensual
    inmueble.comuna = comuna
    inmueble.propietario = propietario_rut
    inmueble.save()

def eliminar_inmueble(inmueble_id):
  inmueble = Inmueble.objects.get(id=inmueble_id)
  inmueble.delete()

def crear_user(username, first_name, last_name, email, password, pass_confirm, direccion, telefono=None):
  if password != pass_confirm:
    messages.error(req, 'Las contraseñas no coinciden')
    return False
  # Creamos el objeto user
  try:
    user = User.objects.create_user(
      username, 
      email, 
      password, 
      first_name = first_name, 
      last_name = last_name
    )
  except IntegrityError:
    # Se le da feedback al usuario
    messages.error(req, 'Este RUT ya está en uso, porfavor ingrese otro') 
    return False
  except ValidationError:
    messages.error(req, 'Este E-mail ya está en uso, porafvor ingrese otro')
    return False
    
  # Creamos el UserProfile
  UserProfile.objects.create(
    user = user, 
    direccion = direccion, 
    telefono = telefono,
    rol = rol)
  # Si todo sale bien, retornamos True
  messages.success(req, 'Su usuario ha sido creado')
  return True, None

def editar_user(username, first_name, last_name, email, password, direccion, telefono=None):
  # Nos traemos el 'user' y modificamos sus datos
  user = User.objects.get(username=username)
  user.first_name = first_name
  user.last_name = last_name
  user.email = email
  user.set_password(password)
  user.save()
  # Nos traemos el 'user_profile' y modificamos sus datos
  user_profile = UserProfile.objects.get(user=user)
  user_profile.direccion = direccion
  user_profile.telefono = telefono
  user_profile.save()

def editar_user_sin_password(username, first_name, last_name, email, direccion, rol,  telefono=None):
  # Nos traemos el 'user' y modificamos sus datos
  user = User.objects.get(username=username)
  user.first_name = first_name
  user.last_name = last_name
  user.email = email
  user.save()
  # Nos traemos el 'user_profile' y modificamos sus datos
  user_profile = UserProfile.objects.get(user=user)
  user_profile.direccion = direccion
  user_profile.telefono = telefono
  user_profile.rol = rol
  user_profile.save()
  
def eliminar_user(rut):
  eliminar = User.objects.get(Usernname = rut)
  eliminar.delete()
  
def cambiar_contraseña(req, password, repeat_password):
  if password != repeat_password:
    messages.error(req, 'Las contraseñas no coinciden')
    return
  request.user.set_password(password)
  request.user.save()
  messages.success(req, 'Contraseña actualizaca correctamente')
  
def obtener_inmuebles_comunas(filtro):
  if filtro is None:
    return Inmueble.objects.all().order_by('comuna')
  # si llegamos acá, significa que SI hay un filtro
  # select * from main_inmueble where nombre like '%Elegante%' or descripcion like '%Elegante%';
  return Inmueble.objects.filter(Q(nombre__icontains=filtro) | Q(descripcion__icontains=filtro)).order_by('comuna')

def obtener_inmuebles_region(filtro):
  consulta = '''
    select I.nombre, I.descripcion, R.nombre as region from main_inmueble as I
    join main_comuna as C on I.comuna_id = C.cod
    join main_region as R on C.region_id = R.cod
    order by R.cod;
  '''
  cursor = connection.cursor()
  cursor.execute(consulta)
  registros = cursor.fetchall() # LAZY LOADING
  return registros

