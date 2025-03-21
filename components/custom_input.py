from enum import Enum
import inspect
import flet as ft
from collections.abc import Callable
import locale
locale.setlocale(locale.LC_ALL, 'es_CL')
import datetime
from data.serach import buscar_modelo
import json
from dataclasses import dataclass, field
from typing import Any, List, Optional

from flet.core.control import Control, OptionalNumber
from flet.core.control_event import ControlEvent
from flet.core.event_handler import EventHandler
from flet.core.ref import Ref
from flet.core.types import OptionalEventCallable
from flet.core.types import OptionalControlEventCallable

class DisplayMode(Enum):
    EDIT = "edit"
    VIEW = "view"
    
class LayoutMode(Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
    HORIZONTAL_WRAP = "horizontal_wrap"
    
STYLE_DEFAULT = {
    "height":44,
}


class CustomIconButton(ft.TextButton):
    def __init__(self, on_click, icon=ft.Icons.random, bgcolor=ft.Colors.PRIMARY_CONTAINER, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon=icon
        self.bgcolor=bgcolor
        self.width=40
        self.height=40
        self.content=ft.Row([ft.Icon(name=self.icon, size=28)])
        self.style=ft.ButtonStyle(padding=ft.padding.all(5), bgcolor=self.bgcolor, shape=ft.RoundedRectangleBorder(radius=3))
        self.on_click=on_click


class CustomAutoField(ft.TextField):
    def __init__(self, field, on_change, width=100, value=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = field.name
        self.label = field.verbose_name
        self.on_change = on_change
        self.value = value
        self.width = width
        self.read_only = True
        self.disabled = True

        
class CustomIntegerField(ft.TextField):
    def __init__(self, field, value=None, on_change=None, width=350, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = field.name
        self.value = value
        self.on_change = on_change
        self.width = width
        self.label = field.verbose_name
        self.height = STYLE_DEFAULT["height"]

    @property
    def value(self):
        try:
            return int(super().value) if super().value and super().value.isdigit() else None
        except ValueError:
            return None

    @value.setter
    def value(self, new_value):
        # Sobrescribir el setter para establecer el valor como cadena
        if  isinstance(new_value, int):
            super(CustomIntegerField, self.__class__).value.fset(self, str(new_value))
        else:
            super(CustomIntegerField, self.__class__).value.fset(self, new_value)
    
    def get_value(self):
        # default value str
        if self.input_type == "int" and f"{self.value}".isdigit():
            return int(self.value)
        else:
            return self.value


class CustomMoneyField(ft.TextField):
    def __init__(self, field, value=None,on_change=None, width=350, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = field.name
        self.custom_on_change = on_change
        self.label = field.verbose_name
        self.value = value
        self.width = width
        self.text_align = ft.TextAlign.RIGHT  # Alinear texto a la derecha
        self.on_focus = self.handle_focus
        self.on_blur = self.handle_blur
        self.height = STYLE_DEFAULT["height"]

        # Valor interno (numérico)
        self._numeric_value = None

        # Inicializar el valor si se pasa como argumento
        initial_value = kwargs.get("value", None)
        if initial_value is not None:
            self.value = initial_value  # Esto llamará al setter de `value`

    @property
    def value(self):
        """Valor visible (formateado como moneda)."""
        if self._numeric_value is None:
            return ""
        return self.format_currency(self._numeric_value)

    @value.setter
    def value(self, new_value):
        """Establece el valor interno (numérico) y actualiza el valor visible."""
        if new_value is None or new_value == "":
            self._numeric_value = None
        else:
            # Convertir el valor a un número entero
            if isinstance(new_value, str):
                self._numeric_value = self.parse_currency(new_value)
            elif isinstance(new_value, (int, float)):
                self._numeric_value = int(new_value)
            else:
                raise ValueError("El valor debe ser un número o una cadena formateada como moneda.")
        # Actualizar el valor visible en el campo
        super(CustomMoneyField, self.__class__).value.fset(self, self.format_currency(self._numeric_value))

    @property
    def numeric_value(self):
        """Valor interno (numérico) para usar en el ORM o cálculos."""
        return self._numeric_value

    @numeric_value.setter
    def numeric_value(self, new_value):
        """Permite establecer directamente el valor numérico interno."""
        self._numeric_value = int(new_value) if new_value is not None else None
        # Actualizar el valor visible en el campo
        super(CustomMoneyField, self.__class__).value.fset(self, self.format_currency(self._numeric_value))

    def handle_focus(self, e):
        """Seleccionar todo el texto al hacer focus."""
        self.selection_start = 0
        self.selection_end = len(self.value) if self.value else 0
        self.update()

    def handle_blur(self, e):
        """Formatear el valor al perder el foco."""
        self.numeric_value = self.parse_currency(super(CustomMoneyField, self.__class__).value.fget(self))
        if self._numeric_value is not None:
            self.value = self._numeric_value  # Esto llamará al setter de `value`
            self.update()
        
        # Disparar el evento on_change con el valor numérico
        if self.custom_on_change:
            self.custom_on_change(None, value=self.numeric_value)

    def format_currency(self, value):
        """Formatea un número como moneda (separado por puntos cada 3 dígitos)."""
        if value is None:
            return ""
        try:
            return f"{int(value):,}".replace(",", ".")
        except ValueError:
            return ""

    def parse_currency(self, value):
        """Convierte un valor formateado como moneda a un número entero."""
        try:
            return int(value.replace(".", ""))
        except ValueError:
            return None

# TODO Terinar de implementar CustomMoneyView
class CustomMoneyView(ft.Row):
    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value
        self.controls = [
            ft.Text(self.format_currency(value), size=16, weight=ft.FontWeight.BOLD, align=ft.TextAlign.RIGHT)
        ]
        
        
class CustomTextField(ft.TextField):
    def __init__(self, field, value=None, on_change=None, width=350, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = field.name
        self.on_change = on_change
        self.width = width
        self.value = value
        self.label = field.verbose_name
        self.height = STYLE_DEFAULT["height"]

    
    def get_value(self):
        # default value str
        if self.input_type == "int" and f"{self.value}".isdigit():
            return int(self.value)
        else:
            return self.value

     
class CustomDateTimeField(ft.Column):
    def __init__(self, field, value=None, on_change=None, helper_text="", read_only=False, helper_style=None, border_color=None,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = field.name
        self.on_change = on_change
        self.value = value
        self.spacing = 2
        self.width = 350
        self.height = STYLE_DEFAULT["height"]
        self._helper_text = helper_text
        self._helper_style = helper_style
        self._border_color = border_color
        self.fecha = None if not value else value.strftime("%d-%m-%Y")
        self.hora = None if not value else value.strftime("%H:%M")
        self.txt_fecha = ft.TextField(label=field.verbose_name, value=self.fecha, width=160, read_only=True)
        self.txt_hora = ft.TextField(label="Hora", value=self.hora, width=80, read_only=True)
        self.date_picker = ft.DatePicker(on_change=self.set_date)
        self.time_picker = ft.TimePicker(on_change=self.set_time)
        self.txt_error = ft.Container(content= ft.Text(self.helper_text, style=self.helper_style, size=11), 
                                      margin=ft.margin.only(left=10), 
                                      visible=True if self.helper_text else False )
        self.controls = [
            ft.Row(controls=[
                self.txt_fecha,
                ft.TextButton(
                    content=ft.Row([
                        ft.Icon(name=ft.Icons.CALENDAR_MONTH, size=28),
                    ]),
                    width=40,height=40,
                    style=ft.ButtonStyle(padding=ft.padding.all(5), bgcolor=ft.Colors.PRIMARY_CONTAINER, shape=ft.RoundedRectangleBorder(radius=3)),
                    on_click=self.open_date_picker
                ),
                self.txt_hora,
                ft.TextButton(
                    content=ft.Row([
                        ft.Icon(name=ft.Icons.ACCESS_TIME, size=28),
                    ]),
                    width=40,height=40,
                    style=ft.ButtonStyle(padding=ft.padding.all(5), bgcolor=ft.Colors.PRIMARY_CONTAINER, shape=ft.RoundedRectangleBorder(radius=3)),
                    on_click=self.open_time_picker
                )
            ]), self.txt_error]
        
    @property
    def helper_text(self):
        return self._helper_text
    
    @helper_text.setter
    def helper_text(self, value):
        self._helper_text = value
        self.txt_error.visible = True if value else False
        self.txt_error.content.value = value
        self.txt_error.update()
        
    @property
    def helper_style(self):
        return self._helper_style
    
    @helper_style.setter
    def helper_style(self, value):
        self._helper_style = value
        self.txt_error.content.style = value
        self.txt_error.update()
        
    @property
    def border_color(self):
        return self._border_color
    
    @border_color.setter
    def border_color(self, value):
        self._border_color = value
        self.txt_fecha.border_color = value
        self.txt_fecha.update()
        self.txt_hora.border_color = value
        self.txt_hora.update()
        
    

    def get_value(self):
        return self.value

    def set_date(self, e):
        self.fecha = datetime.datetime.fromisoformat(e.data).strftime("%d-%m-%Y")
        self.txt_fecha.value = self.fecha
        self.txt_fecha.update()
        self.update_value()
        # self.page.close_control(self.date_picker)

    def set_time(self, e):
        self.hora = e.data
        self.txt_hora.value = self.hora
        self.txt_hora.update()
        self.update_value()
        # self.page.close_control(self.time_picker)

    def open_date_picker(self, e):
        self.page.dialog = self.date_picker
        self.page.open(self.date_picker)

    def open_time_picker(self, e):
        self.page.dialog = self.time_picker
        self.page.open(self.time_picker)

    def update_value(self):
        if self.fecha and self.hora:
            try:
                self.value = datetime.datetime.strptime(f"{self.fecha} {self.hora}", "%d-%m-%Y %H:%M")
            except ValueError:
                self.value = None
        else:
            self.value = None


class CustomCheckbox(ft.Checkbox):
    
    def __init__(self, field, value=None, on_change=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = field.name
        self.label = field.verbose_name
        self.on_change = on_change
        self.value = value
    
    
class CustomDropdown(ft.Dropdown):
    def __init__(self, field, value=None, on_change=None, width=350, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = field.name
        self.value = value
        self.on_change = on_change
        self.width = width
        self.label_style = ft.TextStyle(weight=ft.FontWeight.NORMAL)
        self.options=[ft.dropdown.Option("", text=" ", data=None)] + [ ft.dropdown.Option(str(opt.id), text=str(opt), data=opt) for opt in field.related_model.objects.all()]
        self.label = field.verbose_name
        self.height = STYLE_DEFAULT["height"]

    
    def get_value(self):
        for opt in self.options:
            if self.value == opt.key:
                return opt.data
        return " "


class CustomSearchInput(ft.Row):
    def __init__(self , field, page:ft.Page, on_change = None,  model=None, value=None,data=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.on_change = on_change
        self.name = field.name
        self.model = model
        self.value = value
        self.data = data
        self.spacing = 2
        self.expand = True
        self.height = STYLE_DEFAULT["height"]
        # self.width = 350
        self.dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Busqueda"),
            content=ft.Text("Do you really want to delete all those files?"),
            actions=[
                ft.TextButton("ACEPTAR", on_click= lambda e : self.handle_dlg_yes()),
                ft.TextButton("CANCELAR", on_click= lambda e : self.handle_dlg_no()),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.btn_search = CustomIconButton(icon=ft.Icons.SEARCH, on_click=self.handle_search)
        self.txt_search = ft.TextField(label="Buscar", expand=True, on_submit=self.handle_submit)
        self.searchbar = ft.SearchBar(on_submit=self.handle_submit_searchbar, on_change=self.handle_on_change, value=self.value, data=self.data)
        self.searchbar.view_elevation = 0
        self.searchbar.bar_bgcolor = { ft.ControlState.DEFAULT: ft.Colors.SURFACE, 
                                     ft.ControlState.SELECTED: ft.Colors.SURFACE,  
                                     ft.ControlState.HOVERED: ft.Colors.SURFACE,  
                                     }
        self.searchbar.bar_shadow_color = ft.Colors.ON_PRIMARY
        self.searchbar.bar_shape = ft.RoundedRectangleBorder(radius=0)
        self.searchbar.view_shape = ft.RoundedRectangleBorder(radius=0)
        self.searchbar.bar_shadow_size = 0
        self.searchbar.expand = True
        self.searchbar.height = STYLE_DEFAULT["height"]
        # self.controls = [self.txt_search, self.btn_search]
        self.controls = [self.searchbar]
        
    def handle_search(self, e):
        self.page.open(self.dlg)
        
    def handle_dlg_no(self):
        if self.fn_no:
            pass
        self.page.close(self)
        
    def handle_dlg_yes(self):
        pass
        self.page.close(self)
          
    def close_anchor(self, e):
        text = f"{e.control.data}"
        self.searchbar.close_view(text)
        self.searchbar.value = e.control.data
        self.searchbar.data = e.control.data
        self.searchbar.bar_bgcolor ={ ft.ControlState.DEFAULT: ft.Colors.SECONDARY_CONTAINER, 
                                     ft.ControlState.SELECTED: ft.Colors.SECONDARY_CONTAINER,  
                                     ft.ControlState.HOVERED: ft.Colors.SECONDARY_CONTAINER,  
                                     }
        # ft.Colors.SECONDARY_CONTAINER
        self.data = e.control.data
        self.searchbar.update()
        self.on_change(None, value=self.data)

    # def handle_change(self, e):
        # print(f"handle_change e.data: {e.data}")
        
    def handle_on_change(self, e):
        self.searchbar.bar_bgcolor = ft.Colors.ON_PRIMARY
        self.data = None
        self.searchbar.update()
        self.on_change(None)
        
    def handle_submit_searchbar(self,e):
        if not e.data or len(e.data) <= 3: return
        
        result = buscar_modelo(self.model.objects.all(), e.data)
        if result:
            if len(result) == 1:
                self.searchbar.value = str(result[0])
                self.searchbar.data = result[0]
                self.searchbar.bar_bgcolor = ft.Colors.SECONDARY_CONTAINER
                self.data = result[0]
                self.searchbar.update()
                self.on_change(None, value=self.data)
            else:
                self.searchbar.controls = [ft.ListTile(title=ft.Text(f"{i}"), on_click=self.close_anchor, data=i) for i in result]
                self.searchbar.update()
                self.searchbar.open_view()

    def handle_submit(self,e):
        if not e.data or len(e.data) <= 3: return
        
        result = buscar_modelo(self.model.objects.all(), e.data)
        if result:
            if len(result) == 1:
                self.txt_search.value = str(result[0])
                self.txt_search.data = result[0]
                self.txt_search.update()
            

def get_input_by_type(input_type: str, **kwargs):
    list_inputs = {
            "CustomAutoField": CustomAutoField,
            "CustomIntegerField": CustomIntegerField,
            "CustomCharField": CustomTextField,
            "CustomEmailField": CustomTextField,
            "CustomDateTimeField": CustomDateTimeField,
            "CustomMoneyField": CustomMoneyField,
            "CustomBooleanField": CustomCheckbox,
            "CustomForeignKey": CustomDropdown,
            }

# TODO Agregar funcionalidad para visualizar los campos.
def get_view_by_type(input_type: str, **kwargs):
    list_inputs = {
            "CustomAutoField": CustomAutoField,
            }
    
    filtered_kwargs = filter_kwargs(list_inputs[input_type], kwargs)
    
    if input_type in list_inputs:
        return list_inputs[input_type](**filtered_kwargs)
    else:
        return None

def get_accepted_params(cls):
    """Obtiene los parámetros aceptados por el constructor de una clase."""
    signature = inspect.signature(cls.__init__)
    return list(signature.parameters.keys())

def filter_kwargs(cls, kwargs):
    """Filtra los parámetros de kwargs para que solo incluyan los aceptados por la clase."""
    accepted_params = get_accepted_params(cls)
    return {key: value for key, value in kwargs.items() if key in accepted_params}

class ManagerField(ft.Container):
    def __init__(self,
                 display_mode: DisplayMode = DisplayMode.VIEW,
                 layout_mode: LayoutMode = LayoutMode.VERTICAL,
                 input_type: str = "CustomCharField",
                 expand = 1,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_edit = None
        self.custom_view = None
        self.display_mode = display_mode
        self.input_type = input_type
        self.value = None
        self.name = ""
        self.content = ft.Text("sdfdsf")
        self.expand = expand if layout_mode != LayoutMode.HORIZONTAL_WRAP else None
    
    def build_field(self, **kwargs):
        self.value = kwargs.get("value", None)
        self.name = kwargs.get("name", "")
        if self.display_mode == DisplayMode.EDIT:
            self.custom_edit = get_input_by_type(self.input_type, **kwargs)
            self.content = self.custom_edit
        else:
            self.custom_view = ft.Text(self.value)
            self.content = self.custom_view
    
    def change_mode(self, mode):
        self.display_mode = mode
        if mode == DisplayMode.EDIT:
            self.content = self.custom_edit
        else:
            self.content = self.custom_view
        self.update()
        
    def get_field(self):
        return self.content
        
    
        
