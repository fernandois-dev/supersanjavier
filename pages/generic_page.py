from typing import List, Dict, Optional, Any
import flet as ft
from components.custom_buttons import CustomButtonCupertino
from components.not_data_table import NotDataTable
from data.serach import buscar_modelo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from components.custom_dialogs import DlgConfirm
from pages.conditions import Conditions
from django.db.models import ProtectedError, RestrictedError

class GenericPage(ft.Column):
    """
    Clase genérica para manejar páginas con tablas, paginación y acciones CRUD.
    """
    
    def __init__(self, page: ft.Page, _model, params = {}, conditions = Conditions()):
        """
        Inicializa la página genérica.

        Args:
            page (ft.Page): Página principal de Flet.
            _model (Any): Modelo de Django asociado a la tabla.
            params (Optional[Dict]): Parámetros iniciales para la página.
            conditions (Conditions): Condiciones para el despliegue de datos para la tabla y los filtros.
        """
        super().__init__()
        self.expand: bool = True
        self.spacing: int = 0
        self.params: Dict = params or {}
        self._model: Any = _model
        self.conditions: Conditions = conditions

        # Componentes principales
        self.table: NotDataTable = self._create_table()
        self.page: ft.Page = page
        self.search_active: bool = False
        self.items_selected: int = 0
        self.titulo: str = self._model._meta.object_name
        self.dict_order: Dict[str, str] = {}
        self.text_search: str = ""
        self.text_order: str = ""

        # Paginación
        self.component_pagination: Optional[ft.Row] = None
        self.current_page: int = 1
        self.items_per_page: int = 10
        self.paginator: Optional[Paginator] = None
        self.build_pagination()

        # Componentes de búsqueda
        self.component_search_input: Optional[ft.TextField] = None
        self.component_search_cancel: Optional[ft.TextButton] = None
        self.build_search_cancel()
        self.component_search: Optional[ft.Row] = None

        # Botones y acciones
        self.component_left_buttons: Optional[ft.Row] = None
        self.build_left_buttons()
        self.component_actions: Optional[ft.Row] = None
        self.build_actions()

        # Construir búsqueda
        self.build_search_input()
        self.build_search()

        # Menú de la tabla
        self.menu_table: ft.Row = ft.Row(
            height=40,
            controls=[
                self.component_left_buttons,
                self.component_search,
                self.component_pagination,
            ],
        )
        
    def _create_table(self) -> NotDataTable:
        """
        Crea y configura la tabla principal.

        Returns:
            NotDataTable: Tabla configurada.
        """
        return NotDataTable(
            handle_on_long_press=self.display_form,
            on_row_selected=self.handle_on_row_selected,
            on_click_column=self.set_dict_order,
            conditions=self.conditions,
        )
        
    def build_page(self):
        if "text_order" in self.params:
            self.text_order = self.params["text_order"]
        if "search_filter" in self.params:
            self.text_search = self.params["search_filter"]
            self.component_search_input.value = self.text_search
            if self.text_order == "":
                productos_filtrados = buscar_modelo(self._model.objects.all(), self.text_search)      
            else:
                productos_filtrados = buscar_modelo(self._model.objects.all().order_by(self.text_order), self.text_search)
            self.paginator = Paginator(productos_filtrados, self.items_per_page)  
            
        else:
            # self._data = self._model.objects.all()  #Database call
            if self.text_order == "":
                self.paginator = Paginator(self._model.objects.all(), self.items_per_page)
            else:
                self.paginator = Paginator(self._model.objects.all().order_by(self.text_order), self.items_per_page)
            
        self.load_page_data()
        self.table.set_model(self._model)
        self.table.create_table()
        self.display_main()
        

    
    def load_page_data(self):
        try:
            page_obj = self.paginator.page(self.current_page)
            data_page = page_obj.object_list
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            data_page = self.paginator.page(1).object_list
            self.current_page = 1
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            data_page = self.paginator.page(self.paginator.num_pages).object_list
            self.current_page = self.paginator.num_pages

        self.table.set_data(data_page)
        self.update_pagination_controls()
    
    def display_main(self):
        self.menu_table.controls = [
            self.component_left_buttons,
            self.component_search,
            self.component_pagination,
        ]
        self.table.build_body()
        self.controls = [
            ft.Container(content=self.menu_table, margin=ft.margin.only(10, 5, 10, 15)) , 
            ft.Row(spacing=0, controls=[self.table], expand=True, vertical_alignment=ft.CrossAxisAlignment.START)
        ]
   
    def build_actions(self, count=0, list_objs = []):
        
        row_acciones = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
        #################################################
        ########### BOTON EDITAR ########################
        #################################################
        row_acciones.controls.append(
            ft.Row(height=40, vertical_alignment=ft.MainAxisAlignment.END, controls=[
                ft.Container(
                    content=ft.Row(controls=[
                        ft.Text(f"{count} seleccionados"),
                        ft.TextButton(
                            icon=ft.Icons.CANCEL,
                            width=30,
                            style=ft.ButtonStyle(padding=ft.padding.all(5)),
                            on_click= lambda e: self.cancel_selection()
                        ),
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.END
                                   ),
                    alignment=ft.alignment.center_right,
                    width=160,
                    height=40,
                    bgcolor=ft.Colors.PRIMARY_CONTAINER,
                    border_radius=ft.border_radius.all(3),
                    border=ft.border.all(1, ft.Colors.ON_SECONDARY_CONTAINER),
                )])
        )
        
        if count == 1:
            obj = list_objs[0]
            row_acciones.controls.append(CustomButtonCupertino(text="Editar", icon_name=ft.Icons.EDIT, on_click= lambda e: self.display_form(obj)))
         
        
        #################################################
        ########### MENU DE ACCIONES ####################
        #################################################
        items_accion = []
        items_accion.append(ft.MenuItemButton(
            content=ft.Text("Eliminar"),
            leading=ft.Icon(ft.Icons.DELETE),
            on_click= lambda e: self.handle_delete(),
        ))
        items_accion.append(ft.MenuItemButton(
            content=ft.Text("Desactivar"),
            leading=ft.Icon(ft.Icons.CANCEL),
        ))
        
        menu_controls = [ft.SubmenuButton(
            content=ft.Text("Acciones", color=ft.Colors.ON_SURFACE, size=15, font_family="Roboto Mono"),
            leading=ft.Icon(ft.Icons.MENU, color=ft.Colors.ON_SURFACE),
            controls=items_accion,
        ),]
        
        row_acciones.controls.append(ft.Row(expand=3, alignment=ft.MainAxisAlignment.CENTER,
            controls=[
            ft.MenuBar(
                expand=True,
                style=ft.MenuStyle(
                    alignment=ft.alignment.top_left,
                    bgcolor=ft.Colors.ON_SECONDARY,
                    shadow_color=ft.Colors.ON_SECONDARY,
                    elevation= False,
                    mouse_cursor={
                        ft.ControlState.HOVERED: ft.MouseCursor.WAIT,
                        ft.ControlState.DEFAULT: ft.MouseCursor.ZOOM_OUT,
                    },
                ),
                controls= menu_controls
            )
        ]))
        
        self.component_actions = row_acciones
    
    def build_left_buttons(self):
        self.component_left_buttons = ft.Row(expand=1, controls=[
                ft.CupertinoFilledButton(
                    content=ft.Text("Nuevo"),
                    height=40,
                    padding=ft.padding.symmetric(horizontal=10),
                    on_click= lambda e: self.display_form()
                ),
                ft.Text(self.titulo , size=18, font_family="Roboto", weight=ft.FontWeight.W_400)
            ])
    
    def build_pagination(self) -> None:
        """
        Construye los controles de paginación.
        """
        self.lbl_page_info = ft.Container(
            content=ft.Text("", color=ft.Colors.ON_SURFACE, size=13, font_family="Roboto Mono"),
            padding=ft.padding.symmetric(horizontal=6),
        )
        self.btn_previous = ft.TextButton(
            content=ft.Row([ft.Icon(name=ft.Icons.CHEVRON_LEFT, size=28)]),
            width=40,
            height=40,
            style=ft.ButtonStyle(
                padding=ft.padding.all(5),
                bgcolor=ft.Colors.PRIMARY_CONTAINER,
                shape=ft.RoundedRectangleBorder(radius=3),
            ),
            on_click=lambda e: self.previous_page(),
        )
        self.btn_next = ft.TextButton(
            content=ft.Row([ft.Icon(name=ft.Icons.CHEVRON_RIGHT, size=28)]),
            width=40,
            height=40,
            style=ft.ButtonStyle(
                padding=ft.padding.all(5),
                bgcolor=ft.Colors.PRIMARY_CONTAINER,
                shape=ft.RoundedRectangleBorder(radius=3),
            ),
            on_click=lambda e: self.next_page(),
        )
        self.component_pagination = ft.Row(
            expand=2,
            spacing=1,
            alignment=ft.MainAxisAlignment.END,
            controls=[
                self.lbl_page_info,
                self.btn_previous,
                self.btn_next,
                ft.IconButton(
                    icon=ft.Icons.REFRESH,
                    icon_size=20,
                    tooltip="Recargar Datos",
                    on_click=lambda e: self.search(),
                ),
            ],
        )
    
    def update_pagination_controls(self):
        if self.paginator is not None:
          total_items = self.paginator.count
          total_pages = self.paginator.num_pages

          start_index = (self.current_page - 1) * self.items_per_page + 1
          end_index = min(self.current_page * self.items_per_page, total_items)

          self.lbl_page_info.content.value = f"{start_index}-{end_index}/{total_items}"
          self.btn_previous.disabled = self.current_page == 1
          self.btn_next.disabled = self.current_page == total_pages
          

    def next_page(self):
        if self.current_page < self.paginator.num_pages:
            self.current_page += 1
            self.load_page_data()
            self.table.build_body()
            self.update()

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_page_data()
            self.table.build_body()
            self.update()


    def build_search_input(self):
        self.component_search_input = ft.TextField(
            label="Busqueda",
            height=35,
            icon=ft.Icons.SEARCH,
            text_style=ft.TextStyle(size=14),
            border_color="#ababab",
            on_submit= lambda e: self.set_text_search(e.data)
        )
    
    def build_search_cancel(self, show_close=False):
        self.component_search_cancel = ft.TextButton(
                content=ft.Row([
                    ft.Icon(name=ft.Icons.CANCEL, size=20, color=ft.Colors.TERTIARY),
                ]),
                width=32,
                height=32,
                style=ft.ButtonStyle(padding=ft.padding.all(5)),
                on_click= lambda e: self.cancel_search(),
                visible=show_close
            )
        
    def build_search(self):
        self.component_search = ft.Row(expand=3, alignment=ft.MainAxisAlignment.CENTER, controls=[
            self.component_search_input,
            self.component_search_cancel,
        ])
        
    def cancel_search(self):
        self.text_search = ""
        self.search()
        self.component_search_input.value = ""
        self.component_search_input.update()
    
    def set_dict_order(self, dict_order):
        self.dict_order = dict_order
        self.search()
     
    def set_text_search(self, value):
        self.text_search = value
        self.search()
        
    def search(self):
        if self.text_search == "":
            self.search_active = False
        else:
            self.search_active = True
        
        self.component_search_cancel.visible = True if self.text_search else False
        # self.component_search_cancel.update()
        self.component_search.update()
        
        self.text_order = ""
        for clave in self.dict_order:
            if self.dict_order[clave] == "asc":
                self.text_order = f"{clave}"
            else:
                self.text_order = f"-{clave}"
                
        if(self.text_order == ""):
            productos_filtrados = buscar_modelo(self._model.objects.all(), self.text_search)      
        else:
            productos_filtrados = buscar_modelo(self._model.objects.all().order_by(self.text_order), self.text_search)
        self.paginator = Paginator(productos_filtrados, self.items_per_page)
        self.current_page = 1
        self.load_page_data()
        self.table.build_body()
        self.update()
        self.table.update()
        
    def set_data(self, data):
        self._data = data
      
    def load_data_table(self):
        self.table.fill_data_table()
    
    def set_actions_menu(self, list_objs):
        
        self.build_actions(count=len(list_objs), list_objs=list_objs)
        
        self.menu_table.controls = [
            self.component_left_buttons,
            self.component_actions,
            self.component_pagination,
        ]
        self.menu_table.update()
        
    def cancel_selection(self):
        self.table.clean_selection()
        self.set_search_menu()
    
    def set_search_menu(self):
        self.menu_table.controls = [
            self.component_left_buttons,
            self.component_search,
            self.component_pagination,
        ]
        self.menu_table.update()
    
    def handle_on_row_selected(self, list_obj):  
        if len(list_obj) > 0:
            self.set_actions_menu(list_obj)
        else:
            self.set_search_menu()
            
    
    def btn_cancelar_dlg_si(self):
        self.page.close(self.dlg_alert)
        self.display_main()
        self.update()

    def btn_cancelar_dlg_no(self):
        self.page.close(self.dlg_alert)
             
    def handle_delete(self):
        DlgConfirm(page=self.page, title="Desea eliminar los registros?", fn_yes=self.handle_delete_yes)
    
    def handle_delete_yes(self):
        """
        Maneja la confirmación de eliminación de registros seleccionados.
        """
        for obj in self.table.get_selectd_objects():
            try:
                obj.delete()
            except ProtectedError as e:
                relaciones = self.obtener_relaciones(obj)
                self.dlg_msg = ft.AlertDialog(
                    title=ft.Text(f"No se puede eliminar {str(obj)}."),
                    content=ft.Text(f"Registros relacionados: {relaciones}"),
                )
                self.page.open(self.dlg_msg)
            except RestrictedError as e:
                self.dlg_msg = ft.AlertDialog(
                    title=ft.Text(f"Error al eliminar {str(obj)}."),
                    content=ft.Text(f"Detalles del error: {str(e)}"),
                )
                self.page.open(self.dlg_msg)    
        self.set_search_menu()
        self.search()
            
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
    
    def display_form(self, _obj = None):
        params = {}
        params["returns_params"] = {}
        if self.text_search:
            params["returns_params"]["search_filter"] = self.text_search
        if self.text_order:
            params["returns_params"]["text_order"] = self.text_order
            
        if _obj:
            params["_obj"] = _obj
            self.page.custom_go(f"{self.page.route}/form?origin={self.page.route}?id={_obj.id}", params=params)
        else:
            self.page.custom_go(f"{self.page.route}/form?origin={self.page.route}", params=params)
    