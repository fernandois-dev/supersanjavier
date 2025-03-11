
import django
from django.core.management import call_command
import data.db  # Importa la configuración
from django.conf import settings
import os


django.setup()

# Generar y aplicar migraciones
call_command("makemigrations", "data")
call_command("migrate")