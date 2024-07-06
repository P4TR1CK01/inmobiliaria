from django import forms
from .models import User, Inmueble, SolicitudArriendo

class UserForm(forms.ModelForm):  
  class Meta:
    model = User
    fields = ('nombres', 'apellidos', 'rut', 'direccion', 'telefono_personal', 'correo_electronico', 'tipo_usuario')
    
class InmuebleForm(forms.ModelForm):
  class Meta:
    model = Inmueble
    fields = ('nombre', 'descripcion', 'm2_construidos', 'm2_totales', 'estacionamientos', 'habitaciones', 'banos', 'direccion', 'comuna', 'tipo_inmueble', 'precio_mensual_arriendo')

class SolicitudArriendoForm(forms.ModelForm):
  class Meta:
    model = SolicitudArriendo
    fields = ('inmueble', 'arrendatario', 'fecha_solicitud')