# import requests
# import configparser
# from django.db import transaction
# from django.db import models
# from django.core.validators import MinLengthValidator
# from .custom_fields import CustomCharField, CustomEmailField, CustomDateTimeField, CustomAutoField, CustomIntegerField, CustomBooleanField, CustomForeignKey



# class Producto(models.Model):
#     id = CustomAutoField(primary_key=True, verbose_name="ID", null=False, blank=False, editable=False)
#     codigo = CustomCharField(max_length=10, verbose_name="Código", null=False, blank=False, validators=[MinLengthValidator(3)])
#     nombre = CustomCharField(max_length=100, verbose_name="Nombre", null=False, blank=False)
#     descripcion = CustomCharField(max_length=200, verbose_name="Descripción", null=True, blank=True)
#     precio_compra = CustomIntegerField(verbose_name="Precio Compra", null=False, blank=False)
#     precio_venta = CustomIntegerField(verbose_name="Precio Venta", null=False, blank=False)
#     stock = CustomIntegerField(verbose_name="Stock", null=False, blank=False)
#     categoria = CustomForeignKey('Categoria', verbose_name="Categoría", on_delete=models.SET_NULL, null=True, blank=True)
#     activo = CustomBooleanField(verbose_name="Activo", null=False, blank=False, default=True)
    
#     def __str__(self):
#         return f"{self.codigo} - {self.nombre}"
    
#     class Meta:
#         verbose_name = "Producto"
#         verbose_name_plural = "Productos"
    
#     def delete(self):
#         # Custom logic to manage relations before delete
#         super().delete()


# class Categoria(models.Model):
#     id = CustomAutoField(primary_key=True, verbose_name="ID", null=False, blank=False, editable=False)
#     nombre = CustomCharField(max_length=100, verbose_name="Nombre", null=False, blank=False)
#     descripcion = CustomCharField(max_length=200, verbose_name="Descripción", null=True, blank=True)
#     activo = CustomBooleanField(verbose_name="Activo", null=False, blank=False, default=True)
#     porcentaje_iva = CustomIntegerField(verbose_name="Porcentaje IVA", default="19", null=False, blank=False)
    
    
#     def __str__(self):
#         return self.nombre

#     class Meta:
#         verbose_name = "Categoría"
#         verbose_name_plural = "Categorías"
        
#     def delete(self):
#         # Custom logic to manage relations before delete
#         super().delete()

# class Usuario(models.Model):
#     id = CustomAutoField(primary_key=True, verbose_name="ID", null=False, blank=False, editable=False)
#     nombre = CustomCharField(max_length=100, verbose_name="Nombre", null=False, blank=False)
#     email = CustomEmailField(verbose_name="Email", unique=True, null=False, blank=False)
#     activo = CustomBooleanField(verbose_name="Activo", null=False, blank=False, default=True)

#     def __str__(self):
#         return self.nombre
    
#     class Meta:
#         verbose_name = "Usuario"
#         verbose_name_plural = "Usuarios"

#     def delete(self):
#         # Custom logic to manage relations before delete
#         super().delete()

# class Caja(models.Model):
#     id = CustomAutoField(primary_key=True, verbose_name="ID", null=False, blank=False, editable=False)
#     nombre = CustomCharField(max_length=100, verbose_name="Nombre", null=False, blank=False)
#     fecha_apertura = CustomDateTimeField(verbose_name="Fecha Apertura", null=False, blank=False)
#     fecha_cierre = CustomDateTimeField(verbose_name="Fecha Cierre", null=True, blank=True)
#     usuario_apertura = CustomForeignKey(Usuario, verbose_name="Usuario Apertura", on_delete=models.SET_NULL, null=True, blank=False, related_name="usuario_apertura")
#     usuario_cierre = CustomForeignKey(Usuario, verbose_name="Usuario Cierre", on_delete=models.SET_NULL, null=True, blank=True, related_name="usuario_cierre")
#     monto_apertura = CustomIntegerField(verbose_name="Monto Apertura", null=False, blank=False)
#     monto_cierre = CustomIntegerField(verbose_name="Monto Cierre", null=True, blank=True)
#     activo = CustomBooleanField(verbose_name="Activo", null=False, blank=False, default=True)

