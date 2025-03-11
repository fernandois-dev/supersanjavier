import flet as ft

class NotFoundPage(ft.View):
    def __init__(self):
        super().__init__()
        self.route = "/404"
        self.controls = [
            ft.Text("404 - Page Not Found", size=30),
            ft.Text("The page you're looking for doesn't exist."),
            ft.ElevatedButton("Go Home", on_click=lambda e: self.page.go("/"))
        ]
