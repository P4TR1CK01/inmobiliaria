from django.core.management.base import BaseCommand
from main.services import *

# Se ejecuta usando python manage.py test_client

class Command(BaseCommand):
  def handle(self, *args, **kwargs):
    
    #crear_user('11.222.333-4', 'Marge', 'Simpson', 'néeBouvier@aol.com', '12345', '12345', 'Calle falsa 123')
    #editar_user('22.333.444-5', 'Homero', 'Simpson', 'amantedelacomida53@aol.com', '654321', '654321', ' Avenida Siempreviva 742, '987654321')
    #crear_inmueble('Casa Grande blanca en Villa Alemana', 'Hermosa casa de equina con gran patio', 90, 180, 3, 3, 2, 'Calle 22', 450000, 'casa', '05804', '11.111.111-1')
    #eliminar_inmueble(1)
    #editar_inmueble(3, 'Parcela Amarilla en Villa Alemana', 'Hermosa parcela amarilla en la esquina', 90, 180, 3, 3, 2, 'Calle 22', 750000, 'parcela', 'Villa Alemana', '22.2222.222-2')
    return 'Funciona correctamente'
  
    inmuebles = obtener_inmuebles_comunas()
    import pdb; pdb.set_trace()