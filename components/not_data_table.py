import flet as ft
from typing import Dict, List, Optional, Callable, Any
from components.custom_dialogs import DlgConfirm
from components.field_builder import FieldBuilder
from pages.conditions import Conditions
from components.custom_input import DisplayMode, LayoutMode
from utilities.style_manager import StyleManager as SM
from utilities.style_keys import StyleKeys as SK

class NotDataTableHeader(ft.Container):
    """
    Represents the header of a data table, including column headers and an optional checkbox for selecting all rows.
    """
    def __init__(
        self,
        data: List[Any],
        model: Any,
        is_chk_column_enabled: bool = True,
        is_editable: bool = False,
        handle_all_row_selected: Optional[Callable[[ft.ControlEvent], None]] = None,
        on_click_column: Optional[Callable[[Dict[str, str]], None]] = None,
        conditions: Conditions = Conditions(),
        *args,
        **kwargs,
    ):
        """
        Initializes the NotDataTableHeader component.

        Args:
            data (List[Any]): The data to display in the table.
            model (Any): The model associated with the table.
            is_chk_column_enabled (bool): Whether the checkbox column is enabled.
            is_editable (bool): Whether the table is editable.
            handle_all_row_selected (Optional[Callable[[ft.ControlEvent], None]]): Callback for selecting all rows.
            on_click_column (Optional[Callable[[Dict[str, str]], None]]): Callback for column click events.
            conditions (Conditions): Conditions for filtering and displaying data.
        """
        super().__init__(*args, **kwargs)
        self.is_chk_column_enabled = is_chk_column_enabled
        self.content= None
        
        self._dict = {}
        
        # UI properties
        self.bg_color_primary: str = ft.Colors.with_opacity(1, ft.Colors.SECONDARY_CONTAINER)
        self.bg_color_secondary: str = ft.Colors.with_opacity(0.1, ft.Colors.SECONDARY)
        self.bgcolor=ft.Colors.with_opacity(1, ft.Colors.SECONDARY_CONTAINER)
        self.height=45
        
        self.bg_color_prin = ft.Colors.with_opacity(1, ft.Colors.SECONDARY_CONTAINER)
        self.bg_color_sec = ft.Colors.with_opacity(0.1, ft.Colors.SECONDARY)
        self.on_click_column = on_click_column
        self.handle_all_row_selected = handle_all_row_selected
        self._data = data
        self._model = model
        self.is_editable = is_editable
        
        self.conditions = conditions
        
        # self.chk_column = ft.Checkbox(label="", value=False, width=40, tristate=True, on_change=lambda e: self.handle_all_row_selected(e))
    
    def build_header(self):
        list_header_row = []
        self.chk_column = ft.Checkbox(label="", value=False, width=40, tristate=True, on_change=lambda e: self.handle_all_row_selected(e))
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
                
    def clean_selection(self):
        self.chk_column.value = False
        self.chk_column.update()
                
    def _get_header_alignment(self, col: Any) -> ft.MainAxisAlignment:
        """
        Determines the alignment for a column header.

        Args:
            col (Any): The column to align.

        Returns:
            ft.MainAxisAlignment: The alignment for the column header.
        """
        if col.aligment == "center":
            return ft.MainAxisAlignment.CENTER
        elif col.aligment == "right":
            return ft.MainAxisAlignment.END
        return ft.MainAxisAlignment.START

    def _on_hover(self, e: ft.ControlEvent, col_name: str) -> None:
        """
        Handles hover events on column headers.

        Args:
            e (ft.ControlEvent): The hover event.
            col_name (str): The name of the column being hovered.
        """
        e.control.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.SECONDARY) if e.data == "true" else self.bg_color_primary
        e.control.update()

    def _on_click(self, e: ft.ControlEvent, col_name: str) -> None:
        """
        Handles click events on column headers to toggle sorting.

        Args:
            e (ft.ControlEvent): The click event.
            col_name (str): The name of the column being clicked.
        """
        if col_name in self._dict:
            self._dict[col_name] = "desc" if self._dict[col_name] == "asc" else "asc"
        else:
            self._dict = {col_name: "desc"}
        self.build_header()
        self.update()
        if self.on_click_column:
            self.on_click_column(self._dict)

    def manage_chk_header(self, len_list_rows_selected: int, len_rows: int) -> None:
        """
        Updates the state of the header checkbox based on the number of selected rows.

        Args:
            len_list_rows_selected (int): The number of selected rows.
            len_rows (int): The total number of rows.
        """
        if len_list_rows_selected == len_rows:
            self.chk_column.value = True
        elif len_list_rows_selected == 0:
            self.chk_column.value = False
        else:
            self.chk_column.value = None
        self.content.controls[0].update()

              
