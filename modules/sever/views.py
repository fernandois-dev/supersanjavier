
import flet as ft

from modules.sever.pages.server_config_page import ServerConfigPage



def server_config(page: ft.Page, params: dict):
    view = ServerConfigPage(page=page)
    return view

def server_home_page(page: ft.Page, params: dict):
    return ft.Container(content=ft.Text("Aplicación del servidor."))
