from django.db import models
from apps.comun.models import Usuario
from apps.inventario.models import Producto
from data.custom_fields import CustomAutoField, CustomBooleanField, CustomCharField, CustomDateTimeField, CustomForeignKey, CustomIntegerField


class Caja(models.Model):
    id = CustomAutoField(primary_key=True, verbose_name="ID", null=False, blank=False, editable=False)
    nombre = CustomCharField(max_length=100, verbose_name="Nombre", null=False, blank=False)
    fecha_apertura = CustomDateTimeField(verbose_name="Fecha Apertura", null=False, blank=False)
    fecha_cierre = CustomDateTimeField(verbose_name="Fecha Cierre", null=True, blank=True)
    usuario_apertura = CustomForeignKey(Usuario, verbose_name="Usuario Apertura", on_delete=models.SET_NULL, null=True, blank=False, related_name="usuario_apertura")
    usuario_cierre = CustomForeignKey(Usuario, verbose_name="Usuario Cierre", on_delete=models.SET_NULL, null=True, blank=True, related_name="usuario_cierre")
    monto_apertura = CustomIntegerField(verbose_name="Monto Apertura", null=False, blank=False)
    monto_cierre = CustomIntegerField(verbose_name="Monto Cierre", null=True, blank=True)
    activo = CustomBooleanField(verbose_name="Activo", null=False, blank=False, default=True)

    def __str__(self):
        return f"{self.nombre} - {self.fecha_apertura}"

    class Meta:
        verbose_name = "Caja"
        verbose_name_plural = "Cajas"
    
    def delete(self):
        # Custom logic to manage relations before delete
        super().delete()
    
class ActividadCaja(models.Model):
    id = CustomAutoField(primary_key=True, verbose_name="ID", null=False, blank=False, editable=False)
    caja = CustomForeignKey(Caja, verbose_name="Caja", on_delete=models.CASCADE, null=False, blank=False)
    fecha = CustomDateTimeField(verbose_name="Fecha", null=False, blank=False)
    monto = CustomIntegerField(verbose_name="Monto", null=False, blank=False)
    descripcion = CustomCharField(max_length=200, verbose_name="Descripción", null=True, blank=True)

    def __str__(self):
        return f"{self.caja} - {self.fecha}"

    class Meta:
        verbose_name = "Actividad Caja"
        verbose_name_plural = "Actividad Cajas"
        
    def delete(self):
        # Custom logic to manage relations before delete
        super().delete()


class Venta(models.Model):
    id = CustomAutoField(primary_key=True, verbose_name="ID", null=False, blank=False, editable=False)
    fecha = CustomDateTimeField(verbose_name="Fecha", null=False, blank=False)
    caja = CustomForeignKey(Caja, verbose_name="Caja", on_delete=models.CASCADE, null=False, blank=False)
    usuario = CustomForeignKey(Usuario, verbose_name="Usuario", on_delete=models.SET_NULL, null=True, blank=False)
    total = CustomIntegerField(verbose_name="Total", null=False, blank=False)

    def __str__(self):
        return f"{self.id} - {self.fecha}"

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
    def delete(self):
        # Custom logic to manage relations before delete
        super().delete()
        
class DetalleVenta(models.Model):
    id = CustomAutoField(primary_key=True, verbose_name="ID", null=False, blank=False, editable=False)
    venta = CustomForeignKey(Venta, verbose_name="Venta", on_delete=models.CASCADE, null=False, blank=False)
    producto = CustomForeignKey(Producto, verbose_name="Producto", on_delete=models.CASCADE, null=False, blank=False)
    cantidad = CustomIntegerField(verbose_name="Cantidad", null=False, blank=False)
    precio = CustomIntegerField(verbose_name="Precio", null=False, blank=False)

    def __str__(self):
        return f"{self.id} - {self.producto}"

    class Meta:
        verbose_name = "Detalle Venta"
        verbose_name_plural = "Detalle Ventas"
    
    def delete(self):
        # Custom logic to manage relations before delete
        super().delete()