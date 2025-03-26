import flet as ft
from components.custom_buttons import CustomButtonCupertino
from components.custom_input import LayoutMode
from components.field_builder import FieldBuilder
from components.custom_dialogs import DlgConfirm, DlgAlert
from components.not_data_table import NotDataTable
from pages.conditions import Conditions





class GenericHeaderDetailForm(ft.Container):
    def __init__(self, page: ft.Page, _model, fn_acept= None, fn_cancel=None, _obj = None, params = {}, conditions = Conditions()):
        super().__init__()
        self._model = _model
        self.content = None
        self.page = page
        self.fn_acept = fn_acept
        self.fn_cancel = fn_cancel
        self.obj = _obj
        self.params = params
        
        self.conditions = conditions
        self.btn_aceptar = CustomButtonCupertino("Aceptar", "save", lambda e: self.handle_btn_acepta(), ft.Colors.PRIMARY, ft.Colors.ON_PRIMARY)
        self.btn_cancelar = CustomButtonCupertino("Cancelar", "cancel", lambda e: self.handle_btn_cancelar(), ft.Colors.SECONDARY_CONTAINER, ft.Colors.ON_SURFACE)
        self.container_buttons = ft.Container(
            content=ft.Row([
                    self.btn_cancelar,
                    self.btn_aceptar,
                ],
                alignment=ft.MainAxisAlignment.END,
            ),
            # padding=ft.padding.symmetric(horizontal=10, vertical=10),
        )
        self.txt_page_title = ft.Text(f"{"Editar" if self.obj else "Agregar" } {self._model._meta.object_name}", size=18)
        self.container_header = ft.Container(
            content=ft.Row([self.txt_page_title, self.container_buttons], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        )
        
        self.build_page()
        
    def handle_btn_aceptar(self, e: ft.ControlEvent):
        pass
    
    def handle_btn_cancelar(self, e: ft.ControlEvent):
        pass
    
    def build_page(self):
        if '_obj' in self.params:
            self.obj = self.params['_obj']
        else:
            self.obj = self._model()
            
        obj = self.obj if self.obj else self._model()
        
        self.form = FieldBuilder(obj, layout_mode=LayoutMode.HORIZONTAL_WRAP, conditions = self.conditions, page=self.page)
        # self.form.create_fields()
        # self.form.update_controls()
        
        related_objects = self.get_related_objects(obj)
        
        # Crear tablas para objetos relacionados
        related_tables = []
        for related_name, related_queryset in related_objects.items():
            ro_conditions = Conditions()
            ro_conditions.init_from_dict(self.conditions.related_objects.get(related_name, {}))
            related_table = NotDataTable(is_chk_column_enabled=False, is_editable=True, conditions=ro_conditions, page=self.page)
            related_table.set_model(related_queryset.model)
            related_table.set_data(related_queryset)
            related_table.create_table()
            related_tables.append(ft.Column(controls=[related_table]))
        
        principal_column = ft.Column(controls=[
            self.container_header,
            ft.Divider(),
            self.form,
            ft.Divider(),
            *related_tables,
            ft.Divider(),
            ft.Text("Resumen")
        ])
        
        self.content= principal_column
        # self.update()
    
    def get_related_objects(self, obj):
        related_objects = {}
        if obj.pk:  # Verificar si el objeto tiene una clave primaria
            for relation in obj._meta.related_objects:
                related_name = relation.get_accessor_name()
                related_manager = getattr(obj, related_name)
                related_objects[related_name] = related_manager.all()
        else:
            for relation in obj._meta.related_objects:
                related_name = relation.get_accessor_name()
                related_objects[related_name] = relation.related_model.objects.none()   # Devolver una lista vacía para cada relación
        return related_objects
    
    def btn_aceptar(self):
        
        is_save_correctly = self.form.save()
        if is_save_correctly:
            DlgAlert(page=self.page, title="Registo guardado correctamente")
            self.page.custom_go(self.params["origin"], self.params["returns_params"] if "returns_params" in self.params else {})
     
        
    def btn_cancelar(self):
        # validar si se modificó
        if not self.form.validate_form_change():
            DlgConfirm(page=self.page,title="Desea salir sin guardar?", fn_yes=self.confirma_salir)
        else:
            self.page.custom_go(self.params["origin"], self.params["returns_params"] if "returns_params" in self.params else {})

    def confirma_salir(self):
        self.page.custom_go(self.params["origin"], self.params["returns_params"] if "returns_params" in self.params else {})