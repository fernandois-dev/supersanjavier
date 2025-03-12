from pages.generic_page import GenericPage
from apps.comun.models import Usuario
import flet as ft

from pages.generic_page_form_standar import GenericPageFormStandar



def usuario_list(page: ft.Page, params: dict):
    view = GenericPage(page=page, _model=Usuario, params=params)
    view.build_page()
    return view
    

def usuario_form(page: ft.Page, params: dict):
    view = GenericPageFormStandar(page=page, _model=Usuario, params=params)
    return view