#     def __str__(self):
#         return f"{self.nombre} - {self.fecha_apertura}"

#     class Meta:
#         verbose_name = "Caja"
#         verbose_name_plural = "Cajas"
    
#     def delete(self):
#         # Custom logic to manage relations before delete
#         super().delete()
    
# class ActividadCaja(models.Model):
#     id = CustomAutoField(primary_key=True, verbose_name="ID", null=False, blank=False, editable=False)
#     caja = CustomForeignKey(Caja, verbose_name="Caja", on_delete=models.CASCADE, null=False, blank=False)
#     fecha = CustomDateTimeField(verbose_name="Fecha", null=False, blank=False)
#     monto = CustomIntegerField(verbose_name="Monto", null=False, blank=False)
#     descripcion = CustomCharField(max_length=200, verbose_name="Descripción", null=True, blank=True)

#     def __str__(self):
#         return f"{self.caja} - {self.fecha}"

#     class Meta:
#         verbose_name = "Actividad Caja"
#         verbose_name_plural = "Actividad Cajas"
        
#     def delete(self):
#         # Custom logic to manage relations before delete
#         super().delete()

# class Venta(models.Model):
#     id = CustomAutoField(primary_key=True, verbose_name="ID", null=False, blank=False, editable=False)
#     fecha = CustomDateTimeField(verbose_name="Fecha", null=False, blank=False)
#     caja = CustomForeignKey(Caja, verbose_name="Caja", on_delete=models.CASCADE, null=False, blank=False)
#     usuario = CustomForeignKey(Usuario, verbose_name="Usuario", on_delete=models.SET_NULL, null=True, blank=False)
#     total = CustomIntegerField(verbose_name="Total", null=False, blank=False)

#     def __str__(self):
#         return f"{self.id} - {self.fecha}"

#     class Meta:
#         verbose_name = "Venta"
#         verbose_name_plural = "Ventas"
#     def delete(self):
#         # Custom logic to manage relations before delete
#         super().delete()
        
# class DetalleVenta(models.Model):
#     id = CustomAutoField(primary_key=True, verbose_name="ID", null=False, blank=False, editable=False)
#     venta = CustomForeignKey(Venta, verbose_name="Venta", on_delete=models.CASCADE, null=False, blank=False)
#     producto = CustomForeignKey(Producto, verbose_name="Producto", on_delete=models.CASCADE, null=False, blank=False)
#     cantidad = CustomIntegerField(verbose_name="Cantidad", null=False, blank=False)
#     precio = CustomIntegerField(verbose_name="Precio", null=False, blank=False)

#     def __str__(self):
#         return f"{self.id} - {self.producto}"

#     class Meta:
#         verbose_name = "Detalle Venta"
#         verbose_name_plural = "Detalle Ventas"
    
#     def delete(self):
#         # Custom logic to manage relations before delete
#         super().delete()

# Function to synchronize products from the API
# def sync_products():
#     # Read server configuration from pos_settings.cfg
#     config = configparser.ConfigParser()
#     config.read('d:/code/flet/Sistema Ventas San Javier/servidor/apps/cliente/pos_settings.cfg')

#     ip_servidor = config.get('POS', 'ip_servidor')
#     port_servidor = config.get('POS', 'port_servidor')
#     api_url = f"http://{ip_servidor}:{port_servidor}/api/productos"

#     try:
#         # Fetch product data from the API
#         response = requests.get(api_url)
#         response.raise_for_status()
#         products = response.json()

#         # Insert products into the database
#         with transaction.atomic():
#             # Delete all existing products before synchronization
#             Producto.objects.all().delete()
#             for product in products:
#                 Producto.objects.update_or_create(
#                     codigo=product['codigo'],
#                     defaults={
#                         'nombre': product['nombre'],
#                         'descripcion': product.get('descripcion', ''),
#                         'precio_compra': product['precio_compra'],
#                         'precio_venta': product['precio_venta'],
#                         'stock': product['stock'],
#                         'activo': product.get('activo', True),
#                     }
#                 )
#         print("Products synchronized successfully.")
#     except requests.RequestException as e:
#         print(f"Error fetching products from API: {e}")
#     except Exception as e:
#         print(f"Error inserting products into the database: {e}")
