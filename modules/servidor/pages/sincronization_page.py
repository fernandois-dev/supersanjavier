from datetime import datetime
import flet as ft
import socket
import requests
from concurrent.futures import ThreadPoolExecutor

from components.custom_buttons import CustomButtonCupertino
from components.not_data_table import NotDataTable
from modules.servidor.models import VistaSincronizacion
from modules.ventas.models import Caja, Venta
from django.db import transaction



class SincronizationPage(ft.Container):
    def __init__(self, page=None, config_file="apps/servidor/server_settings.cfg"):
        super().__init__()
        self.page = page
        self.config_file = config_file
        
        self.btn_buscar = CustomButtonCupertino(
            text="Buscar",
            icon=ft.icons.SEARCH,
            on_click=self.handle_on_click_buscar,
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
        
        self.port = self.get_puerto_api()
        
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
        #se agrega un loading en medio de la pantalla
        
        self.loading = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Cargando...", size=18, font_family="Roboto", weight=ft.FontWeight.W_400),
                    ft.ProgressRing(),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            expand=True,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.SCRIM),
            border_radius=10,
            visible=False,
        )
        self.page.overlay.append(self.loading)
        
        
    def get_puerto_api(self):
        """
        Lee el puerto de la API desde el archivo de configuración server_settings.cfg.
        """
        import configparser
        config = configparser.ConfigParser()
        config.read(self.config_file)
        return int(config.get('SERVER', 'puerto_api', fallback=3555))
        
    def get_ultima_venta(self, caja_id):
        """
        Obtiene la última venta registrada en la base de datos local para una caja específica.
        """
        # Aquí deberías implementar la lógica para obtener la última venta de la base de datos local
        # Por ejemplo, podrías usar un ORM o una consulta SQL directa
        # Esto es solo un ejemplo y no funcionará sin una implementación real
        caja = Caja.objects.get(id=caja_id)
        ultima_venta = Venta.objects.filter(caja=caja).order_by('-fecha').first()
        
        if ultima_venta:
            # Aquí puedes formatear la fecha o realizar cualquier otra operación necesaria
            ultima_venta.fecha = ultima_venta.fecha.strftime("%Y-%m-%d %H:%M:%S")
        else:
            ultima_venta = None
        return ultima_venta
    
    def handle_on_click_buscar(self, e):
        # se landa el loading mientras se busca 
        self.loading.visible = True
        self.page.update()
        self.btn_buscar.disabled = True
        self.btn_buscar.update()
        self.buscar(e)
        # se quita el loading y se habilita el boton de buscar
        self.btn_buscar.disabled = False
        self.btn_buscar.update()
        self.loading.visible = False
        self.page.update()

    def buscar(self, e):
        """
        Escanea la red local en busca de puntos de venta y los lista en la tabla.
        """
        # Obtener la IP local y calcular el rango de la red
        local_ip = '192.168.1.1' #socket.gethostbyname(socket.gethostname())
        ip_base = ".".join(local_ip.split(".")[:3])  # Ejemplo: "192.168.1"

        # Lista para almacenar los puntos de venta encontrados
        puntos_de_venta = []

        def verificar_punto_de_venta(ip):
            """
            Verifica si un dispositivo en la red tiene la API de ventas disponible.
            """
            url = f"http://{ip}:{self.port}/api/fecha-ultima-venta/"
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
                
        #recorrer los resultados y buscar informacion de cada caja
        data_table = []
        for punto in puntos_de_venta:
            ip = punto["ip"]
            url = f"http://{ip}:{self.port}/api/fecha-ultima-venta/"
            try:
                response = requests.get(url, timeout=1)
                if response.status_code == 200:
                    data = response.json()
                    ultima_venta = data.get("fecha")
                    if ultima_venta:
                        ultima_venta = datetime.fromisoformat(ultima_venta)
                    caja = data.get("caja")
                    numero_caja = caja.get("nombre")
                    
                    
                    #obtiene ultima venta de esa caja registrada en la base de datos local
                    ultima_sincronizacion = self.get_ultima_venta(caja_id=caja.get("id"))
                    if ultima_sincronizacion:
                        ultima_sincronizacion =datetime.fromisoformat(ultima_sincronizacion)
                    
                    nuevo_registro = VistaSincronizacion(
                        ip=ip,
                        ultima_venta=ultima_venta,
                        numero_caja=numero_caja,
                        ultima_sincronizacion=ultima_sincronizacion,  # Inicialmente sin venta
                    )
                    
                    data_table.append(nuevo_registro)
                    
            except requests.RequestException:
                pass
        self.table.set_data(data_table)  # Actualiza la tabla con los datos obtenidos
        self.table.create_table()
        self.table.set_all_rows_selected(True)  # Selecciona todas las filas
        self.update()
    
    def sincronizar(self, e):
        # TODO Implementar la lógica de sincronización aquí
        
        #recorre los registros seleccionados y sincroniza la informacion
        for registro in self.table.get_selected_rows():
            param = ""
            if registro.ultima_sincronizacion:
                param = "?fecha_desde=" + str(registro.ultima_sincronizacion)
            
            ip = registro.ip
            url = f"http://{ip}:{self.port}/api/ventas{param}"
            try:
                response = requests.post(url, timeout=1)
                if response.status_code == 200:
                    
                    # inicia transaccion en la base de datos del orm
                    with transaction.atomic():
                        for venta in response.json():
                            self.guarda_venta(venta)
                            
            except requests.RequestException:
                pass
     
    def guarda_venta(self, venta):
        """
        Guarda la venta en la base de datos local.
        """
        # Aquí deberías implementar la lógica para guardar la venta en la base de datos local
        # Por ejemplo, podrías usar un ORM o una consulta SQL directa
        # Esto es solo un ejemplo y no funcionará sin una implementación real
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