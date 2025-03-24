import flet as ft
import copy
from components.custom_dialogs import DlgConfirm
from components.field_builder import FieldBuilder
from pages.conditions import Conditions
from components.custom_input import DisplayMode, LayoutMode, get_input_by_type

class NotDataTableHeader(ft.Container):
    def __init__(self, data, model, is_chk_column_enabled = True, is_being_editing = False, conditions=Conditions(), *args, **kwargs):
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
        self.is_being_editing = is_being_editing
        
        self.conditions = conditions
        
        self.chk_column = ft.Checkbox(label="", value=False, width=40, tristate=True, on_change=lambda e: self.handle_all_row_selected(e))
    
    def build_header(self):
        list_header_row = []
            # HEADERS
        if not list_header_row:
            if self.is_chk_column_enabled: list_header_row.append(self.chk_column)
            
            if self.is_being_editing: list_header_row.append(ft.Container(width=40))
            
            fields_order = self.conditions.fields_order or [field.name for field in self._model._meta.fields]
        
            for field_name in fields_order:
                col = next((field for field in self._model._meta.fields if field.name == field_name), None)
                if not col:
                    continue
                if col.hidden or col.name in self.conditions.fields_excluded: 
                    continue
                
                sort = getattr(col, "is_sortable", False)
                order_col = ""
                for key in self._dict:
                    if key == col.name:
                        order_col = f'{key}-{self._dict[key]}'
                    
                # HEADER ALIGMENT    
                if "BooleanField" in type(col).__name__:
                    header_aligment = ft.MainAxisAlignment.CENTER
                elif "IntegerField" in type(col).__name__ :
                    header_aligment = ft.MainAxisAlignment.END
                elif "MoneyField" in type(col).__name__ :
                    header_aligment = ft.MainAxisAlignment.END
                else:
                    header_aligment = ft.MainAxisAlignment.START
                    
                        
                if sort:
                    if "desc" in order_col:
                        icon = ft.Icon("arrow_drop_down")
                    else:
                        icon = ft.Icon("arrow_drop_up")
                    
                    text_header = ft.Container(
                        content=ft.Row(
                            controls=[ft.Text(col.verbose_name, weight="bold", expand=True), icon], 
                            alignment=header_aligment), 
                        margin=ft.margin.symmetric(horizontal=0),
                    )
                else:
                    text_header = ft.Container(
                        content=ft.Row(
                            controls=[ft.Text(col.verbose_name, weight="bold"),],
                            alignment=header_aligment),
                        margin=ft.margin.symmetric(horizontal=0),
                        expand=True,
                    )
                    
                
                # if "BooleanField" in type(col).__name__:
                #     container = ft.Container(text_header, 
                #                                         expand=1, alignment=ft.alignment.center, 
                #                                         on_hover= (lambda e: on_hover(e)) if sort else None,
                #                                         on_click= (lambda e: on_click(e)) if sort else None,
                #                                         data=col.name,
                #                                         bgcolor= self.bg_color_sec if col.name in order_col else self.bg_color_prin,
                #                                         )
                # elif "IntegerField" in type(col).__name__ :
                #     container = ft.Container(text_header, 
                #                                         on_hover= (lambda e: on_hover(e)) if sort else None,
                #                                         on_click= (lambda e: on_click(e)) if sort else None,
                #                                         expand=1, 
                #                                         data=col.name,
                #                                         alignment=ft.alignment.center_right,
                #                                         bgcolor= self.bg_color_sec if col.name in order_col else self.bg_color_prin,
                #                                         )
                # else:
                #     container = ft.Container(text_header, 
                #                                         on_hover= (lambda e: on_hover(e)) if sort else None,
                #                                         on_click= (lambda e: on_click(e)) if sort else None,
                #                                         expand=1,
                #                                         data=col.name,
                #                                         padding=ft.padding.symmetric(horizontal=0),
                #                                         alignment=ft.alignment.center_left,
                #                                         bgcolor= self.bg_color_sec if col.name in order_col else self.bg_color_prin,
                #                                         )
                container = ft.Container(text_header, 
                                                        on_hover= (lambda e: on_hover(e)) if sort else None,
                                                        on_click= (lambda e: on_click(e)) if sort else None,
                                                        expand=self.conditions.fields_expand.get(col.name, 1),
                                                        data=col.name,
                                                        padding=ft.padding.symmetric(horizontal=0),
                                                        alignment=ft.alignment.center_left,
                                                        bgcolor= self.bg_color_sec if col.name in order_col else self.bg_color_prin,
                                                        margin=ft.margin.symmetric(horizontal=5),
                                                        )
                # container.expand = self.conditions.fields_expand.get(col.name, 1)
                list_header_row.append(container)
                
        self.content= ft.Row(controls=list_header_row, spacing=0)

        
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

              
# class NotDataRowTable(ft.Row):
#     def __init__(self, obj, is_editable = False, conditions={}, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.obj = obj
#         self.is_editable = is_editable
#         self.controls = []
#         self.dict_values = {}
#         self.expand = True
        
