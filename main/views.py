from django.shortcuts import render, redirect
from .models import User, Inmueble, SolicitudArriendo
from .forms import UserForm, InmuebleForm, SolicitudArriendoForm

# Create your views here.

def crear_usuario(req):
  if req.method == 'POST':
    form = UserForm(req.POST)
    if form.is_valid():
      form.save()
      return redirect('lista_usuarios')
  else:
    form = UserForm()
  return render(req, 'crear_usuario.html', {'form': form})
def lista_usuarios(req):
  usuarios = User.objects.all()
  return render(req, 'lista_usuarios.html', {'usuarios': usuarios})

def crear_inmueble(req):
  if req.method == 'POST':
    form = InmuebleForm(req.POST)
    if form.is_valid():
      form.save()
      return redirect('lista_inmuebles')
  else:
    form = InmuebleForm()
  return render(req, 'crear_inmueble.html', {'form': form})

def lista_inmuebles(req):
  inmuebles = Inmueble.objects.all()
  return render(req, 'lista_inmuebles.html', {'inmuebles': inmuebles})

def crear_solicitud_arriendo(req):
  if req.method == 'POST':
    form = SolicitudArriendoForm(req.POST)
    if form.is_valid():
      form.save()
      return redirect('lista_solicitudes_arriendo')
  else:
    form = SolicitudArriendoForm()
  return render(req, 'crear_solicitud_arriendo.html', {'form': form})

def lista_solicitudes_arriendo(req):
  solicitudes_arriendo = SolicitudArriendo.objects.all()
  return render(req, 'lista_solicitudes_arriendo.html', {'solicitudes_arriendo'})