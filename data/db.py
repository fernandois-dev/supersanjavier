import os
import django
from django.conf import settings

# Configurar Django ORM


settings.configure(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",  # Puedes cambiar a PostgreSQL/MySQL
            "NAME": os.path.join(os.path.dirname(__file__), "database.db"),
            # "NAME": "database.db",
        }
    },
    INSTALLED_APPS=["data"],  # Usar la ruta completa
    LANGUAGE_CODE = "es",
    USE_I18N = True,
    USE_L10N = True
)

# Inicializar Django
# django.setup()