import django

import settings  # Cargar configuración del ORM
django.setup()

import random
from faker import Faker
from apps.inventario.models import Producto, Categoria

fake = Faker()

def generar_datos_ejemplo():
    # Crear 10 categorías de ejemplo
    nombres_categorias = [
        "Electrónica", "Hogar", "Ropa", "Deportes", "Juguetes",
        "Alimentos", "Bebidas", "Libros", "Muebles", "Herramientas"
    ]
    categorias = []
    for nombre in nombres_categorias:
        categoria = Categoria(
            nombre=nombre,
            descripcion=fake.text(max_nb_chars=50),
            porcentaje_iva=random.choice([5, 10, 19]),
            activo=True
        )
        categorias.append(categoria)
    Categoria.objects.bulk_create(categorias)

    # Obtener las categorías creadas
    categorias_creadas = list(Categoria.objects.all())

    # Crear 500 productos de ejemplo
    productos = []
    for _ in range(500):
        categoria = random.choice(categorias_creadas)
        producto = Producto(
            codigo=fake.unique.bothify(text="PROD-####"),
            nombre=fake.word().capitalize(),
            codigo_barras=fake.unique.ean(length=13),
            precio_compra=round(random.uniform(10, 500), 2),
            precio_venta=round(random.uniform(20, 1000), 2),
            stock=random.randint(0, 100),
            categoria=categoria,
            activo=random.choice([True, False])
        )
        productos.append(producto)
    Producto.objects.bulk_create(productos)

    print("Datos de ejemplo generados correctamente.")

if __name__ == "__main__":
    generar_datos_ejemplo()