from fastapi import FastAPI
from modules.inventario.models import Categoria, Producto
from modules.inventario.serializers import CategoriaSerializer, ProductoSerializer
from modules.ventas.models import Caja
from modules.ventas.serializers import CajaSerializer
from uvicorn import Config, Server

# Crear la instancia de FastAPI
fastapi_app = FastAPI()

# Definir las rutas de FastAPI
@fastapi_app.get("/api/productos/")
def get_productos():
    """
    Endpoint para obtener la lista de productos.
    """
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    return serializer.data

@fastapi_app.get("/api/categorias/")
def get_categorias():
    """
    Endpoint para obtener la lista de categorías.
    """
    categorias = Categoria.objects.all()
    serializer = CategoriaSerializer(categorias, many=True)
    return serializer.data

@fastapi_app.get("/api/cajas/")
def get_cajas():
    """
    Endpoint para obtener la lista de cajas.
    """
    cajas = Caja.objects.all()
    serializer = CajaSerializer(cajas, many=True)
    return serializer.data

def start_fastapi(app: FastAPI, port: int):
    """
    Inicia el servidor FastAPI en un hilo separado.
    """
    config = Config(app=app, host="0.0.0.0", port=port, log_level="info")
    server = Server(config)
    server.run()