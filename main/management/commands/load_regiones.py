from django.core.management.base import BaseCommand
import csv
from main.models import Region

# Se ejecuta usando python manage.py test_client

class Command(BaseCommand):
  def handle(self, *args, **kwargs):
    archivo = open('data/comuna.csv', 'r')
    reader = csv.reader(archivo, delimiter=';')
    next(reader) # Se salta la primera linea
    nombre_regiones =[]
    for fila in reader:
      if fila[2] not in nombre_regiones:
      #si no tenemos el nombre de la region previamente guardada, la agregamos a la base de datos
        Region.objects.create(nombre=fila[2], cod=fila[3])
      #guardamos su nombre para no volver a agregarla
        nombre_regiones.append(fila[2]) 
    print (nombre_regiones)