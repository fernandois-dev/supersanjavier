import flet as ft

from components.left_navigation_menu import LeftNavigationMenu
from menudata import MenuData
from pages.generic_page import GenericPage
from pages.not_found_page import NotFoundPage
from router.router import Router #new import




menudata = MenuData()

class ControlView(ft.Row):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.menudata = menudata
        self.left_nav = LeftNavigationMenu(menudata, page)
        self.control_page = ControlPages(page = self.page)
        self.expand = True
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            self.left_nav,
            ft.VerticalDivider(width=1),
            self.control_page,
        ]

    def display(self, params):
        self.control_page.display(params)
        self.page.update()

    def update_menu_selection(self, route):
        self.left_nav.update_selected_index(route)
    
    def update_selected_item(self):
        self.left_nav.update_selected_item()
        

class ControlPages(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.expand = 1
        self.controls = []
        self.page = page
        self.router = Router(self.page)  # Instantiate the Router
        self.scroll = ft.ScrollMode.AUTO

    def display(self, params):
        # ask the router for the page
        page_to_render = self.router.get_page(self.page.route, params)
        if page_to_render is not None:
            self.controls = [page_to_render]
            self.update()
        else:
            self.controls = [ft.Text("Page not found")]
            self.update()