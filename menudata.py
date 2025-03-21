import flet as ft


class ControlGroup:
    def __init__(self, name: str, label: str, icon: str, selected_icon: str = None, children: list = None):
        self.name = name
        self.label = label
        self.icon = icon
        self.selected_icon = selected_icon or icon
        self.children = children or []

    def add_child(self, child):
        self.children.append(child)


class MenuData:
    def __init__(self):
        self.control_groups = self.get_control_groups()

    def get_control_groups(self):
        return [
            ControlGroup(
                name="/",
                label="Inicio",
                icon=ft.icons.HOME,
                selected_icon=ft.icons.HOME_OUTLINED,
            ),
            ControlGroup(
                name="productos",
                label="Productos",
                icon=ft.icons.SHOPPING_BAG_OUTLINED,
                selected_icon=ft.icons.SHOPPING_BAG,
            ),
            ControlGroup(
                name="categorias",
                label="Categorias",
                icon=ft.icons.CATEGORY_OUTLINED,
                selected_icon=ft.icons.CATEGORY,
            ),
            ControlGroup(
                name="usuarios",
                label="Usuarios",
                icon=ft.icons.PERSON_OUTLINED,
                selected_icon=ft.icons.PERSON,
            ),
            ControlGroup(
                name="cajas",
                label="Cajas",
                icon=ft.Icons.COMPUTER,
                selected_icon=ft.icons.COMPUTER,
                children=[
                    ControlGroup(
                        name="cajas/listado",
                        label="Listado de Cajas",
                        icon=ft.icons.VIEW_LIST_OUTLINED,
                        selected_icon=ft.icons.VIEW_LIST,
                    ),
                    ControlGroup(
                        name="cajas/actividad",
                        label="Actividad de Cajas",
                        icon=ft.icons.EDIT_NOTE_OUTLINED,
                        selected_icon=ft.icons.EDIT_NOTE,
                    ),
                ],
            ),
            ControlGroup(
                name="ventas",
                label="Ventas",
                icon=ft.icons.RECEIPT_LONG_OUTLINED,
                selected_icon=ft.icons.RECEIPT_LONG,
                children=[
                    ControlGroup(
                        name="ventas/listado",
                        label="Listado de Ventas",
                        icon=ft.icons.VIEW_LIST_OUTLINED,
                        selected_icon=ft.icons.VIEW_LIST,
                    ),
                    ControlGroup(
                        name="ventas/detalle",
                        label="Detalle de Ventas",
                        icon=ft.icons.INFO_OUTLINED,
                        selected_icon=ft.Icons.INFO,
                    ),
                ],
            ),
        ]

