import flet as ft
from collections.abc import Callable
import locale
locale.setlocale(locale.LC_ALL, 'es_CL')
from django.core.exceptions import ValidationError
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
        

class FormButtons(ft.Row):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alignment=ft.MainAxisAlignment.END
        self.controls = []
        self.width=350

    def create_button(self, nombre, fn, color = ft.Colors.PRIMARY, bgcolor = ft.Colors.ON_PRIMARY):
        self.controls.append(
            ft.CupertinoButton(
                content=ft.Text(nombre),
                height=39, width=100,
                padding=ft.padding.symmetric(horizontal=10),
                on_click= lambda e: fn(),
                bgcolor=bgcolor,
                color=color
            )
        )

class FormFields(ft.Column):
    def __init__(self, obj, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alignment=ft.MainAxisAlignment.END
        self.controls = []
        self.init_values = {}
        self.width=350
        self.obj = obj
        
        
    def create_fields(self):
        self.init_values = {}
        self.controls = []
        for field in self.obj._meta.fields:
            if "BooleanField" in type(field).__name__ :
                self.controls.append(CustomCheckbox(label=field.verbose_name, name=field.name, value=getattr(self.obj, field.name)))
            if "CharField" in type(field).__name__ :
                self.controls.append(CustomTextField(label=field.verbose_name, name=field.name, value=getattr(self.obj, field.name),is_required=not field.null, input_type="str"))
            if "EmailField" in type(field).__name__ :
                self.controls.append(CustomTextField(label=field.verbose_name, name=field.name, value=getattr(self.obj, field.name),is_required=not field.null, input_type="str"))
            if "DateTimeField" in type(field).__name__ :
                self.controls.append(CustomDateTimeField(label=field.verbose_name, name=field.name, value=getattr(self.obj, field.name)))
            if "AutoField" in type(field).__name__ :
                self.controls.append(CustomTextField(label=field.verbose_name, name=field.name, value=getattr(self.obj, field.name), disabled=True, input_type="str"))
            if "IntegerField" in type(field).__name__ :
                self.controls.append(CustomTextField(label=field.verbose_name, name=field.name, value=getattr(self.obj, field.name), input_type="int"))    
            if "ForeignKey" in type(field).__name__ :
                self.controls.append(
                    CustomDropdown(label=field.verbose_name, name=field.name, value=getattr(self.obj, f"{field.name}_id") ,
                        options=[ft.dropdown.Option("", text=" ", data=None)] + [ ft.dropdown.Option(str(opt.id), text=str(opt), data=opt) for opt in field.related_model.objects.all()],)
                )
                
            # INIT VALUES, COMPARE TO SAVE
        for field in self.controls:
            if "ForeignKey" in type(field).__name__ :
                self.init_values[field.name] = field.related_model(id=field.value) if field.value else " "
            else:
                self.init_values[field.name] = field.get_value()
            
        

class Form(ft.Column):
    def __init__(self, obj, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controls = []
        self.width=350
        self.obj = obj
        self.form_fields = FormFields(self.obj)
        self.form_buttons = FormButtons()

    def create_fields(self):
        self.form_fields.create_fields()
        
    def create_button(self, *args, **kwargs):
        self.form_buttons.create_button(*args, **kwargs)
        
    def update_controls(self):
        self.controls = [self.form_fields, self.form_buttons]
    
    def validate(self):
        is_valid: bool = True
        for field in self.form_fields.controls:
            if hasattr(field, 'validate'):
                if not field.validate():
                    is_valid = False
        return is_valid
    
    def set_errors(self, errors):
        for field in self.form_fields.controls:
            if field.name in errors.message_dict:
                field.helper_text = ' - '.join(errors.message_dict[field.name])
                field.helper_style = ft.TextStyle(color="red")
                field.border_color = "red"
               
            else:
                field.helper_text = None
                field.border_color = None
            field.update()

    def save(self):
        form_values = self.get_values()
        # VALIDATION 
        obj_validation = self.obj
        for atributo in form_values: setattr(obj_validation, atributo, form_values[atributo])
        try:
            self.obj.full_clean()
            # SAVE
            for atributo in form_values: setattr(self.obj, atributo, form_values[atributo])
            self.obj.save()
            return True
        except ValidationError as ex:
            self.set_errors(ex)
            return False
    
    
    def get_values(self):
        ret = {}
        for field in self.form_fields.controls:
            if field.name == "id":
                if f"{field.name}".isdigit():
                    ret[field.name] = field.get_value()
            else:
                if self.form_fields.init_values[field.name] != field.get_value():
                    ret[field.name] = field.get_value()
        return ret
            
    def validate_form_change(self):
        is_valid: bool = True
        for field in self.form_fields.controls:
            if field.name != "id" and self.form_fields.init_values[field.name] != field.get_value():
                is_valid = False
        return is_valid
   
class NotDataTableHeader(ft.Container):
    def __init__(self, data, model, is_chk_column_enabled = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_chk_column_enabled = is_chk_column_enabled
        self.content= None
        self.bgcolor=ft.Colors.with_opacity(1, ft.Colors.SECONDARY_CONTAINER)
        self.height=45
        self._dict = {}
        
        self.bg_color_prin = ft.Colors.with_opacity(1, ft.Colors.SECONDARY_CONTAINER)
        self.bg_color_sec = ft.Colors.with_opacity(0.1, ft.Colors.SECONDARY)
        self.on_click_column = None
        self.handle_all_row_selected = None
        self._data = data
        self._model = model
        
        self.chk_column = ft.Checkbox(label="", value=False, width=40, tristate=True, on_change=lambda e: self.handle_all_row_selected(e))
    
    def build_header(self):
        list_header_row = []
            # HEADERS
        if not list_header_row:
            if self.is_chk_column_enabled: list_header_row.append(self.chk_column)
            for col in self._model._meta.fields:
                sort = getattr(col, "is_sortable", False)
                if not col.hidden:
                    order_col = ""
                    for key in self._dict:
                        if key == col.name:
                            order_col = f'{key}-{self._dict[key]}'
                        
                    # HEADER ALIGMENT    
                    if "BooleanField" in type(col).__name__:
                        header_aligment = ft.MainAxisAlignment.CENTER
                    elif "IntegerField" in type(col).__name__ :
                        header_aligment = ft.MainAxisAlignment.END
                    else:
                        header_aligment = ft.MainAxisAlignment.START
                        
                           
                    if sort:
                        if "desc" in order_col:
                            icon = ft.Icon("arrow_drop_down")
                        else:
                            icon = ft.Icon("arrow_drop_up")
                        
                        text_header = ft.Container(content=
                                            ft.Row(controls=[
                                                ft.Text(col.verbose_name, weight="bold", expand=True), 
                                                icon
                                            ], 
                                            alignment=header_aligment), 
                                            margin=ft.margin.symmetric(horizontal=5)
                                        )
                    else:
                        text_header = ft.Container(content=
                                        ft.Row(controls=[
                                            ft.Text(col.verbose_name, weight="bold"),                                       
                                        ],
                                        alignment=header_aligment
                                        ),
                                    margin=ft.margin.symmetric(horizontal=5),
                                    expand=True,
                                    
                                    )
                        
                    
                    if "BooleanField" in type(col).__name__:
                        list_header_row.append(ft.Container(text_header, 
                                                            expand=1, alignment=ft.alignment.center, 
                                                            on_hover= (lambda e: on_hover(e)) if sort else None,
                                                            on_click= (lambda e: on_click(e)) if sort else None,
                                                            data=col.name,
                                                            bgcolor= self.bg_color_sec if col.name in order_col else self.bg_color_prin,
                                                            ))
                    elif "IntegerField" in type(col).__name__ :
                        list_header_row.append(ft.Container(text_header, 
                                                            on_hover= (lambda e: on_hover(e)) if sort else None,
                                                            on_click= (lambda e: on_click(e)) if sort else None,
                                                            expand=1, 
                                                            data=col.name,
                                                            alignment=ft.alignment.center_right,
                                                            bgcolor= self.bg_color_sec if col.name in order_col else self.bg_color_prin,
                                                            ))
                    else:
                        list_header_row.append(ft.Container(text_header, 
                                                            on_hover= (lambda e: on_hover(e)) if sort else None,
                                                            on_click= (lambda e: on_click(e)) if sort else None,
                                                            expand=1,
                                                            data=col.name,
                                                            padding=ft.padding.symmetric(horizontal=5),
                                                            alignment=ft.alignment.center_left,
                                                            bgcolor= self.bg_color_sec if col.name in order_col else self.bg_color_prin,
                                                            ))
    
        self.content= ft.Row(controls=list_header_row)

        
        def on_hover(e):
            else_color = None
            if e.control.data in self._dict:
                else_color= ft.Colors.with_opacity(0.1, ft.Colors.SECONDARY)
            else:
                else_color= ft.Colors.with_opacity(1, ft.Colors.SECONDARY_CONTAINER)
                
            e.control.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.SECONDARY) if e.data == "true" else else_color
            e.control.update()
                
        def on_click(e):
            if e.control.data in self._dict:
                if self._dict[e.control.data] == "asc":
                    self._dict[e.control.data] = "desc"
                else:
                    self._dict[e.control.data] = "asc"
            else:
                self._dict = {}
                self._dict[e.control.data] = "desc"
            self.build_header()
            self.update()
            if self.on_click_column:
                self.on_click_column(self._dict)
                
    def manage_chk_header(self, len_list_rows_selected, len_rows):
        if(len_list_rows_selected == len_rows):
                self.chk_column.value = True
        elif(len_list_rows_selected == 0):
            self.chk_column.value = False
        else:
            self.chk_column.value = None
        self.chk_column.update()
                

class NotDataTable(ft.Column):
    def __init__(self, is_chk_column_enabled = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expand = True
        self.headers = []
        self.rows = []
        self.spacing=0
        self._data = None
        self._model = None
        self.is_chk_column_enabled = is_chk_column_enabled
        self.on_row_selected = None
        self.on_long_press = None
        self.on_click_column = None
        self.controls = []
        self.dict_order = {}
        
        self.not_headers= None
        self.chk_column = None
        
        self.component_header = None
        self.component_body = ft.Column(controls=[], spacing=0)
        
    def set_data(self, data):
        self._data = data
        
    def set_model(self, model):
        self._model = model
        
    def build_header(self):
        self.component_header = NotDataTableHeader(is_chk_column_enabled=self.is_chk_column_enabled, data=self._data, model=self._model)
        self.component_header.on_click_column = self.on_click_column
        self.component_header.handle_all_row_selected = self.handle_all_row_selected
        self.component_header.build_header()
    
    def build_body(self):
        self.rows = []
        list_data_row = []
        for idx, obj in enumerate(self._data):
            list_data_row.append(self.make_row(idx, obj))
        self.component_body.controls=list_data_row
        
    def update_body(self):
        self.component_body.update()
        
    def create_table(self):
        self.build_header()
        self.build_body()
        self.controls = [self.component_header, self.component_body]
            
    def make_row(self, idx, obj):
        list_data_cell = []
        self.chk_column = ft.Checkbox(value= False, width=40, on_change=lambda e: handle_row_selected(e), data=obj)
        if self.is_chk_column_enabled: list_data_cell.append(self.chk_column)
        for col in obj._meta.fields:
            value = getattr(obj, col.name)
            if not col.hidden:
                if "BooleanField" in type(col).__name__:
                    list_data_cell.append(ft.Container(content=ft.Checkbox(value= value, disabled=True), expand=1, alignment=ft.alignment.center))
                elif "IntegerField" in type(col).__name__ :
                    list_data_cell.append(
                        ft.Container(ft.Text("{:,}".format(value).replace(",", ".") if value is not None else ""), expand=1, alignment=ft.alignment.center_right))
                else:
                    list_data_cell.append(ft.Container(ft.Text(value), expand=1, alignment=ft.alignment.center_left))
                        
        self.rows.append(list_data_cell)
            
        def handle_row_selected(e):
            list_rows_selected = self.list_rows_selected()
            self.component_header.manage_chk_header(len(list_rows_selected), len(self.rows))
        
            if self.on_row_selected:
                self.on_row_selected(list_rows_selected)
                
            e.control.update()
        
        row_container = ft.Container(content= ft.Row(controls=list_data_cell ),
            height=40,
            border = ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.with_opacity(0.2 , ft.Colors.ON_SURFACE_VARIANT))),
            bgcolor=ft.Colors.with_opacity(0.0 if idx%2 == 0 else 0.3  , ft.Colors.SECONDARY_CONTAINER),
            key=idx,
            on_long_press= lambda e: self.handle_long_press(obj),
            data=obj.id)
        def on_hover(e):
            row_container.bgcolor =  ft.Colors.with_opacity(0.8, ft.Colors.SECONDARY_CONTAINER) if e.data == "true" else ft.Colors.with_opacity(0.1 if e.control.key%2 == 0 else 0.4  , ft.Colors.SECONDARY_CONTAINER)
            row_container.update()
        row_container.on_hover = lambda e: on_hover(e)      
        
        return row_container
    
    def list_rows_selected(self):
        return [row[0].data for row in self.rows if row[0].value]
        
    def get_container_header (self, controls):
        header_row = ft.Container(
            content= ft.Row(controls=controls),
            bgcolor=ft.Colors.with_opacity(1, ft.Colors.SECONDARY_CONTAINER),
            height=45,
        )
        return header_row
    
    def get_container_body (self, controls):
        header_row = ft.Container(
            content= ft.Row(controls=controls),
            bgcolor=ft.Colors.with_opacity(1, ft.Colors.SECONDARY_CONTAINER),
            height=40,
        )
        return header_row
        
    def handle_all_row_selected(self, e):
        if e.control.value == None:
            e.control.value = False
            e.control.update()
            
        if e.control.value:
            for row in self.rows:
                row[0].value = True
                row[0].update()
        else:
            for row in self.rows:
                row[0].value = False
                row[0].update()
                
        list_rows_selected = self.list_rows_selected()
        if self.on_row_selected:
            self.on_row_selected(list_rows_selected)
        
    def handle_long_press(self, obj):
        if self.on_long_press:
            self.on_long_press(obj)
        
    def clean_selection(self):
        for row in self.rows:
            row[0].value = False
        self.update()
        

 

# class CustomDataTable(ft.DataTable):
#     def __init__(self) -> None:
#         super().__init__(columns=[
#             ft.DataColumn(ft.Text("")),
            
#         ], rows=[])
#         self.expand = True
#         self.sort_column_index=0
#         self.sort_ascending=True
#         self.show_checkbox_column=True
#         self.count_rows_selected = 0
#         self.vertical_lines=ft.BorderSide(0.1)
#         self.fn_long_press = None
#         self._model = None
    
#     def set_model(self, input_model):
#         self._model = input_model
        
        
#     def populate_table(self):
#         list_data_row = []
#         list_data_column = []
#         list_obj = self._model.objects.all()
        
#         for obj in list_obj:
#             list_data_cell = []
            
            
#             # COLUMNS
#             if not list_data_column:
#                 list_data_column.append(ft.DataColumn(ft.Checkbox(label="", value=False)))
#                 for col in obj._meta.fields:
#                     if not col.hidden:
#                         list_data_column.append(ft.DataColumn(ft.Text(col.verbose_name, weight="bold"), 
#                             numeric= True if type(col).__name__ in ["IntegerField",]=="numeric" else False,
#                             on_sort=lambda e: print(f"{e.column_index}, {e.ascending}")
#                         ))
            
#             # ROWS
            
#             list_data_cell.append(ft.DataCell(ft.Checkbox(value= getattr(obj, col.name),disabled=True )))
#             for col in obj._meta.fields:
#                 if not col.hidden:
#                     if "BooleanField" in type(col).__name__:
#                         list_data_cell.append(ft.DataCell(ft.Checkbox(value= getattr(obj, col.name),disabled=True )))
#                     else:
#                         list_data_cell.append(ft.DataCell(ft.Text( getattr(obj, col.name) )))
                    
#             list_data_row.append(ft.DataRow(list_data_cell, 
#                                             data=obj.id,
#                                             on_select_changed=lambda e: self.set_row_selected(e), 
#                                             on_long_press= lambda e: self.handle_long_press(e)))
            
#         if list_data_column: self.columns = list_data_column
#         if list_data_row: self.rows = list_data_row
        
    
#     def fill_data_table(self):
#         self.populate_table()
#         self.update()
    
#     def set_row_selected(self, e):
#         e.control.selected = not (e.control.selected)
#         self.change_manu_bar(e)
#         e.control.update()
        
#     def handle_long_press(self, e):
#         if self.fn_long_press:
#             self.fn_long_press(edit_id = e.control.data)
#         print(e)
        
#     def change_manu_bar(self, e):
#         count = len([1 for row in self.rows if row.selected])
#         if count > 0:
#             self.parent.parent.set_actions_menu(count)
#         else:
#             self.parent.parent.set_search_menu()
        
#     def clean_selection(self):
#         for row in self.rows:
#             row.selected = False
#         self.update()
#         self.parent.parent.set_search_menu()
        
class DlgConfirm(ft.AlertDialog):
    def __init__(self, page: ft.Page, fn_yes: Callable = None) -> None:
        super().__init__()
        self.modal=True
        self.page = page
        self.title=ft.Text("Desea eliminar los registros?")
        self.actions_alignment=ft.MainAxisAlignment.END
        self.actions=[
            ft.TextButton("Si", on_click= lambda e : self.handle_yes()),
            ft.TextButton("No", on_click= lambda e : self.page.close(self)),
        ]
        self.fn_yes = fn_yes
    
    def set_open(self):
        self.page.open(self)
        
    def handle_yes(self):
        self.fn_yes()
        self.page.close(self)
    