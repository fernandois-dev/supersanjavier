from .views import caja_actividad_form, caja_actividad_list, caja_form, detalle_venta_form, detalle_venta_list, caja_list
from .views import venta_list, venta_form

routes = {
    "/cajas/listado": caja_list,
    "/cajas/listado/form": caja_form,
    "/cajas/actividad": caja_actividad_list,
    "/cajas/actividad/form": caja_actividad_form,
    "/ventas/detalle": detalle_venta_list,
    "/ventas/detalle/form": detalle_venta_form,
    "/ventas/listado": venta_list,
    "/ventas/listado/form": venta_form,
}
