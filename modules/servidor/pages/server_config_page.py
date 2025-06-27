import flet as ft
import configparser
import os

# from components.custom_input import CustomToast


class ServerConfigPage(ft.Container):
    def __init__(self, page=None, config_file=None):
        super().__init__()
        self.page = page
        self.config_path = os.path.abspath(os.path.join(os.getcwd(), "apps/servidor/server_settings.cfg")) if config_file is None else config_file
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"El archivo de configuración no se encontró en: {self.config_path}")
        self.config = configparser.ConfigParser()
        self.page.on_keyboard_event = self.handle_keypress

        # Cargar configuración existente o crear una nueva
        if os.path.exists(self.config_path):
            self.load_config()
        else:
            self.create_default_config()

        # Campos de configuración
        self.txt_numero_puerto = ft.TextField(
            label="Número de puerto",
            value=self.config.get("SERVER", "FASTAPI_PORT"),
            width=300,
        )

        # Botones
        self.btn_guardar = ft.ElevatedButton(
            text="Guardar Configuración",
            icon=ft.icons.SAVE,
            on_click=self.save_config,
        )
        self.btn_cerrar = ft.ElevatedButton(
            text="Cerrar",
            icon=ft.icons.CLOSE,
            on_click=self.close_window,
        )

        # Layout de la ventana
        self.content = ft.Column(
            controls=[
                ft.Text("Configuración del Servidor", size=20, weight=ft.FontWeight.BOLD),
                self.txt_numero_puerto,
                ft.Row(
                    controls=[self.btn_guardar, self.btn_cerrar],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            spacing=20,
            width=400,
            height=300,
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
        self.config.read(self.config_path)

    def create_default_config(self):
        """Crea una configuración por defecto si no existe el archivo."""
        self.config["SERVER"] = {
            "FASTAPI_PORT": "3500",
        }
        with open(self.config_path, "w") as configfile:
            self.config.write(configfile)

    def save_config(self, e):
        """Guarda la configuración en el archivo."""
        self.config["SERVER"]["FASTAPI_PORT"] = self.txt_numero_puerto.value

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
