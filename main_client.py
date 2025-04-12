import flet as ft
import django

from menudata import MenuData
import settings  # Cargar configuración del ORM
django.setup()

# filepath: d:\code\flet\Sistema Ventas San Javier\servidor\main.py
from utilities.style_manager import StyleManager
from apps.cliente.styles import STYLES

from modules.pos.routes import routes as pos_routes
from router.control import ControlView
        
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


ft.app(main, #view=ft.AppView.WEB_BROWSER
       )
