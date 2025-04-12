
from django.db import models
from django.core.validators import MinLengthValidator
from data.custom_fields import CustomAutoField, CustomBooleanField, CustomCharField, CustomForeignKey, CustomIntegerField, CustomMoneyField


class Producto(models.Model):
    id = CustomAutoField(primary_key=True, verbose_name="ID", null=False, blank=False, editable=False)
    codigo = CustomCharField(max_length=10, verbose_name="Código", null=True, blank=True, validators=[MinLengthValidator(3)], is_searchable=True)
    nombre = CustomCharField(max_length=100, verbose_name="Nombre", null=False, blank=False, is_sortable=True, is_searchable=True)
    codigo_barras = CustomCharField(max_length=20, verbose_name="Código de Barras", null=True, blank=True, is_sortable=True, is_searchable=True)
    precio_compra = CustomMoneyField(verbose_name="Precio Compra", null=True, blank=True)
    precio_venta = CustomMoneyField(verbose_name="Precio Venta", null=False, blank=False)
    stock = CustomIntegerField(verbose_name="Stock", null=True, blank=True, default=0)
    categoria = CustomForeignKey('Categoria', verbose_name="Categoría", on_delete=models.SET_NULL, null=True, blank=True)
    activo = CustomBooleanField(verbose_name="Activo", null=True, blank=True, default=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["-id"]
    
    def delete(self):
        # Custom logic to manage relations before delete
        super().delete()


class Categoria(models.Model):
    id = CustomAutoField(primary_key=True, verbose_name="ID", null=False, blank=False, editable=False)
    nombre = CustomCharField(max_length=100, verbose_name="Nombre", null=False, blank=False)
    descripcion = CustomCharField(max_length=200, verbose_name="Descripción", null=True, blank=True)
    porcentaje_iva = CustomIntegerField(verbose_name="Porcentaje IVA", default="19", null=False, blank=False)
    activo = CustomBooleanField(verbose_name="Activo", null=False, blank=False, default=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["-id"]
        
    def delete(self):
        # Custom logic to manage relations before delete
        super().delete()