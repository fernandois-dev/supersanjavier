# in a new file, e.g., router.py
import flet as ft
from utilities.template_routes import TemplateRoute
from pages.not_found_page import NotFoundPage
from pages.home_page import HomePage





class Router:
    def __init__(self, page: ft.Page, modules = [] ):
        self.page = page
        # main_pages = {"/": lambda page, model: HomePage(page, model),}
        # self.routes = main_pages | inventario_routes | ventas_routes | comun_routes
        self.routes = modules
        

    def get_page(self, route: str, params: dict = {}) -> ft.Control | None:
        troute = TemplateRoute(route, params=params)
        
        for pattern, factory in self.routes.items():
            if troute.match(pattern):
                return factory(self.page, troute.params)
                # try:
                #     return factory(self.page, troute.params)
                # except Exception as e:
                #     # Log the error, maybe display a generic error page
                #     print(f"Error instantiating page for route {route}: {e}")
                #     # return ErrorPage()
                #     return None

        return NotFoundPage() 
