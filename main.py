import flet as ft
import django

import data.db  # Cargar configuración del ORM
django.setup()

from router.control import ControlView
        
            
def main(page: ft.Page):
    
    page.title = "Sistema de Gestion de Inventario"
    page.params = {}
    page.custom_go = lambda route, params=None: custom_go(route, params)

    page.fonts = {
        "Roboto Mono": "RobotoMono-VariableFont_wght.ttf",
        "Roboto Slab": "RobotoSlab[wght].ttf",
        
    }
    
    control_view = ControlView(page = page)
    
    
    def custom_go(route, params=None):
        page.params = params
        page.go(route)
    

    def route_change(e):
        control_view.display(params = page.params)
        page.update()
        control_view.update_menu_selection(page.route)
        control_view.update_selected_item()
        page.params = {}
        page.update()
    

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

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
        
    page.theme_mode = ft.ThemeMode.LIGHT
    page.on_error = lambda e: print("Page error:", e.data)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    page.add(control_view) 


ft.app(main, #view=ft.AppView.WEB_BROWSER
       )
