from django.db import transaction


def save_venta(venta_data):
    """
    Guarda una venta y su detalle en la base de datos.

    Args:
        venta_data (dict): Diccionario con los datos de la venta, incluyendo el detalle de la venta.
    """
    from modules.ventas.models import Venta, DetalleVenta

    with transaction.atomic():
        # Guardar o actualizar la venta
        for obj in venta_data:
            venta, created = Venta.objects.update_or_create(
                id=None,
                defaults={
                    'caja_id': obj['caja'],
                    'fecha': obj['fecha'],
                    'total': obj['total'],
                    'state': obj['state'],
                    'usuario': obj['usuario'],
                }
            )

            # Eliminar detalles existentes de la venta si ya existían
            if not created:
                DetalleVenta.objects.filter(venta=venta).delete()

            # Guardar los detalles de la venta
            for detalle in obj['detalle_venta']:
                DetalleVenta.objects.create(
                    venta=venta,
                    producto_id=detalle['producto'],
                    cantidad=detalle['cantidad'],
                    precio=detalle['precio'],
                    descuento=detalle['descuento'],
                    total=detalle['total'],
                )