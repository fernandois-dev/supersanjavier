import json
import os
import django

# Configura el entorno de Django
import settings 
django.setup()

from modules.inventario.models import Categoria, Producto

with open("ejemplo_productos_supermercado.json", encoding="utf-8") as f:
    data = json.load(f)

# Crear o actualizar categorías
categoria_objs = {}
for cat in data["categorias"]:
    obj, _ = Categoria.objects.update_or_create(
        nombre=cat["nombre"],
        defaults={
            "descripcion": cat.get("descripcion", ""),
            "porcentaje_iva": cat.get("porcentaje_iva", 19),
            "activo": cat.get("activo", True),
        }
    )
    categoria_objs[cat["nombre"]] = obj

# Crear productos
for prod in data["productos"]:
    Producto.objects.update_or_create(
        codigo=prod["codigo"],
        defaults={
            "nombre": prod["nombre"],
            "codigo_barras": prod.get("codigo_barras"),
            "precio_compra": prod.get("precio_compra"),
            "precio_venta": prod["precio_venta"],
            "stock": prod.get("stock", 0),
            "categoria": categoria_objs.get(prod["categoria_nombre"]),
            "activo": prod.get("activo", True),
        }
    )

print("✅ Datos cargados correctamente.")