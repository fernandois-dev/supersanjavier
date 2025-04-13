import os
import sys
import django
from django.conf import settings
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "apps")))


# Configurar Django ORM


settings.configure(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",  # Puedes cambiar a PostgreSQL/MySQL
            "NAME": "data/database.db",
            # "NAME": os.path.join(os.path.dirname(__file__), "data/database.db"),
            # "NAME": "database.db",
        }
    },
    INSTALLED_APPS=[
        'modules.comun', 
        'modules.inventario', 
        'modules.ventas',
        # 'modules.api',
        ],
    LANGUAGE_CODE = "es",
    USE_I18N = True,
    USE_L10N = True,
    USE_TZ = False
)
