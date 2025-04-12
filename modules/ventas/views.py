from components.custom_input import SearchField
from pages.generic_page import GenericPage
from modules.ventas.models import Caja, Venta, DetalleVenta, ActividadCaja
import flet as ft

from pages.generic_page_form_standard import GenericPageFormStandar
from pages.generic_header_detail_form import GenericHeaderDetailForm
from pages.conditions import Conditions
from utilities.utilities import num_or_zero




def caja_list(page: ft.Page, params: dict):
    view = GenericPage(page=page, _model=Caja, params=params)
    view.build_page()
    return view

def caja_form(page: ft.Page, params: dict):
    view = GenericPageFormStandar(page=page, _model=Caja, params=params)
    return view

def venta_list(page: ft.Page, params: dict):
    conditions = Conditions(
        fields_excluded=["state"],
    )
    view = GenericPage(page=page, _model=Venta, params=params, conditions=conditions)
    view.build_page()
    return view

def venta_form(page: ft.Page, params: dict):
    conditions = Conditions(
        # overrides_input_type={
        #         "usuario": SearchField
        #     },
        fields_excluded=["state"],
        related_objects={"detalleventa_set": {
            'fields_excluded': ["id","venta"],
            'fields_order':["cantidad", "producto", "precio","descuento", "total"],
            'fields_calculations':{
                "precio": { 
                    "depends": ["producto"], 
                    "calculation": lambda obj: obj.producto.precio_venta if obj.producto_id else 0},
                "total": { 
                    "depends": ["cantidad", "precio", "descuento"], 
                    "calculation": lambda obj: num_or_zero(obj.cantidad) * ((num_or_zero(obj.precio)-num_or_zero(obj.descuento)))},
                "__parent__total": {
                    "depends": ["total"],  # Depende de los hijos
                    "calculation": lambda parent, children: sum(child.total for child in children if child.total)
                }
            },
            'overrides_input_type':{
                "producto": SearchField
            },
            'fields_expand':{"cantidad":2, "producto":4, "precio":3, "descuento":3,"total":3}
        }}
    )
    view = GenericHeaderDetailForm(page=page, _model=Venta, params=params, conditions=conditions)
    return view

def caja_actividad_list(page: ft.Page, params: dict):
    view = GenericPage(page=page, _model=ActividadCaja, params=params)
    view.build_page()
    return view

def caja_actividad_form(page: ft.Page, params: dict):
    view = GenericPageFormStandar(page=page, _model=ActividadCaja, params=params)
    return view

def detalle_venta_list(page: ft.Page, params: dict):
    view = GenericPage(page=page, _model=DetalleVenta, params=params)
    view.build_page()
    return view

def detalle_venta_form(page: ft.Page, params: dict):
    view = GenericPageFormStandar(page=page, _model=DetalleVenta, params=params)
    return view

