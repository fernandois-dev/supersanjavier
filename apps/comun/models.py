from django.db import models
from data.custom_fields import CustomCharField, CustomEmailField, CustomDateTimeField, CustomAutoField, CustomIntegerField, CustomBooleanField, CustomForeignKey



class Usuario(models.Model):
    id = CustomAutoField(primary_key=True, verbose_name="ID", null=False, blank=False, editable=False)
    nombre = CustomCharField(max_length=100, verbose_name="Nombre", null=False, blank=False)
    email = CustomEmailField(verbose_name="Email", unique=True, null=False, blank=False)
    activo = CustomBooleanField(verbose_name="Activo", null=False, blank=False, default=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ["nombre"]

    def delete(self):
        # Custom logic to manage relations before delete
        super().delete()
