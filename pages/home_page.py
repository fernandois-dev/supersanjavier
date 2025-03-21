import flet as ft



class HomePage(ft.View):
    def __init__(self, page: ft.Page = None, _model = None, params = {}):
        super().__init__()
        self.route = "/404"
        self.controls = [
            ft.Text("404 - Pageddd Not Found", size=30),
            ft.Text("The page you're looking for doesn't exist."),
            ft.ElevatedButton("Go Home", on_click=lambda e: self.page.go("/")),
            ft.AutoComplete(
            suggestions=[
                ft.AutoCompleteSuggestion(key="one 1", value="One"),
                ft.AutoCompleteSuggestion(key="two 2", value="Two"),
                ft.AutoCompleteSuggestion(key="three 3", value="Three"),
            ],
            on_select=lambda e: print(e.control.selected_index, e.selection),
        )
        ]
