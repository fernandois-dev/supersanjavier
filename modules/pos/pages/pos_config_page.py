import flet as ft
import configparser
import os

from components.custom_buttons import CustomButtonCupertino

# from components.custom_input import CustomToast


class POSConfigPage(ft.Container):
    def __init__(self, page=None, config_file="apps/cliente/pos_settings.cfg"):
        super().__init__()
        self.page = page
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.page.on_keyboard_event = self.handle_keypress

        # Cargar configuración existente o crear una nueva
        if os.path.exists(self.config_file):
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
        # Botones
        self.btn_guardar = CustomButtonCupertino(
            text="Guardar Configuración",
            icon_name=ft.icons.SAVE,
            on_click=self.save_config,
            color=ft.Colors.ON_SECONDARY,
            bgcolor=ft.Colors.SECONDARY,
        )
        self.btn_cerrar = CustomButtonCupertino(
            text="Cerrar",
            icon_name=ft.icons.CLOSE,
            on_click=self.close_window,
            color=ft.Colors.ON_SECONDARY,
            bgcolor=ft.Colors.SECONDARY,
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
                    ]
                ),
                ft.Row(
                    controls=[self.btn_guardar, self.btn_cerrar],
                    alignment=ft.MainAxisAlignment.END,
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
        
            
    def load_config(self):
        """Carga la configuración desde el archivo."""
        self.config.read(self.config_file)

    def create_default_config(self):
        """Crea una configuración por defecto si no existe el archivo."""
        self.config["POS"] = {
            "numero_caja": "1",
            "usuario_caja": "admin",
            "ip_servidor": "127.0.0.1",
            "port_servidor": "3555",
        }
        with open(self.config_file, "w") as configfile:
            self.config.write(configfile)

    def save_config(self, e):
        """Guarda la configuración en el archivo."""
        self.config["POS"]["numero_caja"] = self.txt_numero_caja.value
        self.config["POS"]["usuario_caja"] = self.txt_usuario_caja.value
        self.config["POS-SERVIDOR"]["ip_servidor"] = self.txt_ip_servidor.value
        self.config["POS-SERVIDOR"]["port_servidor"] = self.port_servidor.value

        with open(self.config_file, "w") as configfile:
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