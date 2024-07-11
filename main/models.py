from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.

class UserProfile(models.Model):
  direccion = models.CharField(max_length=255, blank=False)
  telefono_personal = models.CharField(max_length=25, null=True)
  user = models.OneToOneField(User,
    related_name='usuario',
    on_delete=models.CASCADE
  )
  def __str__(self):
    nombre = self.user.first_name
    apellido = self.user.last_name
    usuario = self.user.username
    return f'{nombre} {apellido} | {usuario}'
  
class Region(models.Model):
  cod = models.CharField(max_length=5, primary_key=True)
  nombre = models.CharField(max_length=255)

class Comuna(models.Model): 
  cod = models.CharField(max_length=5, primary_key=True)
  nombre = models.CharField(max_length=255)
  region = models.ForeignKey(
    Region,
    on_delete=models.RESTRICT,
    related_name='comunas'
  )
  def __str__(self):
    nombre = self.nombre
    return f'{nombre}'
  
class Inmueble(models.Model):
  inmuebles = (
    ('casa', 'Casa'),
    ('departamento', 'Departamento'),
    ('parcela', 'Parcela')
  )
  nombre = models.CharField(max_length=50)
  descripcion = models.TextField(max_length=1500)
  m2_construidos = models.IntegerField(validators=[MinValueValidator(1)])
  m2_totales = models.IntegerField(validators=[MinValueValidator(1)]) # O del terreno
  num_estacionamientos = models.IntegerField(validators=[MinValueValidator(0)], default=0)
  num_habitaciones = models.IntegerField(validators=[MinValueValidator(1)], default=1)
  num_baños = models.IntegerField(validators=[MinValueValidator(0)], default=0)
  direccion = models.CharField(max_length=255)
  precio_mensual_arriendo = models.IntegerField(validators=[MinValueValidator(1000)], null=True)
  #precio_ufs = models.FloatField(validators=[MinValueValidator(1.0)], null=True)
  tipo_de_inmueble = models.CharField(max_length=20, choices=inmuebles)
  #llaves foraneas
  comuna = models.ForeignKey(
    Comuna, 
    related_name='inmuebles',
    on_delete=models.RESTRICT
    )
  propietario = models.ForeignKey(
    User, 
    related_name='inmuebles',
    on_delete=models.RESTRICT, 
    )
  def __str__(self):
    nombre = self.nombre
    comuna = self.comuna
    return f' {nombre}, {comuna} | {tipo_inmueble}'
  
class Solicitud(models.Model):
  estados = (
    ('pendiente', 'Pendiente'), 
    ('rechazada', 'Rechazada'), 
    ('aprobada', 'Aprobada')
  )
  inmueble = models.ForeignKey(
    Inmueble, 
    related_name='solicitudes',
    on_delete=models.CASCADE, 
  )
  arrendador = models.ForeignKey(
    User, 
    related_name='solicitudes', 
    on_delete=models.CASCADE
  )
  fecha = models.DateTimeField(auto_now_add=True)
  estado = models.CharField(max_length=50, choices=estados)
