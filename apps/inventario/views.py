from pages.generic_page import GenericPage
from apps.inventario.models import Producto, Categoria
import flet as ft

from pages.generic_page_form_standar import GenericPageFormStandar



def producto_list(page: ft.Page, params: dict):
    view = GenericPage(page=page, _model=Producto, params=params)
    view.build_page()
    return view
    

def producto_form(page: ft.Page, params: dict):
    view = GenericPageFormStandar(page=page, _model=Producto, params=params)
    return view

def categoria_list(page: ft.Page, params: dict):
    view = GenericPage(page=page, _model=Categoria, params=params)
    view.build_page()
    return view

def categoria_form(page: ft.Page, params: dict):
    view = GenericPageFormStandar(page=page, _model=Categoria, params=params)
    return view

