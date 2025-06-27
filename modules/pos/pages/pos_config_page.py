import flet as ft
import configparser
import os

from components.custom_buttons import CustomButtonCupertino
from modules.pos.uilities import get_api_cajas_url, get_api_categorias_url, get_api_productos_url, sync_cajas, sync_categories, sync_products


# from components.custom_input import CustomToast


class POSConfigPage(ft.Container):
    def __init__(self, page=None, config_file=None):
        super().__init__()
        self.page = page
        self.config_path = os.path.abspath(os.path.join(os.getcwd(), "apps/cliente/pos_settings.cfg")) if config_file is None else config_file
        self.config = configparser.ConfigParser()
        self.page.on_keyboard_event = self.handle_keypress

        self.btn_sync = CustomButtonCupertino(
            text="Sincronizar",
            icon=ft.icons.SYNC,
            on_click=lambda e: self.sync(),
            color=ft.Colors.ON_PRIMARY,
            bgcolor=ft.Colors.PRIMARY,
        )

        # Cargar configuración existente o crear una nueva
        if os.path.exists(self.config_path):
            self.load_config()
        else:
            self.create_default_config()

        # Campos de configuración
        self.txt_numero_caja = ft.TextField(
            label="Número de Caja",
            value=self.config.get("POS", "numero_caja"),
            width=300,
        )
        self.txt_usuario_caja = ft.TextField(
            label="Usuario de Caja",
            value=self.config.get("POS", "usuario_caja"),
            width=300,
        )
        self.txt_ip_servidor = ft.TextField(
            label="IP del Servidor",
            value=self.config.get("POS-SERVIDOR", "ip_servidor"),
            width=300,
        )
        self.port_servidor = ft.TextField(
            label="PORT",
            value=self.config.get("POS-SERVIDOR", "port_servidor"),
            width=300,
        )
        self.chk_carga_productos = ft.Checkbox(
            label="Cargar Productos al iniciar",
            value=self.config.getboolean("POS", "carga_productos"),
        )
        
        # Botones
        self.btn_guardar = CustomButtonCupertino(
            text="Guardar Configuración",
            icon=ft.icons.SAVE,
            on_click=self.save_config,
            color=ft.Colors.ON_PRIMARY,
            bgcolor=ft.Colors.PRIMARY,
        )

        # Layout de la ventana
        self.content = ft.Column(
            controls=[
                ft.Text("Configuración del Punto de Venta", size=20, weight=ft.FontWeight.BOLD),
                ft.Column(
                    controls=[
                        self.txt_numero_caja,
                        self.txt_usuario_caja,
                        self.txt_ip_servidor,
                        self.port_servidor,
                        self.chk_carga_productos
                    ]
                ),
                ft.Row(
                    controls=[self.btn_guardar, self.btn_sync],
                    alignment=ft.MainAxisAlignment.START,
                ),
            ],
            spacing=20,
            width=400,
        )

    def handle_keypress(self, e: ft.KeyboardEvent):
        """
        Handles keypress events to toggle between field layouts.
        """
        
        if e.key == "F8":
            # go to config page
            self.page.go("/")
        
    def sync(self):
        # se sincronizan las categorias desde el servidor
        api_categorias_url = get_api_categorias_url(self.config_path)
        response = sync_categories(api_url=api_categorias_url)  # Synchronize categories from the server

        if response[0] == 1:
            self.page.open(ft.SnackBar(ft.Text(response[1])))
        else:
            self.page.open(ft.SnackBar(ft.Text(response[1]), bgcolor=ft.Colors.RED_800))

        # se actualizan los productos desde el servidor
        api_productos_url = get_api_productos_url(self.config_path)
        response = sync_products(api_url=api_productos_url)

        if response[0] == 1:
            self.page.open(ft.SnackBar(ft.Text(response[1])))
        else:
            self.page.open(ft.SnackBar(ft.Text(response[1]), bgcolor=ft.Colors.RED_800))

        # se sincronizan las cajas desde el servidor
        api_cajas_url = get_api_cajas_url(self.config_path)
        response = sync_cajas(api_url=api_cajas_url)

        if response[0] == 1:
            self.page.open(ft.SnackBar(ft.Text(response[1])))
        else:
            self.page.open(ft.SnackBar(ft.Text(response[1]), bgcolor=ft.Colors.RED_800))

    def load_config(self):
        """Carga la configuración desde el archivo."""
        self.config.read(self.config_path)

    def create_default_config(self):
        """Crea una configuración por defecto si no existe el archivo."""
        self.config["POS"] = {
            "numero_caja": "2",
            "usuario_caja": "admin",
            "carga_productos": "true",
        }
        self.config["POS-SERVIDOR"] = {
            "ip_servidor": "192.168.1.4",
            "port_servidor": "3555",
        }
        self.config["POS-API"] = {
            "api_port": "3555",
        }

        with open(self.config_path, "w") as configfile:
            self.config.write(configfile)

    def save_config(self, e):
        """Guarda la configuración en el archivo."""
        self.config["POS"]["numero_caja"] = self.txt_numero_caja.value
        self.config["POS"]["usuario_caja"] = self.txt_usuario_caja.value
        self.config["POS-SERVIDOR"]["ip_servidor"] = self.txt_ip_servidor.value
        self.config["POS-SERVIDOR"]["port_servidor"] = self.port_servidor.value
        self.config["POS"]["carga_productos"] = str(self.chk_carga_productos.value)

        with open(self.config_path, "w") as configfile:
            self.config.write(configfile)

        # ft.Toast("Configuración guardada correctamente.").show()
        self.page.open(ft.SnackBar(ft.Text(f"Configuración guardada correctamente")))
        self.page.update()
        # toast = CustomToast("Configuración guardada", duration=3, close_button=True)
        # toast.show(self.page)

    def close_window(self, e):
        """Cierra la ventana de configuración."""
        self.page.on_keyboard_event = None
        self.page.go("/")