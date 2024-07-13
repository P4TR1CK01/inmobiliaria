
from django.core.management.base import BaseCommand
import csv
from main.models import Comuna
# Se ejecuta usando python manage.py test_client

class Command(BaseCommand):
  def handle(self, *args, **kwargs):
    archivo = open('data/comunas.csv',
    encoding='utf-8')
    reader = csv.reader(archivo, delimiter=';')
    next(reader) # Se salta la primera linea
    nombre_regiones =[]
    for fila in reader:
      #si no tenemos el nombre de la region previamente guardada, la agregamos a la base de datos
      Comuna.objects.create(nombre=fila[0], cod=fila[1], region_id=fila[3])
