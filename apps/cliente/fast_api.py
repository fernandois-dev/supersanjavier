from fastapi import FastAPI
from modules.inventario.models import Categoria, Producto
from modules.inventario.serializers import CategoriaSerializer, ProductoSerializer
from modules.ventas.models import Venta
from modules.ventas.serializers import UltimaVentaSerializer, VentaSerializer
from uvicorn import Config, Server

# Crear la instancia de FastAPI
fastapi_app = FastAPI()

# Definir las rutas de FastAPI

@fastapi_app.get("/api/ventas/")
def get_ventas(fecha_desde: str = None):
    """
    Endpoint para obtener la lista de ventas.
    """
    ventas = Venta.objects.all()
    if fecha_desde:
        ventas = ventas.filter(fecha__gte=fecha_desde)
    serializer = VentaSerializer(instance=ventas, many=True)
    return serializer.data

@fastapi_app.get("/api/fecha-ultima-venta/")
def get_fecha_ultima_venta():
    """
    Endpoint para obtener la fecha de la última venta.
    """
    ultima_venta = Venta.objects.latest('fecha')
    serializer = UltimaVentaSerializer(instance=ultima_venta)
    return serializer.data


def start_fastapi(app: FastAPI, port: int):
    """
    Inicia el servidor FastAPI en un hilo separado.
    """
    config = Config(app=app, host="0.0.0.0", port=port, log_level="info")
    server = Server(config)
    server.run()