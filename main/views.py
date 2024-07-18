from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.services import editar_user_sin_password

# Create your views here.
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
      req.POST['telefono'])
  else:
    editar_user_sin_password(
      current_user.username,
      req.POST['first_name'],
      req.POST['last_name'],
      req.POST['email'],
      req.POST['direccion'])
  messages.success(req, "Ha actualizado sus datos con éxito")
  return redirect('/')

# pendientes para trabajar con grupos
def solo_arrendadores(req):
  return HttpResponse('sólo arrendadores')

def solo_arrendatarios(req):
  return HttpResponse('sólo arrendatarios')