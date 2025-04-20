import flet as ft

class CustomButtonCupertino(ft.CupertinoButton):
    def __init__(self, text, icon, on_click, bgcolor=ft.Colors.ON_SECONDARY, color=ft.Colors.ON_SURFACE, height = 40):
        super().__init__(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(name=icon, color=color),
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
        

class CustomIconButton(ft.TextButton):
    def __init__(self, on_click, icon=ft.Icons.random, bgcolor=ft.Colors.PRIMARY_CONTAINER, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon=icon
        self.bgcolor=bgcolor
        self.width=40
        self.height=40
        self.content=ft.Row([ft.Icon(name=self.icon, size=28)])
        self.style=ft.ButtonStyle(padding=ft.padding.all(9), bgcolor=self.bgcolor, shape=ft.RoundedRectangleBorder(radius=3))
        self.on_click=on_click