#         self.conditions = conditions
        
#         self.make_row()
        
        
#     def make_row(self):
#         list_data_cell = []
#         # list_row_values = {}
        
#         fields_order = self.conditions.fields_order or [field.name for field in self.obj._meta.fields]
        
#         for field_name in fields_order:
#             col = next((field for field in self.obj._meta.fields if field.name == field_name), None)
#             if not col:
#                 continue
            
#             value = getattr(self.obj, col.name, None)
#             # self.dict_values[col.name] = value
#             if col.hidden or col.name in self.conditions.fields_excluded: continue
#             # list_row_values[col.name] = value
#             if self.is_editable:
#                 if "BooleanField" in type(col).__name__:
#                     input = get_input_by_type(ControlInputType.CustomCheckbox, value=value, name=col.name, on_change=self.create_on_change_handler(col))
#                     aligment = ft.alignment.bottom_center
#                 elif "IntegerField" in type(col).__name__:
#                     input = get_input_by_type(ControlInputType.CustomIntegerField, value=value, name=col.name, on_change=self.create_on_change_handler(col))
#                     aligment = ft.alignment.center_right
#                 elif "MoneyField" in type(col).__name__:
#                     input = get_input_by_type(ControlInputType.CustomIntegerField, value=value, name=col.name, on_change=self.create_on_change_handler(col))
#                     aligment = ft.alignment.center_right
#                 elif "ForeignKey" in type(col).__name__:
#                     input = get_input_by_type(ControlInputType.CustomSearchInput, model=col.related_model, name=col.name, value=value, data=value, page=self.page, on_change=self.create_on_change_handler(col))
#                     aligment = ft.alignment.center_left
#                 else:
#                     input = get_input_by_type(ControlInputType.CustomTextField, value=value, name=col.name, on_change=self.create_on_change_handler(col))
#                     aligment = ft.alignment.center_left
#                 list_data_cell.append(ft.Container(content=input, expand=1, alignment=aligment, data=col.name))
#             else:
#                 if "BooleanField" in type(col).__name__:
#                     list_data_cell.append(ft.Container(content=ft.Checkbox(value=value, disabled=True), expand=1, alignment=ft.alignment.center))
#                 elif "IntegerField" in type(col).__name__:
#                     list_data_cell.append(
#                         ft.Container(ft.Text("{:,}".format(value).replace(",", ".") if value is not None else ""), expand=1, alignment=ft.alignment.center_right))
#                 else:
#                     list_data_cell.append(ft.Container(ft.Text(value), expand=1, alignment=ft.alignment.center_left))
        
#         self.controls=list_data_cell
    
#     def create_on_change_handler(self, col):
#         def on_change(e, value = None):
#             def update_depentents(obj, col_name):
#                 for field, depend_calculation in self.conditions.fields_calculations.items():
#                     depends = depend_calculation.get("depends", [])
#                     calculation = depend_calculation.get("calculation", None)
#                     if col_name in depends:  # Evitar recalcular el mismo campo
#                         new_value = calculation(obj)
#                         setattr(obj, field, new_value)
                        
#                         # Actualizar el control correspondiente
#                         for control in self.controls:
#                             if control.data == field:
#                                 if isinstance(control.content, ft.TextField):
#                                     control.content.value = new_value
#                                 elif isinstance(control.content, ft.Checkbox):
#                                     control.content.value = bool(new_value)
#                                 control.update()
                        
