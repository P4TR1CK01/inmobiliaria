from main.models import UserProfile
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

def crear_inmueble(nombre:str, descripcion:str, m2_construidos:int, m2_totales:int, num_estacionamientos:int, num_habitaciones:int, num_baños:int, direccion:str, precio:int, precio_ufs:int, comuna:str, propietario:str):
  
  comuna = Comuna.objects.get(nombre=comuna)
  
  propietario = User.objects.get(username=rut_propietario)
  
  Inmueble.objects.create(
    nombre = nombre,
    descripcion = descripcion,
    m2_construidos = m2_construidos,
    m2_totales = m2_totales,
    num_estacionamientos = num_estacionamientos,
    num_habitaciones = num_habitaciones,
    num_baños = num_baños,
    direccion = direccion, 
    precio = precio,
    precio_ufs = precio_ufs,
    tipo_de_inmueble = tipo_de_inmueble,
    comuna = comuna,
    propietario = propietario
  )

def editar_inmueble(inmueble_id:int, nombre:str, descripcion:str, m2_construidos:int, m2_totales:int, num_estacionamientos:int, num_habitaciones:int, num_baños:int, direccion:str, precio_mensual_arriendo:int, tipo_de_inmueble:str, comuna:str, rut_propietario:str):
  inmueble = Inmueble.objects.get=(id=inmueble_id)
  comuna = Comuna.objects.get(nombre=comuna)
  propietario = User.objects.get(username=rut_propietario)
  inmueble.nombre = nombre
  inmueble.descripcion = descripcion
  inmueble.m2_construidos = m2_construidos
  inmueble.m2_totales = m2_totales
  inmueble.num_estacionamientos = num_estacionamientos
  inmueble.num_habitaciones = num_habitaciones
  inmueble.num_baños = num_baños
  inmueble.direccion = direccion
  inmueble.precio_mensual_arriendo = precio_mensual_arriendo
  inmueble.tipo_de_inmueble = tipo_de_inmueble
  inmueble.comuna = comuna
  inmueble.propietario = propietario
  inmueble.save()

def eliminar_inmuebles(inmueble_id):
  eliminar = Inmueble.objects.get(id=inmueble_id)
  eliminar.delete()

def crear_user(username:str, first_name:str, last_name:str, email:str, password:str, pass_confirm:str, direccion:str, telefono:str=None) -> list[bool, str]:
# 1.Validamos que las password coincidan
  if password != pass_confirm:
    return False, 'las contraseñas no coinciden'
# 2. Creamos el objeto user
  try:
    user = User.objects.create_user(
      username,
      email,
      password,
      first_name=first_name, 
      last_name=last_name
    )
#3. Creamos el UserProfile
  except IntegrityError:
    return False, 'El rut ya existe'
  UserProfile.objects.create(
    user=user, 
    direccion=direccion, 
    telefono=telefono
  )
#4. Si todo sale bien, retornamos True
  return True

def editar_user(username:str, first_name:str, last_name:str, email:str, password:str, pass_confirm:str, direccion:str, telefono:str=None):
  #1. Nos traemos el 'user' y modificamos sus datos
  user = User.objects.get(username=username)
  user.first_name = first_name
  user.last_name = last_name
  user.email = email
  user.set_password(password)
  user.save()
  #2. Nos traemos el 'userprofile' y modificamos sus datos
  userprofile = UserProfile.objects.get(user=user)
  userprofile.direccion = direccion
  userprofile.telefono = telefono
  userprofile.save()

def eliminar_user(rut:str):
  eliminar = User.objects.get(username=rut)
  eliminar.delete()