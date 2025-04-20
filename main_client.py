import configparser
import os
import flet as ft
import django
import apps.cliente.settings# Cargar configuración del ORM
django.setup()

# filepath: d:\code\flet\Sistema Ventas San Javier\servidor\main.py
from modules.ventas.models import Caja
from utilities.style_manager import StyleManager
from apps.cliente.styles import STYLES

# Import para el servidor FastAPI
from apps.cliente.fast_api import start_fastapi, fastapi_app
import threading

from modules.pos.routes import routes as pos_routes
from router.control import ControlView
from modules.pos.uilities import get_api_cajas_url, get_api_categorias_url, get_api_productos_url, sync_cajas, sync_categories, sync_products

import configparser

# Read the port from server_settings.cfg
config = configparser.ConfigParser()
config.read('apps/cliente/pos_settings.cfg')
FASTAPI_PORT = int(config.get('POS-API', 'api_port', fallback=8000))

      
def load_cash_register_from_config():
    """
    Load the cash register configuration from the settings file.

    Returns:
        dict: A dictionary containing the cash register configuration.
    """
    config_path = os.path.join(
        os.path.dirname(__file__), 
        'apps/cliente/pos_settings.cfg'
    )
    config_path = os.path.abspath(config_path)
    
    config = configparser.ConfigParser()
    config.read(config_path)

    caja_config = {
        'numero_caja': config.get('POS', 'numero_caja'),
    }
    
    return caja_config
        
def custom_go(page: ft.Page, route: str, params: dict = None) -> None:
    """
    Custom navigation function to handle route changes with parameters.

    Args:
        page (ft.Page): The Flet page instance.
        route (str): The route to navigate to.
        params (dict, optional): Parameters to pass to the route. Defaults to None.
    """
    page.params = params or {}
    page.go(route)

def route_change(page: ft.Page, control_view: ControlView, e: ft.ControlEvent) -> None:
    """
    Handles route changes and updates the control view.

    Args:
        page (ft.Page): The Flet page instance.
        control_view (ControlView): The main control view instance.
        e (ft.ControlEvent): The route change event.
    """
    control_view.display(params=page.params)
    page.update()
    # control_view.update_menu_selection(page.route)
    # control_view.update_selected_item()
    page.params = {}
    page.update()
    
def view_pop(page: ft.Page) -> None:
    """
    Handles the back navigation (view pop) in the app.

    Args:
        page (ft.Page): The Flet page instance.
    """
    page.views.pop()
    top_view = page.views[-1]
    page.go(top_view.route)
     
def main(page: ft.Page):
    """
    Main entry point for the Flet application.

    Args:
        page (ft.Page): The Flet page instance.
    """
    # Page configuration
    
    # Configurar estilos globales
    StyleManager.configure(STYLES)

    page.padding = ft.padding.only(left=10, top=10, right=10, bottom=0)
    page.title = "Inventory Management System"
    page.params = {}
    page.custom_go = lambda route, params=None: custom_go(page, route, params)
    page.fonts = {
        "Roboto Mono": "RobotoMono-VariableFont_wght.ttf",
        "Roboto Slab": "RobotoSlab[wght].ttf",
    }
    page.theme_mode = ft.ThemeMode.LIGHT
    page.on_error = lambda e: print("Page error:", e.data)
    
    
    
    # Initialize the main control view
    # menudata = MenuData()
    modules = pos_routes
    control_view = ControlView(page=page, modules=modules, menudata=None)
    
    # se sincronizan las categorias desde el servidor
    api_categorias_url = get_api_categorias_url()
    sync_categories(api_url=api_categorias_url)  # Synchronize categories from the server
    
    # se actualizan los productos desde el servidor
    api_productos_url = get_api_productos_url()
    sync_products(api_url=api_productos_url)
    
    # se sincronizan las cajas desde el servidor
    api_cajas_url = get_api_cajas_url()
    sync_cajas(api_url=api_cajas_url)  # Synchronize cash registers from the server
    
    # se establece el objeto caja leyendolo desde pos_settings.cfg y se deja como variable en page
    numero_caja = load_cash_register_from_config()
    page.caja = Caja.objects.filter(numero=numero_caja['numero_caja']).first()
    
    # AppBar configuration
    page.appbar = ft.AppBar(
        leading=ft.Container(padding=5, content=ft.Image(src=f"logo.svg")),
        leading_width=40,
        title=ft.Text("Inventario"),
        center_title=True,
        bgcolor=ft.Colors.INVERSE_PRIMARY,
        actions=[
            ft.Container(
                padding=16, content=ft.Text(f"Flet version: {ft.version.version}, {page.route}")
            )
        ],
    )

    # Event handlers
    page.on_route_change = lambda e: route_change(page, control_view, e)
    page.on_view_pop = lambda: view_pop(page)

    # Navigate to the initial route
    page.go(page.route)

    # Add the main control view to the page
    page.add(control_view)
    
    # Iniciar FastAPI en un hilo separado
    threading.Thread(target=start_fastapi, args=(fastapi_app, FASTAPI_PORT), daemon=True).start()



ft.app(main, #view=ft.AppView.WEB_BROWSER
       )
