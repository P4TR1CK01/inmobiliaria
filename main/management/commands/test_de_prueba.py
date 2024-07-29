from django.core.management.base import BaseCommand
from main.services import *

# Se ejecuta python manage.py test_de_prueba
class Command(BaseCommand):
  #def handle(self, *args, **kwargs):
    #prueba de funciones desde services.py
  print('Test de programa')
    #crear_user('11.222.333-4', 'Marge', 'Simpson', 'néeBouvier@aol.com', '12345', '12345', 'Calle falsa 123')
    #editar_user('22.333.444-5', 'Homero', 'Simpson', 'amantedelacomida53@aol.com', '654321', '654321', ' Avenida Siempreviva 742, '987654321')
    #eliminar_user('11.222.333-4')
    #crear_inmueble('Casa Grande blanca en Villa Alemana', 'Hermosa casa de equina con gran patio', 90, 180, 3, 3, 2, 'Calle 22', 450000, 'casa', '05804', '11.111.111-1')
    #eliminar_inmueble(1)
    #editar_inmueble(3, 'Parcela Amarilla en Villa Alemana', 'Hermosa parcela amarilla en la esquina', 90, 180, 3, 3, 2, 'Calle 22', 750000, 'parcela', 'Villa Alemana', '22.2222.222-2')
  crear_user('13343-2', 'bola', 'depelos', 'bola@hola', '1234', '1234', 'calle 2', 'arrendatario', '6556565')

  #return 'Funciona correctamente'
  