from django.db import models
from data.custom_fields import CustomAutoField, CustomBooleanField, CustomCharField, CustomForeignKey, CustomIntegerField, CustomMoneyField, CustomDateTimeField


class VistaSincronizacion(models.Model):
    numero_caja = CustomCharField(max_length=100, verbose_name="Caja", null=False, blank=False, is_sortable=True, is_searchable=True, primary_key=True)
    ip = CustomCharField(max_length=100, verbose_name="IP", null=False, blank=False, is_sortable=True, is_searchable=True)
    ultima_venta = CustomDateTimeField(verbose_name="Ultima Venta", null=True, blank=True, is_sortable=True, is_searchable=True)
    ultima_sincronizacion = CustomDateTimeField(verbose_name="Ultima Sincronización", null=True, blank=True, is_sortable=True, is_searchable=True)

    class Meta:
        managed = False  # Indica que Django no debe gestionar este modelo
        db_table = 'vista_sincronizacion'  # Nombre de la vista en la base de datos
        
        
    