from fastapi import FastAPI
from modules.inventario.models import Producto
from data.serializers import ProductoSerializer
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


def start_fastapi(app: FastAPI, port: int):
    """
    Inicia el servidor FastAPI en un hilo separado.
    """
    config = Config(app=app, host="0.0.0.0", port=port, log_level="info")
    server = Server(config)
    server.run()