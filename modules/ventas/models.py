from datetime import datetime
from django.db import models
from modules.comun.models import Usuario
from modules.inventario.models import Producto
from data.custom_fields import CustomAutoField, CustomBooleanField, CustomCharField, CustomDateTimeField, CustomForeignKey, CustomIntegerField, CustomMoneyField

VENTA_STATE_CHOICES = [
    ("BR", "Borrador"),
    ("CR", "Creada"),
    ("AN", "Anulada"),
]

class Caja(models.Model):
    id = CustomAutoField(primary_key=True, verbose_name="ID", null=False, blank=False, editable=False)
    numero = CustomIntegerField(verbose_name="Número", null=False, blank=False, unique=True, default=0)
    nombre = CustomCharField(max_length=100, verbose_name="Nombre", null=False, blank=False)
    activo = CustomBooleanField(verbose_name="Activo", null=True, blank=True, default=True)
    
    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name = "Caja"
        verbose_name_plural = "Cajas"
        ordering = ["-id"]
    
    
class ActividadCaja(models.Model):
    id = CustomAutoField(primary_key=True, verbose_name="ID", null=False, blank=False, editable=False)
    caja = CustomForeignKey(Caja, verbose_name="Caja", on_delete=models.PROTECT, null=False, blank=False)
    fecha_apertura = CustomDateTimeField(verbose_name="Fecha Apertura", null=False, blank=False, default=None)
    fecha_cierre = CustomDateTimeField(verbose_name="Fecha Cierre", null=True, blank=True)
    usuario = CustomForeignKey(Usuario, verbose_name="Usuario Apertura", on_delete=models.SET_NULL, null=True, blank=False, related_name="usuario")
    monto_apertura = CustomMoneyField(verbose_name="Monto Apertura", null=True, blank=True, default=0)
    monto_cierre = CustomMoneyField(verbose_name="Monto Cierre", null=True, blank=True, default=0)

    def __str__(self):
        return f"{self.caja} - {self.fecha}"

    class Meta:
        verbose_name = "Actividad Caja"
        verbose_name_plural = "Actividad Cajas"
        ordering = ["-id"]


class Venta(models.Model):
    id = CustomAutoField(primary_key=True, verbose_name="ID", null=False, blank=False, editable=False)
    fecha = CustomDateTimeField(verbose_name="Fecha", null=False, blank=False, default=datetime.now)
    caja = CustomForeignKey(Caja, verbose_name="Caja", on_delete=models.PROTECT, null=False, blank=False)
    usuario = CustomForeignKey(Usuario, verbose_name="Usuario", on_delete=models.SET_NULL, null=True, blank=True)
    total = CustomMoneyField(verbose_name="Total", null=False, blank=False, read_only=True)
    state = CustomCharField(max_length=3, verbose_name="Estado", default="BR" ,null=True, blank=True, choices=VENTA_STATE_CHOICES)

    def __str__(self):
        return f"{self.id} - {self.fecha}"

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ["-id"]
        
    def delete(self):
        # Custom logic to manage relations before delete
        super().delete()
        
class DetalleVenta(models.Model):
    id = CustomAutoField(primary_key=True, verbose_name="ID", null=False, blank=False, editable=False)
    venta = CustomForeignKey(Venta, verbose_name="Venta", on_delete=models.CASCADE, null=False, blank=False, related_name='detalle_venta')
    producto = CustomForeignKey(Producto, verbose_name="Producto", on_delete=models.PROTECT, null=False, blank=False, is_sortable=True)
    cantidad = CustomIntegerField(verbose_name="Cantidad", null=False, blank=False)
    precio = CustomMoneyField(verbose_name="Precio", null=False, blank=False)
    descuento = CustomMoneyField(verbose_name="Descuento", null=False, blank=False, default=0)
    total = CustomMoneyField(verbose_name="Total", null=False, blank=False, read_only=True, default=0)

    def __str__(self):
        return f"{self.id} - {self.producto}"

    class Meta:
        verbose_name = "Detalle Venta"
        verbose_name_plural = "Detalle Ventas"
        ordering = ["-id"]
    
    def delete(self):
        # Custom logic to manage relations before delete
        super().delete()