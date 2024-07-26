import csv
from django.core.management.base import BaseCommand
from main.services import obtener_inmuebles_comunas

class Command(BaseCommand):
  def add_arguments(self, parser):
    # Argumentos posicionales
    parser.add_argument('-f', '--f', type=str, nargs='+')
  def handle(self, *args, **kwargs):
    file = open('data/inmuebles_comuna.txt', 'w',encoding='utf-8')
    filtro = None
    if 'f' in kwargs.keys() and kwargs['f'] is not None:
      filtro = kwargs['f'][0]
    inmuebles = obtener_inmuebles_comunas(filtro)
    #with open('data/inmuebles_comuna.txt', 'w') as file:
    for inmueble in inmuebles:
      linea = f'{inmueble.nombre}\t{inmueble.descripcion}\t{inmueble.comuna.nombre}'
      file.write(linea)
      file.write('\n')
      print(linea)
    file.close()