class NotDataRowTable(ft.Container):
    def __init__(self, obj, idx, confirm_delete_row=None, is_editable = False, conditions={}, is_chk_column_enabled=True, handle_on_long_press=None,
                 handle_chk_row_selected=None, get_parent=None, get_children=None, *args, **kwargs):
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
        
        self.chk_column = ft.Checkbox(value= False, width=40, height=40, on_change=lambda e: self.handle_on_change_chk_column(e), data=obj)
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
        self.form = FieldBuilder(obj=obj, layout_mode=LayoutMode.HORIZONTAL, diplay_mode=diplay_mode, get_children=get_children,
                                 conditions=self.conditions, page=self.page, get_parent=get_parent)
        self.controls.append(self.form)
        self.content= ft.Row(controls=self.controls, vertical_alignment=ft.VerticalAlignment.CENTER, spacing=0)
        # Styles of the row
        self.height=SM.get(SK.TABLE_ROW_HEIGHT, None)
     
    def handle_on_change_chk_column(self, e):
        if e.control.value == True:
            self.is_selected = True
        else:
            self.is_selected = False
        self.handle_chk_row_selected(e)
        
    def check_is_selected(self):
        return self.is_selected
    
    def clean_selection(self):
        self.chk_column.value = False
        self.chk_column.update()
    
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
        self.is_selected = value
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
    """
    A generic data table component for displaying, editing, and managing rows of data.
    """
    def __init__(
        self,
        is_chk_column_enabled: bool = True,
        is_editable: bool = False,
        handle_on_long_press: Optional[Callable[[Any], None]] = None,
        handle_on_chk_row_click: Optional[Callable[[ft.ControlEvent], None]] = None,
        on_row_selected: Optional[Callable[[List[Any]], None]] = None,
        on_click_column: Optional[Callable[[ft.ControlEvent], None]] = None,
        conditions: Conditions = Conditions(),
        page: Optional[ft.Page] = None,
        get_parent: Optional[Callable[[], Any]] = None,
        *args,
        **kwargs,
    ):
        """
        Initializes the NotDataTable component.

        Args:
            is_chk_column_enabled (bool): Whether the checkbox column is enabled.
            is_editable (bool): Whether the table is editable.
            handle_on_long_press (Optional[Callable[[Any], None]]): Callback for long press events on rows.
            handle_on_chk_row_click (Optional[Callable[[ft.ControlEvent], None]]): Callback for checkbox row clicks.
            on_row_selected (Optional[Callable[[List[Any]], None]]): Callback for row selection events.
            handle_on_chk_header_click (Optional[Callable[[ft.ControlEvent], None]]): Callback for header checkbox clicks.
            conditions (Conditions): Conditions for filtering and displaying data.
            page (Optional[ft.Page]): The parent page.
            get_parent (Optional[Callable[[], Any]]): Function to get the parent object.
        """
        super().__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        self.expand: bool = True
        self.header: Optional[NotDataTableHeader] = None
        self.page: Optional[ft.Page] = page
        self.rows: List[NotDataRowTable] = []
        self.spacing: int = 0
        self._data: Optional[List[Any]] = None
        self._model: Optional[Any] = None
        self.is_chk_column_enabled: bool = is_chk_column_enabled
        self.is_editable: bool = is_editable
        self.is_being_edited: bool = False
        self.on_row_selected: Optional[Callable[[List[Any]], None]] = on_row_selected
        self.handle_on_long_press: Optional[Callable[[Any], None]] = handle_on_long_press
        self.handle_on_chk_row_click: Optional[Callable[[ft.ControlEvent], None]] = handle_on_chk_row_click
        self.on_click_column: Optional[Callable[[Dict[str, str]], None]] = on_click_column
        self.get_parent: Optional[Callable[[], Any]] = get_parent
        self.conditions: Conditions = conditions

        # Components
        self.dict_order: Dict[str, str] = {}
        self.chk_column: Optional[ft.Checkbox] = None
        self.component_buttons: ft.Container = ft.Container()
        self.component_header: ft.Column = ft.Column(controls=[], spacing=0)
        self.component_body: ft.Column = ft.Column(controls=[], spacing=0)
        self.component_footer: ft.Column = ft.Column(controls=[], spacing=0)
        self.controls: List[ft.Control] = [
            self.component_buttons,
            self.component_header,
            self.component_body,
            self.component_footer,
        ]

        # Buttons for adding and removing rows
        self.btn_add_row: ft.TextButton = self._create_add_row_button()
        self.btn_remove_row: ft.TextButton = self._create_remove_row_button()
       
    def _create_add_row_button(self) -> ft.TextButton:
        """
        Creates the button for adding new rows.

        Returns:
            ft.TextButton: The add row button.
        """
        return ft.TextButton(
            content=ft.Row([ft.Icon(name=ft.Icons.ADD, size=28)]),
            width=40,
            height=40,
            style=ft.ButtonStyle(
                padding=ft.padding.all(5),
                bgcolor=ft.Colors.PRIMARY_CONTAINER,
                shape=ft.RoundedRectangleBorder(radius=3),
            ),
            on_click=lambda e: self.add_row(),
        )
        
    def clean_selection(self):
        for row in self.component_body.controls:
            row.clean_selection()
            
        self.header.clean_selection()
         
    def _create_remove_row_button(self) -> ft.TextButton:
        """
        Creates the button for removing selected rows.

        Returns:
            ft.TextButton: The remove row button.
        """
        return ft.TextButton(
            content=ft.Row([ft.Icon(name=ft.Icons.REMOVE, size=28)]),
            width=40,
            height=40,
            style=ft.ButtonStyle(
                padding=ft.padding.all(5),
                bgcolor=ft.Colors.TERTIARY_CONTAINER,
                shape=ft.RoundedRectangleBorder(radius=3),
            ),
            on_click=lambda e: self.delete_selected_rows(e),
        ) 
        
    def set_data(self, data: List[Any]) -> None:
        """
        Sets the data for the table.

        Args:
            data (List[Any]): The data to display in the table.
        """
        self._data = data

    def set_model(self, model: Any) -> None:
        """
        Sets the model for the table.

        Args:
            model (Any): The model to use for the table.
        """
        self._model = model

        
    def build_header(self) -> None:
        """
        Builds the table header.
        """
        self.header = NotDataTableHeader(
            is_chk_column_enabled=self.is_chk_column_enabled,
            data=self._data,
            model=self._model,
            is_editable=self.is_editable,
            conditions=self.conditions,
            handle_all_row_selected=self.handle_on_click_chk_row,
            on_click_column=self.on_click_column,
        )
        self.header.build_header()
        self.component_header.controls = [self.header]
    
    def build_body(self):
        """
        Builds the table body with rows of data.
        """
        list_data_row = [
            NotDataRowTable(
                obj=obj,
                idx=idx,
                is_editable=self.is_editable,
                conditions=self.conditions,
                handle_on_long_press=self.handle_on_long_press,
                is_chk_column_enabled=self.is_chk_column_enabled,
                handle_chk_row_selected=self.handle_chk_row_selected,
                confirm_delete_row=self.confirm_delete_row,
                get_children=self.get_children,
                get_parent=self.get_parent,
            ) for idx, obj in enumerate(self._data)
        ]
        self.component_body.controls=list_data_row
    
    def build_footer(self):
        """
        Builds the table footer with the button btn_add_row.
        """
        if self.is_editable:
            self.component_footer.controls.append(
                ft.Container(
                    content=self.btn_add_row, 
                    margin=ft.margin.symmetric(horizontal=0, vertical=5)
                )
            )   
            
    def get_children(self):
        return [row.form for row in self.component_body.controls]
    
    def confirm_delete_row(self):
        self.component_body.controls = [row for row in self.component_body.controls if not row.check_is_selected()]
        self.update_body()
        
    def update_body(self):
        self.component_body.update()
        
    def create_table(self):
        self.build_header()
        self.build_body()
        self.build_footer()
        
    def get_selectd_objects(self):
        return [row.obj for row in self.component_body.controls if row.check_is_selected()]
    
    
    def handle_chk_row_selected(self, e):
        list_rows_selected = self.list_rows_selected()
        self.header.manage_chk_header(len(list_rows_selected), len(self.component_body.controls))
    
        if self.on_row_selected:
            self.on_row_selected(list_rows_selected)
            
        e.control.update()
        
    def list_rows_selected(self):
        return [row.obj for row in self.component_body.controls if row.check_is_selected()]
        
    def handle_on_click_chk_row(self, e):
        if e.control.value == None:
            e.control.value = False
            e.control.update()
        
        for row in self.component_body.controls:
            row.set_value_chk_row(e.control.value)
            
                
        list_rows_selected = self.list_rows_selected()
        if self.on_row_selected:
            self.on_row_selected(list_rows_selected)
        
    def add_row(self):
        """
        Adds a new row to the table.
        """
        idx = len(self.component_body.controls)
        new_row = NotDataRowTable(
            self._model(), 
            idx, 
            is_editable=self.is_editable, 
            conditions=self.conditions, 
            handle_on_long_press=self.handle_on_long_press, 
            is_chk_column_enabled=self.is_chk_column_enabled,
            handle_chk_row_selected=self.handle_chk_row_selected,
            confirm_delete_row=self.confirm_delete_row,
            get_children=self.get_children,
            get_parent=self.get_parent
        )
        self.component_body.controls.append(new_row)
        self.update_body()
    
    def save(self, **kwargs):
        """
        Saves all rows in the table.

        Returns:
            bool: True if all rows were saved successfully, False otherwise.
        """
        return all(row.save(**kwargs) for row in self.component_body.controls)
    
    def check_is_dirty(self):
        """
        Checks if any row in the table has unsaved changes.

        Returns:
            bool: True if there are unsaved changes, False otherwise.
        """
        return any(row.check_is_dirty() for row in self.component_body.controls)