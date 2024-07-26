import csv
from django.core.management.base import BaseCommand
from main.services import obtener_inmuebles_region

class Command(BaseCommand):
  def add_arguments(self, parser):
    # Argumentos posicionales
    parser.add_argument('-f', '--f', type=str, nargs='+')
  def handle(self, *args, **kwargs):
    file = open('data/inmuebles_region.txt', 'w',encoding='utf-8')
    filtro = None
    if 'f' in kwargs.keys() and kwargs['f'] is not None:
      filtro = kwargs['f'][0]
    inmuebles = obtener_inmuebles_region(filtro)
    for inmueble in inmuebles:
      linea = f'{inmueble[0]} \t {inmueble[1]} \t {inmueble[2]}'
      file.write(linea)
      file.write('\n')
      print(inmueble)
    archivo.close()