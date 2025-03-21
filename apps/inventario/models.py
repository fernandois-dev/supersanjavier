
from django.db import models
from django.core.validators import MinLengthValidator
from data.custom_fields import CustomAutoField, CustomBooleanField, CustomCharField, CustomForeignKey, CustomIntegerField, CustomMoneyField


class Producto(models.Model):
    id = CustomAutoField(primary_key=True, verbose_name="ID", null=False, blank=False, editable=False)
    codigo = CustomCharField(max_length=10, verbose_name="Código", null=False, blank=False, validators=[MinLengthValidator(3)])
    nombre = CustomCharField(max_length=100, verbose_name="Nombre", null=False, blank=False)
    descripcion = CustomCharField(max_length=200, verbose_name="Descripción", null=True, blank=True)
    precio_compra = CustomMoneyField(verbose_name="Precio Compra", null=False, blank=False)
    precio_venta = CustomMoneyField(verbose_name="Precio Venta", null=False, blank=False)
    stock = CustomIntegerField(verbose_name="Stock", null=False, blank=False)
    categoria = CustomForeignKey('Categoria', verbose_name="Categoría", on_delete=models.SET_NULL, null=True, blank=True)
    activo = CustomBooleanField(verbose_name="Activo", null=False, blank=False, default=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
    
    def delete(self):
        # Custom logic to manage relations before delete
        super().delete()


class Categoria(models.Model):
    id = CustomAutoField(primary_key=True, verbose_name="ID", null=False, blank=False, editable=False)
    nombre = CustomCharField(max_length=100, verbose_name="Nombre", null=False, blank=False)
    descripcion = CustomCharField(max_length=200, verbose_name="Descripción", null=True, blank=True)
    activo = CustomBooleanField(verbose_name="Activo", null=False, blank=False, default=True)
    porcentaje_iva = CustomIntegerField(verbose_name="Porcentaje IVA", default="19", null=False, blank=False)
    
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        
    def delete(self):
        # Custom logic to manage relations before delete
        super().delete()