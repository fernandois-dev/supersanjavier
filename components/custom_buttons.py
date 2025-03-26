import flet as ft

class CustomButtonCupertino(ft.CupertinoButton):
    def __init__(self, text, icon_name, on_click, bgcolor=ft.Colors.ON_SECONDARY, color=ft.Colors.ON_SURFACE, height = 40):
        super().__init__(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(name=icon_name, color=color),
                        ft.Text(text, color=color, size=15, font_family="Roboto Mono"),
                    ],
                    tight=True,
                    ),
                    on_hover=self.on_hover
                ),
                height=height,
                bgcolor=bgcolor,
                on_click=on_click,
                padding=ft.padding.symmetric(horizontal=10, vertical=0),
            )
        self.bgcolor_original = bgcolor
        self.bgcolor = self.bgcolor_original

    def on_hover(self, e: ft.HoverEvent):
        if e.data == "true":
            self.bgcolor = ft.Colors.with_opacity(0.5, self.bgcolor_original)
        else:
            self.bgcolor = self.bgcolor_original
        self.update()