#                         update_depentents(obj, field)
#              # Actualizar el valor del campo
#             setattr(self.obj, col.name, e.control.value if e else value)
#             update_depentents(self.obj, col.name) # Actualizar los campos dependientes
             
#         return on_change
        

class NotDataTable(ft.Column):
    def __init__(self, is_chk_column_enabled = True, is_editable = False, conditions=Conditions(), page:ft.Page=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expand = True
        self.header = None
        self.page=page
        self.rows = []
        self.spacing=0
        self._data = None
        self._model = None
        self.is_chk_column_enabled = is_chk_column_enabled
        self.is_editable = is_editable
        self.is_being_edited = False
        self.on_row_selected = None
        self.on_long_press = None
        self.on_click_column = None
        
        self.conditions = conditions
        
        self.dict_order = {}
        
        self.chk_column = None
        
        self.component_header = ft.Column(controls=[], spacing=0)
        self.component_body = ft.Column(controls=[], spacing=0)
        self.component_footer = ft.Column(controls=[], spacing=0)
        self.component_buttons = ft.Container()
        
        self.controls = [self.component_buttons, self.component_header, self.component_body, self.component_footer]
        
        self.switch_edit = ft.Switch(label="Editar", on_change=self.on_changed_switch_edit, value=True)
        self.btn_add_row = ft.TextButton(content=ft.Row([ft.Icon(name=ft.Icons.ADD, size=28),]),
                    width=40,height=40,
                    style=ft.ButtonStyle(padding=ft.padding.all(5), bgcolor=ft.Colors.PRIMARY_CONTAINER, shape=ft.RoundedRectangleBorder(radius=3)),
                    on_click=lambda e: self.add_row()
                )
        self.btn_remove_row = ft.TextButton(content=ft.Row([ft.Icon(name=ft.Icons.REMOVE, size=28),]),
                    width=40,height=40,
                    style=ft.ButtonStyle(padding=ft.padding.all(5), bgcolor=ft.Colors.TERTIARY_CONTAINER, shape=ft.RoundedRectangleBorder(radius=3)),
                    on_click=lambda e: self.delete_selected_rows(e)
                )
        
        
    def set_data(self, data):
        self._data = data
        
    def set_model(self, model):
        self._model = model
        
    def build_header(self):
        self.header = NotDataTableHeader(is_chk_column_enabled=self.is_chk_column_enabled, data=self._data, model=self._model, is_being_editing=self.switch_edit.value and self.is_editable, conditions=self.conditions)
        self.header.on_click_column = self.on_click_column
        self.header.handle_all_row_selected = self.handle_all_row_selected
        self.header.build_header()
        self.component_header.controls = [self.header]
    
    def build_body(self):
        self.rows = []
        list_data_row = []
        for idx, obj in enumerate(self._data):
            list_data_row.append(self.make_row(idx, obj))
        self.component_body.controls=list_data_row
        if self.is_editable and self.switch_edit.value:
            self.component_body.controls.append(ft.Container(content=self.btn_add_row, margin=ft.margin.symmetric(horizontal=0, vertical=5)))
        a = 0
        
        
    def update_body(self):
        self.component_body.update()
        
    def create_table(self):
        self.build_header()
        self.build_body()
        
        # self.controls = [self.component_header, self.component_body]
        if self.is_editable:
            self.switch_edit.value = False if self._data else True
            self.controls.insert(0, ft.Container(content=ft.Row(controls=[self.switch_edit], 
                                                                alignment=ft.MainAxisAlignment.END), 
                                                 margin=ft.margin.symmetric(horizontal=10, vertical=5)))
        # self.update()
            
    def make_row(self, idx, obj):
        list_data_cell = []
        original_obj = copy.deepcopy(obj)
        
        self.chk_column = ft.Checkbox(value= False, width=40, height=40, on_change=lambda e: handle_row_selected(e), data=obj)
        
        if self.is_chk_column_enabled: list_data_cell.append(self.chk_column)
        if self.is_editable and self.switch_edit.value: 
            btn_remove_row = ft.TextButton(content=ft.Row([ft.Icon(name=ft.Icons.REMOVE, size=28),]),
                                           width=40, height=30,
                                           style=ft.ButtonStyle(padding=ft.padding.all(5), bgcolor=ft.Colors.TERTIARY_CONTAINER, shape=ft.RoundedRectangleBorder(radius=3)),
                                           on_click=lambda e, idx=idx: self.delete_row(e, idx))
            list_data_cell.append(ft.Container(content=btn_remove_row, margin=ft.margin.symmetric(horizontal=0, vertical=0)))
        
        diplay_mode=DisplayMode.EDIT if self.switch_edit.value and self.is_editable else DisplayMode.VIEW
        list_data_cell.append(FieldBuilder(obj=obj, layout_mode=LayoutMode.HORIZONTAL, diplay_mode=diplay_mode, conditions=self.conditions, page=self.page))
            
        def handle_row_selected(e):
            list_rows_selected = self.list_rows_selected()
            self.header.manage_chk_header(len(list_rows_selected), len(self.rows))
        
            if self.on_row_selected:
                self.on_row_selected(list_rows_selected)
                
            e.control.update()
        
        row_container = ft.Container(content= ft.Row(controls=list_data_cell, vertical_alignment=ft.VerticalAlignment.CENTER, spacing=0),
            # height=44,
            padding=ft.padding.only(top=2, bottom=0),
            border = ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.with_opacity(0.2 , ft.Colors.ON_SURFACE_VARIANT))),
            bgcolor= ft.Colors.with_opacity(0.0 if idx%2 == 0 else 0.3  , ft.Colors.SECONDARY_CONTAINER),
            alignment=ft.alignment.center,
            key=idx,
            # on_long_press= lambda e: self.handle_long_press(obj),
            data={"obj_original":original_obj, "chk":self.chk_column},)
        def on_hover(e):
            row_container.bgcolor =  ft.Colors.with_opacity(0.8, ft.Colors.SECONDARY_CONTAINER) if e.data == "true" else ft.Colors.with_opacity(0.1 if e.control.key%2 == 0 else 0.4  , ft.Colors.SECONDARY_CONTAINER)
            row_container.update()
        if not (self.is_editable and self.switch_edit.value):
            row_container.on_hover = lambda e: on_hover(e)      
        
        return row_container
    
    def list_rows_selected(self):
        return [row.data["obj_original"] for row in self.component_body.controls if row.data["chk"].value]
        
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
        
    def add_row(self):
        idx = len(self.rows)
        new_row = self.make_row(idx, self._model())
        self.component_body.controls.insert(0, new_row)
        self.update_body()
    
    def compare_objects(self, obj1, obj2):
        for field in obj1._meta.fields:
            value1 = getattr(obj1, field.name, None)
            value2 = getattr(obj2, field.name, None)
            if value1 != value2:
                return False
        return True
    
    def confirm_delete_row(self, idx):
        del self.component_body.controls[idx]
        self.update_body()
  
    def delete_row(self, e, idx):
        obj = self.component_body.controls[idx].data["obj_original"]
        obj_editado = self.component_body.controls[idx].content.controls[1].obj
        if obj.id or not self.compare_objects(obj, obj_editado):
            DlgConfirm(page=self.page, title="Confirma que desea eliminar los registros?", fn_yes=lambda: self.confirm_delete_row(idx))
        else:
            self.confirm_delete_row(idx)
    # def delete_selected_rows(self, e):
    #     selected_rows = self.list_rows_selected()
    #     self._data = [obj for obj in self._data if obj.id not in selected_rows]
    #     self.build_body()
    #     self.update_body()
    
    def get_row_by_id(self, id):    
        for row in self.rows:
            if row[0].data.id == id:
                return row
        return None
    
    def save_changes(self):
        for row in self.rows:
            obj = row[0].data
            for col, cell in zip(obj._meta.fields, row[1:]):
                if isinstance(cell.content, ft.TextField):
                    setattr(obj, col.name, cell.content.value)
            obj.save()
    
    def on_changed_switch_edit(self, e):
        self.build_header()
        self.build_body()
        # self.is_being_edited = e.control.value
        
        # self.create_table()
        
        self.update()
            