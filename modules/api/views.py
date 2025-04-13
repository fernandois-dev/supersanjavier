from modules.api.models import ProductoSerializer
from modules.inventario.models import Producto


from rest_framework.generics import ListAPIView

class ProductoListView(ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

