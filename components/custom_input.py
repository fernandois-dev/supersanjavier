import flet as ft
from collections.abc import Callable
import locale
locale.setlocale(locale.LC_ALL, 'es_CL')
import datetime




class CustomTextField(ft.TextField):
    
    def __init__(self, is_required=False, name:str ="", input_type:str="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_required = is_required
        self.name = name
        self.input_type = input_type
    
    def get_value(self):
        # default value str
        if self.input_type == "int" and f"{self.value}".isdigit():
            return int(self.value)
        else:
            return self.value
        
class CustomDateTimeField(ft.Column):
    def __init__(self, is_required=False, name:str ="", label = "", helper_text="", helper_style=None, value=None, border_color=None,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_required = is_required
        self.name = name
        self.spacing = 2
        self._helper_text = helper_text
        self._helper_style = helper_style
        self._border_color = border_color
        self.value = value
        self.fecha = None if not value else value.strftime("%d-%m-%Y")
        self.hora = None if not value else value.strftime("%H:%M")
        self.txt_fecha = ft.TextField(label=label, value=self.fecha, width=160, read_only=True)
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
    
    def __init__(self, is_required=False, name:str ="",  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_required = is_required
        self.name = name
    
    def get_value(self):
        # default value str
        return self.value
    
    
class CustomDropdown(ft.Dropdown):
    def __init__(self, is_required=False, name:str ="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_required = is_required
        self.name = name
        self.width=350
        self.label_style = ft.TextStyle(weight=ft.FontWeight.NORMAL)
    
    def get_value(self):
        for opt in self.options:
            if self.value == opt.key:
                return opt.data
        return " "
        

