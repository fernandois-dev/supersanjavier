from rest_framework import serializers

from modules.inventario.models import Caja

class CajaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caja
        fields = '__all__'