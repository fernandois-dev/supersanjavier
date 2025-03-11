# in a new file, e.g., router.py
import flet as ft
from pages.generic_page import GenericPage
from pages.generic_page_form_standar import GenericPageFormStandar
from data.models import Producto, Categoria, Usuario, Caja, ActividadCaja, Venta, DetalleVenta
from utilities.template_routes import TemplateRoute
from typing import Callable
from pages.not_found_page import NotFoundPage



class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.routes = {
            "/productos": lambda params: GenericPage(page=self.page, _model=Producto, params=params),
            "/productos/form": lambda params: GenericPageFormStandar(page=self.page, _model=Producto, params=params),
            "/categorias": lambda params: GenericPage(page=self.page, _model=Categoria, params=params),
            "/categorias/form": lambda params: GenericPageFormStandar(page=self.page, _model=Categoria, params=params),
            "/usuarios": lambda params: GenericPage(page=self.page, _model=Usuario, params=params),
            "/usuarios/form": lambda params: GenericPageFormStandar(page=self.page, _model=Usuario, params=params),
            "/cajas/listado": lambda params: GenericPage(page=self.page, _model=Caja, params=params),
            "/cajas/listado/form": lambda params: GenericPageFormStandar(page=self.page, _model=Caja, params=params),
            "/cajas/actividad": lambda params: GenericPage(page=self.page, _model=ActividadCaja, params=params),
            "/cajas/actividad/form": lambda params: GenericPageFormStandar(page=self.page, _model=ActividadCaja, params=params),
            "/ventas/detalle": lambda params: GenericPage(page=self.page, _model=Venta, params=params),
            "/ventas/detalle/form": lambda params: GenericPageFormStandar(page=self.page, _model=Venta, params=params),
            "/ventas/listado": lambda params: GenericPage(page=self.page, _model=DetalleVenta, params=params),
            "/ventas/listado/form": lambda params: GenericPageFormStandar(page=self.page, _model=DetalleVenta, params=params),
        }

    def get_page(self, route: str, params: dict = {}) -> ft.Control | None:
        troute = TemplateRoute(route, params=params)
        
        for pattern, factory in self.routes.items():
            if troute.match(pattern):
                try:
                    return factory(troute.params)
                except Exception as e:
                    # Log the error, maybe display a generic error page
                    print(f"Error instantiating page for route {route}: {e}")
                    # return ErrorPage()
                    return None

        return NotFoundPage() 
