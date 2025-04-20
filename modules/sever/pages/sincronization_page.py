import flet as ft

from components.custom_buttons import CustomButtonCupertino

class SincronizationPage(ft.Container):
    def __init__(self, page=None, config_file="apps/servidor/server_settings.cfg"):
        super().__init__()
        self.page = page
        
        self.btn_buscar = CustomButtonCupertino(
            text="Buscar",
            icon=ft.icons.SEARCH,
            tooltip="Buscar",
            on_click=self.buscar,
        )
        self.btn_sincronizar = CustomButtonCupertino(
            text="Sincronizar",
            icon=ft.icons.SYNC,
            tooltip="Sincronizar",
            on_click=self.sincronizar,
        )
        
        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("Sincronización"),
                    alignment=ft.alignment.center,
                    padding=10,
                ),
                ft.Row(
                    controls=[
                        self.btn_buscar,
                        self.btn_sincronizar,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Text("tabla"),     
            ]
        )
    
    def buscar(self, e):
        # TODO Implementar la lógica de búsqueda aquí
        pass
    
    def sincronizar(self, e):
        # TODO Implementar la lógica de sincronización aquí
        pass