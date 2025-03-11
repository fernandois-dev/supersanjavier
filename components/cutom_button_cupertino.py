import flet as ft

class CustomButtonCupertino(ft.CupertinoButton):
    def __init__(self, text, icon_name, on_click, bgcolor=ft.Colors.ON_SECONDARY, color=ft.Colors.ON_SURFACE, height = 40):
        super().__init__(
            content=ft.Row(
                [
                    ft.Icon(name=icon_name, color=color),
                    ft.Text(text, color=color, size=15, font_family="Roboto Mono"),
                ],
                tight=True,
            ),
            height=height,
            bgcolor=bgcolor,
            on_click=on_click,
        )
