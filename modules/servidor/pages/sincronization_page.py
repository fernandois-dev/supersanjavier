import flet as ft
import socket
import requests
from concurrent.futures import ThreadPoolExecutor

from components.custom_buttons import CustomButtonCupertino
from components.not_data_table import NotDataTable
from modules.servidor.models import VistaSincronizacion

class SincronizationPage(ft.Container):
    def __init__(self, page=None, config_file="apps/servidor/server_settings.cfg"):
        super().__init__()
        self.page = page
        
        self.btn_buscar = CustomButtonCupertino(
            text="Buscar",
            icon=ft.icons.SEARCH,
            on_click=self.buscar,
            bgcolor=ft.Colors.SECONDARY,
            color=ft.Colors.ON_SECONDARY,
        )
        self.btn_sincronizar = CustomButtonCupertino(
            text="Sincronizar",
            icon=ft.icons.SYNC,
            on_click=self.sincronizar,
            bgcolor=ft.Colors.PRIMARY,
            color=ft.Colors.ON_PRIMARY,
        )
        
        self._model = VistaSincronizacion()  # Aquí deberías inicializar tu modelo de datos
        
        self.table: NotDataTable = self._create_table()
        self.table.set_model(self._model)
        self.table.set_data([])
        self.table.create_table()
        
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        self.btn_buscar,
                        self.btn_sincronizar,
                        ft.Text("Sincronizar" , size=18, font_family="Roboto", weight=ft.FontWeight.W_400)
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                self.table,     
            ]
        )
    
    def buscar(self, e):
        """
        Escanea la red local en busca de puntos de venta y los lista en la tabla.
        """
        # Obtener la IP local y calcular el rango de la red
        local_ip = socket.gethostbyname(socket.gethostname())
        ip_base = ".".join(local_ip.split(".")[:3])  # Ejemplo: "192.168.1"
        puerto_api = 3555  # Cambia esto al puerto donde se publica la API de los puntos de venta

        # Lista para almacenar los puntos de venta encontrados
        puntos_de_venta = []

        def verificar_punto_de_venta(ip):
            """
            Verifica si un dispositivo en la red tiene la API de ventas disponible.
            """
            url = f"http://{ip}:{puerto_api}/api/ventas/"
            try:
                response = requests.get(url, timeout=1)
                if response.status_code == 200:
                    return {"ip": ip, "estado": "Disponible"}
            except requests.RequestException:
                pass
            return None

        # Escanear la red en paralelo
        with ThreadPoolExecutor(max_workers=50) as executor:
            ips = [f"{ip_base}.{i}" for i in range(1, 255)]
            resultados = executor.map(verificar_punto_de_venta, ips)

        # Filtrar los resultados válidos
        for resultado in resultados:
            if resultado:
                puntos_de_venta.append(resultado)
    
    def sincronizar(self, e):
        # TODO Implementar la lógica de sincronización aquí
        pass
    
    def _create_table(self) -> NotDataTable:
        """
        Crea y configura la tabla principal.

        Returns:
            NotDataTable: Tabla configurada.
        """
        return NotDataTable(
            handle_on_long_press=None,
            on_row_selected=None,
            on_click_column=None,
            conditions=None,
        )