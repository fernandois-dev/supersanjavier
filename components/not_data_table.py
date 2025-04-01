import flet as ft
import copy
from components.custom_dialogs import DlgConfirm
from components.field_builder import FieldBuilder
from pages.conditions import Conditions
from components.custom_input import DisplayMode, LayoutMode, get_input_by_type

class NotDataTableHeader(ft.Container):
    def __init__(self, data, model, is_chk_column_enabled = True, is_editable = False, handle_all_row_selected=None, on_click_column=None, conditions=Conditions(), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_chk_column_enabled = is_chk_column_enabled
        self.content= None
        self.bgcolor=ft.Colors.with_opacity(1, ft.Colors.SECONDARY_CONTAINER)
        self.height=45
        self._dict = {}
        
        self.bg_color_prin = ft.Colors.with_opacity(1, ft.Colors.SECONDARY_CONTAINER)
        self.bg_color_sec = ft.Colors.with_opacity(0.1, ft.Colors.SECONDARY)
        self.on_click_column = on_click_column
        self.handle_all_row_selected = handle_all_row_selected
        self._data = data
        self._model = model
        self.is_editable = is_editable
        
        self.conditions = conditions
        
        self.chk_column = ft.Checkbox(label="", value=False, width=40, tristate=True, on_change=lambda e: self.handle_all_row_selected(e))
    
    def build_header(self):
        list_header_row = []
            # HEADERS
        if not list_header_row:
            if self.is_chk_column_enabled: list_header_row.append(self.chk_column)
            
            if self.is_editable: list_header_row.append(ft.Container(width=40))
            
            fields_order = self.conditions.fields_order or [field.name for field in self._model._meta.fields]
        
            for field_name in fields_order:
                col = next((field for field in self._model._meta.fields if field.name == field_name), None)
                if not col:
                    continue
                if col.hidden or col.name in self.conditions.fields_excluded: 
                    continue
                
                
                order_col = ""
                for key in self._dict:
                    if key == col.name:
                        order_col = f'{key}-{self._dict[key]}'
                    
                # HEADER ALIGMENT    
                if col.aligment == "center":
                    header_aligment = ft.MainAxisAlignment.CENTER
                elif col.aligment == "right":
                    header_aligment = ft.MainAxisAlignment.END
                else:
                    header_aligment = ft.MainAxisAlignment.START
                    
                
                icon = ft.Container()
                text_header_expand = None
                sort = getattr(col, "is_sortable", False) if not self.is_editable else False
                if sort:
                    icon = ft.Icon("arrow_drop_down") if "desc" in order_col else ft.Icon("arrow_drop_up")
                    text_header_expand = 1
                text_header = ft.Container(
                    content=ft.Row(
                        controls=[ft.Text(col.verbose_name, weight="bold", expand=text_header_expand),icon],
                        alignment=header_aligment),
                    margin=ft.margin.symmetric(horizontal=0),
                    expand=True,
                )
                    
                container = ft.Container(text_header, 
                    on_hover=(lambda e: on_hover(e)) if sort else None,
                    on_click=(lambda e: on_click(e)) if sort else None,
                    expand=self.conditions.fields_expand.get(col.name, 1),
                    data=col.name,
                    padding=ft.padding.symmetric(horizontal=5),
                    alignment=ft.alignment.center_left,
                    bgcolor=self.bg_color_sec if col.name in order_col else self.bg_color_prin,
                    # margin=ft.margin.symmetric(horizontal=5),
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

              
class NotDataRowTable(ft.Container):
    def __init__(self, obj, idx, confirm_delete_row=None, is_editable = False, conditions={}, is_chk_column_enabled=True, handle_on_long_press=None,
                 handle_chk_row_selected=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = obj
        self.idx = idx
        self.confirm_delete_row = confirm_delete_row
        self.conditions = conditions
        self.is_editable = is_editable
        self.is_chk_column_enabled = is_chk_column_enabled
        self.handle_on_long_press = handle_on_long_press
        self.handle_chk_row_selected = handle_chk_row_selected
        self.is_selected:bool = False
        
        self.padding = ft.padding.only(top=2, bottom=0)
        self.border = ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.with_opacity(0.2 , ft.Colors.ON_SURFACE_VARIANT)))
        self.bgcolor= ft.Colors.with_opacity(0.0 if idx%2 == 0 else 0.3  , ft.Colors.SECONDARY_CONTAINER)
        self.alignment=ft.alignment.center
        self.on_long_press= None if is_editable else lambda e: self.handle_on_long_press(obj)
        self.on_hover = None if is_editable else lambda e: self.handle_on_hover(e)
        
        self.chk_column = ft.Checkbox(value= False, width=40, height=40, on_change=lambda e: self.handle_chk_row_selected(e), data=obj)
        self.btn_remove_row = ft.TextButton(content=ft.Row([ft.Icon(name=ft.Icons.REMOVE, size=28),]),
                                           width=40, height=30,
                                           style=ft.ButtonStyle(padding=ft.padding.all(5), bgcolor=ft.Colors.TERTIARY_CONTAINER, shape=ft.RoundedRectangleBorder(radius=3)),
                                           on_click=lambda e, idx=idx: self.delete_row())
        
        self.controls = []
        if self.is_chk_column_enabled: 
            self.controls.append(self.chk_column)
        if self.is_editable: 
            self.controls.append(ft.Container(content=self.btn_remove_row, margin=ft.margin.symmetric(horizontal=0, vertical=0)))
            
        diplay_mode=DisplayMode.EDIT if self.is_editable else DisplayMode.VIEW
        self.form = FieldBuilder(obj=obj, layout_mode=LayoutMode.HORIZONTAL, diplay_mode=diplay_mode, conditions=self.conditions, page=self.page)
        self.controls.append(self.form)
        self.content= ft.Row(controls=self.controls, vertical_alignment=ft.VerticalAlignment.CENTER, spacing=0)
        
    def check_is_selected(self):
        return self.chk_column.value if self.chk_column else False
    
    def handle_on_hover(self, e):
        self.bgcolor =  ft.Colors.with_opacity(0.8, ft.Colors.SECONDARY_CONTAINER) if e.data == "true" else ft.Colors.with_opacity(0.1 if self.idx%2 == 0 else 0.4  , ft.Colors.SECONDARY_CONTAINER)
        self.update()
        
    def save(self, **kwargs):
        return self.form.save(**kwargs)
        
    def delete_obj(self):
        if not self.obj._state.adding:
            self.obj.delete()
            
    def delete_row(self):
        if not self.obj._state.adding or self.form.check_is_dirty():
            DlgConfirm(page=self.page, title="Confirma que desea eliminar los registros?", fn_yes=lambda: self.handle_remove_yes())
        else:
            self.handle_remove_yes()
                 
    def handle_remove_yes(self):
        if self.obj._state.adding:
            self.is_selected = True
            self.confirm_delete_row()
        else:
            try:
                elemento = self.obj
                relaciones = self.obtener_relaciones(elemento)
                
                if relaciones:
                    self.dlg_msg = ft.AlertDialog(title=ft.Text(f"No se puede eliminar {str(elemento)}. Registros relacionados: {relaciones}"))
                    self.page.open(self.dlg_msg)
                else:
                    elemento.delete()
                self.is_selected = True
                self.confirm_delete_row()
            except Exception as e:
                self.dlg_msg = ft.AlertDialog(title=ft.Text(f"Error al eliminar los registros: {e}"))
                self.page.open(self.dlg_msg)
            
    def obtener_relaciones(self, obj):
        """
        Devuelve un diccionario con los nombres de los modelos relacionados y la cantidad de registros asociados.
        """
        relaciones = {}
        for relation in obj._meta.related_objects:
            related_name = relation.get_accessor_name()
            related_manager = getattr(obj, related_name)
            
            count = related_manager.count()  # Contar registros relacionados
            if count > 0:
                relaciones[relation.related_model.__name__] = count
        
        return relaciones

    def set_value_chk_row(self, value):
        self.chk_column.value = value
        self.chk_column.update()
   
    def handle_row_selected(self, e):
        list_rows_selected = self.list_rows_selected()
        self.header.manage_chk_header(len(list_rows_selected), len(self.rows))
    
        if self.on_row_selected:
            self.on_row_selected(list_rows_selected)
            
        e.control.update()
      
    def list_rows_selected(self):
        return [row.data["obj_original"] for row in self.controls if row.data["chk"].value]
            
    def _confirm_delete_row(self):
        self.is_selected = True
        if self.confirm_delete_row:
            self.confirm_delete_row()
            
    def check_is_selected(self):
        return self.is_selected
    
    def set_is_selected(self, value):
        self.is_selected = value
    
    def check_is_dirty(self):
        return self.form.check_is_dirty()
            
    def handle_chk_selected(self, e):
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


class NotDataTable(ft.Column):
    def __init__(self, is_chk_column_enabled = True, is_editable = False, handle_on_long_press=None, handle_on_chk_row_click=None, on_row_selected=None,
                 handle_on_chk_header_click=None, conditions=Conditions(), page:ft.Page=None, *args, **kwargs):
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
        self.on_row_selected = on_row_selected
        self.handle_on_long_press = handle_on_long_press
        self.handle_on_chk_row_click = handle_on_chk_row_click
        self.handle_on_chk_header_click = handle_on_chk_header_click
        self.on_click_column = None
        
        self.conditions = conditions
        
        self.dict_order = {}
        
        self.chk_column = None
        
        self.component_buttons = ft.Container()
        self.component_header = ft.Column(controls=[], spacing=0)
        self.component_body = ft.Column(controls=[], spacing=0)
        self.component_footer = ft.Column(controls=[], spacing=0)     
        self.controls = [self.component_buttons, self.component_header, self.component_body, self.component_footer]
        
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
        self.header = NotDataTableHeader(
                        is_chk_column_enabled=self.is_chk_column_enabled, 
                        data=self._data, 
                        model=self._model, 
                        is_editable=self.is_editable, 
                        conditions=self.conditions,
                        handle_all_row_selected = self.handle_on_click_chk_row,
                        on_click_column=self.on_click_column)
        self.header.build_header()
        self.component_header.controls = [self.header]
    
    def build_body(self):
        self.rows = []
        list_data_row = []
        for idx, obj in enumerate(self._data):
            # list_data_row.append(self.make_row(idx, obj))
            list_data_row.append(NotDataRowTable(obj, idx, 
                                                is_editable=self.is_editable, 
                                                conditions=self.conditions, 
                                                handle_on_long_press=self.handle_on_long_press, 
                                                is_chk_column_enabled=self.is_chk_column_enabled,
                                                handle_chk_row_selected=self.handle_chk_row_selected,
                                                confirm_delete_row=self.confirm_delete_row,
                                                ),
                                                
                                 )
        self.component_body.controls=list_data_row
        if self.is_editable:
            self.component_footer.controls.append(ft.Container(content=self.btn_add_row, margin=ft.margin.symmetric(horizontal=0, vertical=5)))
        else:
            self.component_footer.controls = []
        a = 0
    
    def confirm_delete_row(self):
        self.component_body.controls = [row for row in self.component_body.controls if not row.check_is_selected()]
        self.update_body()
        
    def update_body(self):
        self.component_body.update()
        
    def create_table(self):
        self.build_header()
        self.build_body()
    
    
    def handle_chk_row_selected(self, e):
        list_rows_selected = self.list_rows_selected()
        self.header.manage_chk_header(len(list_rows_selected), len(self.component_body.controls))
    
        if self.on_row_selected:
            self.on_row_selected(list_rows_selected)
            
        e.control.update()
        
    def list_rows_selected(self):
        return [row.obj for row in self.component_body.controls if row.check_is_selected()]
        # for row in self.component_body.controls:
        #     if row.chk_column.value:
        #         return True
        
    def handle_on_click_chk_row(self, e):
        if e.control.value == None:
            e.control.value = False
            e.control.update()
        
        for row in self.component_body.controls:
            row.set_value_chk_row(e.control.value)
            
                
        list_rows_selected = self.list_rows_selected()
        if self.on_row_selected:
            self.on_row_selected(list_rows_selected)
        
        # self.controls = [self.component_header, self.component_body]
        # if self.is_editable:
        #     self.switch_edit.value = False if self._data else True
        #     self.controls.insert(0, ft.Container(content=ft.Row(controls=[self.switch_edit], 
        #                                                         alignment=ft.MainAxisAlignment.END), 
        #                                          margin=ft.margin.symmetric(horizontal=10, vertical=5)))
        # self.update()
            
    # def make_row(self, idx, obj):
    #     list_data_cell = []
    #     original_obj = copy.deepcopy(obj)
        
    #     self.chk_column = ft.Checkbox(value= False, width=40, height=40, on_change=lambda e: handle_row_selected(e), data=obj)
        
    #     if self.is_chk_column_enabled: list_data_cell.append(self.chk_column)
    #     if self.is_editable: 
    #         btn_remove_row = ft.TextButton(content=ft.Row([ft.Icon(name=ft.Icons.REMOVE, size=28),]),
    #                                        width=40, height=30,
    #                                        style=ft.ButtonStyle(padding=ft.padding.all(5), bgcolor=ft.Colors.TERTIARY_CONTAINER, shape=ft.RoundedRectangleBorder(radius=3)),
    #                                        on_click=lambda e, idx=idx: self.delete_row(e, idx))
    #         list_data_cell.append(ft.Container(content=btn_remove_row, margin=ft.margin.symmetric(horizontal=0, vertical=0)))
        
    #     diplay_mode=DisplayMode.EDIT if self.is_editable else DisplayMode.VIEW
    #     horizontal_form = FieldBuilder(obj=obj, layout_mode=LayoutMode.HORIZONTAL, diplay_mode=diplay_mode, conditions=self.conditions, page=self.page)
    #     list_data_cell.append(horizontal_form)
            
    #     def handle_row_selected(e):
    #         list_rows_selected = self.list_rows_selected()
    #         self.header.manage_chk_header(len(list_rows_selected), len(self.rows))
        
    #         if self.on_row_selected:
    #             self.on_row_selected(list_rows_selected)
                
    #         e.control.update()
    #     long_press = None
    #     if not self.is_editable:
    #         long_press = lambda e: self.handle_long_press(obj)
            
    #     row_container = ft.Container(content= ft.Row(controls=list_data_cell, vertical_alignment=ft.VerticalAlignment.CENTER, spacing=0),
    #         # height=44,
    #         padding=ft.padding.only(top=2, bottom=0),
    #         border = ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.with_opacity(0.2 , ft.Colors.ON_SURFACE_VARIANT))),
    #         bgcolor= ft.Colors.with_opacity(0.0 if idx%2 == 0 else 0.3  , ft.Colors.SECONDARY_CONTAINER),
    #         alignment=ft.alignment.center,
    #         key=idx,
    #         on_long_press=long_press,
    #         data=horizontal_form,)
    #     def on_hover(e):
    #         row_container.bgcolor =  ft.Colors.with_opacity(0.8, ft.Colors.SECONDARY_CONTAINER) if e.data == "true" else ft.Colors.with_opacity(0.1 if e.control.key%2 == 0 else 0.4  , ft.Colors.SECONDARY_CONTAINER)
    #         row_container.update()
    #     if not self.is_editable:
    #         row_container.on_hover = lambda e: on_hover(e)      
        
    #     return row_container
    
    # def list_rows_selected(self):
    #     return [row.data["obj_original"] for row in self.component_body.controls if row.data["chk"].value]
        
    # def get_container_header (self, controls):
    #     header_row = ft.Container(
    #         content= ft.Row(controls=controls),
    #         bgcolor=ft.Colors.with_opacity(1, ft.Colors.SECONDARY_CONTAINER),
    #         height=45,
    #     )
    #     return header_row
    
    # def get_container_body (self, controls):
    #     header_row = ft.Container(
    #         content= ft.Row(controls=controls),
    #         bgcolor=ft.Colors.with_opacity(1, ft.Colors.SECONDARY_CONTAINER),
    #         height=40,
    #     )
    #     return header_row
        
    
        
    # def handle_long_press(self, obj):
    #     if self.on_long_press:
    #         self.on_long_press(obj)
        
    def add_row(self):
        idx = len(self.component_body.controls)
        # new_row = self.make_row(idx, self._model())
        new_row = NotDataRowTable(self._model(), idx, 
                                                is_editable=self.is_editable, 
                                                conditions=self.conditions, 
                                                handle_on_long_press=self.handle_on_long_press, 
                                                is_chk_column_enabled=self.is_chk_column_enabled,
                                                handle_chk_row_selected=self.handle_chk_row_selected,
                                                confirm_delete_row=self.confirm_delete_row
                                                )
        self.component_body.controls.append(new_row)
        self.update_body()
    
    def save(self, **kwargs):
        ret = True
        for row in self.component_body.controls:
            if not row.save(**kwargs):
                ret = False
        return ret
    
    def check_is_dirty(self):
        for row in self.component_body.controls:
            if row.check_is_dirty():
                return True
        return False
    
    # def on_changed_switch_edit(self, e):
    #     self.build_header()
    #     self.build_body()
    #     # self.is_being_edited = e.control.value
        
    #     # self.create_table()
        
    #     self.update()
            