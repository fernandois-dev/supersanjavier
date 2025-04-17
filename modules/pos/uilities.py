import os
import requests
import configparser
from django.db import transaction

from modules.inventario.models import Producto

def get_api_productos_url():
    # Read server configuration from pos_settings.cfg
    config_path = os.path.join(
        os.path.dirname(__file__), 
        '../../apps/cliente/pos_settings.cfg'
    )
    config_path = os.path.abspath(config_path)
    config = configparser.ConfigParser()
    config.read(config_path)

    ip_servidor = config.get('POS', 'ip_servidor')
    port_servidor = config.get('POS', 'port_servidor')
    return f"http://{ip_servidor}:{port_servidor}/api/productos"

def sync_products(api_url):

    try:
        # Fetch product data from the API
        response = requests.get(api_url)
        response.raise_for_status()
        products = response.json()

        # Insert products into the database
        with transaction.atomic():
            # Delete all existing products before synchronization
            Producto.objects.all().delete()
            for product in products:
                Producto.objects.update_or_create(
                    codigo=product['codigo'],
                    defaults={
                        'nombre': product['nombre'],
                        'descripcion': product.get('descripcion', ''),
                        'precio_compra': product['precio_compra'],
                        'precio_venta': product['precio_venta'],
                        'stock': product['stock'],
                        'activo': product.get('activo', True),
                    }
                )
        print("Products synchronized successfully.")
    except requests.RequestException as e:
        print(f"Error fetching products from API: {e}")
    except Exception as e:
        print(f"Error inserting products into the database: {e}")
        