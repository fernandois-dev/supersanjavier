import os
import requests
import configparser
from django.db import transaction

from modules.inventario.models import Categoria, Producto
from modules.ventas.models import Caja

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

def get_api_categorias_url():
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
    return f"http://{ip_servidor}:{port_servidor}/api/categorias"

def get_api_cajas_url():
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
    return f"http://{ip_servidor}:{port_servidor}/api/cajas"

def sync_products(api_url):

    try:
        # Fetch product data from the API
        response = requests.get(api_url)
        response.raise_for_status()
        products = response.json()

        # Insert products into the database
        with transaction.atomic():
            # Delete all existing products before synchronization
            # Producto.objects.all().delete()
            for product in products:
                categoria = Categoria.objects.filter(id=product['categoria']).first() if product.get('categoria') else None
                Producto.objects.update_or_create(
                    id=product['id'],
                    defaults={
                        'nombre': product['nombre'],
                        'codigo': product['codigo'],
                        'descripcion': product.get('descripcion', ''),
                        'precio_compra': product['precio_compra'],
                        'precio_venta': product['precio_venta'],
                        'stock': product['stock'],
                        'activo': product.get('activo', True),
                        'categoria': categoria,
                    }
                )
            # elimina los productos que no esten en la api
            ids = [product['id'] for product in products]
            Producto.objects.exclude(id__in=ids).delete()
            
        print("Products synchronized successfully.")
    except requests.RequestException as e:
        print(f"Error fetching products from API: {e}")
    except Exception as e:
        print(f"Error inserting products into the database: {e}")
        
def sync_categories(api_url):
    try:
        # Fetch category data from the API
        response = requests.get(api_url)
        response.raise_for_status()
        categories = response.json()

        # Insert categories into the database
        with transaction.atomic():
            # Delete all existing categories before synchronization
            # Categoria.objects.all().delete()
            for category in categories:
                Categoria.objects.update_or_create(
                    id=category['id'],
                    defaults={
                        'nombre': category['nombre'],
                        'descripcion': category.get('descripcion', ''),
                    }
                )
            # elimina las categorias que no esten en la api
            ids = [category['id'] for category in categories]
            Categoria.objects.exclude(id__in=ids).delete()
            
        print("Categories synchronized successfully.")
    except requests.RequestException as e:
        print(f"Error fetching categories from API: {e}")
    except Exception as e:
        print(f"Error inserting categories into the database: {e}")
    
def sync_cajas(api_url):
    try:
        # Fetch category data from the API
        response = requests.get(api_url)
        response.raise_for_status()
        cajas = response.json()

        # Insert categories into the database
        with transaction.atomic():
            # Delete all existing categories before synchronization
            # Categoria.objects.all().delete()
            for caja in cajas:
                Caja.objects.update_or_create(
                    id=caja['id'],
                    defaults={
                        'nombre': caja['nombre'],
                        'descripcion': caja.get('descripcion', ''),
                    }
                )
            # elimina las categorias que no esten en la api
            ids = [caja['id'] for caja in cajas]
            Caja.objects.exclude(id__in=ids).delete()
            
        print("Cajas synchronized successfully.")
    except requests.RequestException as e:
        print(f"Error fetching cajas from API: {e}")
    except Exception as e:
        print(f"Error inserting cajas into the database: {e}")
        