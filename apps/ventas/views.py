from pages.generic_page import GenericPage
from apps.ventas.models import Caja, Venta, DetalleVenta, ActividadCaja
import flet as ft

from pages.generic_page_form_standar import GenericPageFormStandar



def caja_list(page: ft.Page, params: dict):
    view = GenericPage(page=page, _model=Caja, params=params)
    view.build_page()
    return view
    

def caja_form(page: ft.Page, params: dict):
    view = GenericPageFormStandar(page=page, _model=Caja, params=params)
    return view

def venta_list(page: ft.Page, params: dict):
    view = GenericPage(page=page, _model=Venta, params=params)
    view.build_page()
    return view

def venta_form(page: ft.Page, params: dict):
    view = GenericPageFormStandar(page=page, _model=Venta, params=params)
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

