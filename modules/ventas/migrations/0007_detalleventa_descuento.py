# Generated by Django 5.1.7 on 2025-04-04 09:38

import data.custom_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ventas", "0006_alter_detalleventa_producto_alter_venta_caja_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="detalleventa",
            name="descuento",
            field=data.custom_fields.CustomMoneyField(
                default=0, verbose_name="Descuento"
            ),
        ),
    ]
