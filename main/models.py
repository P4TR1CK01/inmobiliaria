from django.db import models

# Create your models here.

class User(models.Model):
  nombres = models.CharField(max_length=50)
  apellidos = models.CharField(max_length=50)
  rut = models.CharField(max_length=12, unique=True)
  direccion = models.CharField(max_length=100)
  telefono_personal = models.CharField(max_length=20)
  correo_electronico = models.EmailField(unique=True)
  tipo_usuario = models.CharField(max_length=10, choices=[('arrendatario', 'Arrendatario'), ('arrendador,' 'Arrendador')])

class Inmueble(moels.Model):
  nombre = models.CharField(max_length=50)
  descripcion = models.TextField()
  m2_construidos = models.IntegerField()
  m2_totaes = models.IntegerField()
  estacionamientos = models.IntegerField()
  habitaciones = models.IntegerField()
  baños = models.IntegerField()
  direccion = models.CharField(max_length=100)
  comuna = models.CharField(max_length=50)
  tipo_inmueble = models.CharField(max_length=10, choices=[('casa', 'Casa'), ('departamento', 'Departamento'), ('parcela', 'Parcela')])
  precio_mensual_arriendo = models.DecimalField(max_digits=10, decimal_places=2)

class SolicitudArriendo(models.Model):
  Inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
  arrendatario = models.ForeignKey(User, on_delete=models.CASCADE)
  fecha_solicitud = models.DateTimeField(auto_now_add=True)
  