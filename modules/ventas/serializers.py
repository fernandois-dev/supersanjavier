from rest_framework import serializers

from modules.ventas.models import Caja, DetalleVenta, Venta

class CajaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caja
        fields = '__all__'
        
class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = '__all__'
        
class VentaSerializer(serializers.ModelSerializer):
    detalle_venta = DetalleVentaSerializer(many=True, read_only=True)

    class Meta:
        model = Venta
        fields = ['id', 'caja', 'fecha', 'total', 'state', 'usuario', 'detalle_venta']
        