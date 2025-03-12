
import django
from django.core.management import call_command
import settings  # Importa la configuración
from django.conf import settings
import os


django.setup()

# Generar y aplicar migraciones
call_command("makemigrations", "comun")
call_command("makemigrations", "inventario")
call_command("makemigrations", "ventas")
call_command("migrate")