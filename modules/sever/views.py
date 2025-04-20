
import flet as ft

from modules.sever.pages.server_config_page import ServerConfigPage
from modules.sever.pages.sincronization_page import SincronizationPage



def server_config(page: ft.Page, params: dict):
    view = ServerConfigPage(page=page)
    return view

def server_home_page(page: ft.Page, params: dict):
    return ft.Container(content=ft.Text("Aplicación del servidor."))

def server_sync_page(page: ft.Page, params: dict):
    view = SincronizationPage(page=page)
    return view
