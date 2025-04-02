import flet as ft
from components.custom_buttons import CustomButtonCupertino, CustomIconButton
from components.custom_input import LayoutMode
from components.field_builder import FieldBuilder
from components.custom_dialogs import DlgConfirm, DlgAlert
from components.not_data_table import NotDataTable
from pages.conditions import Conditions
from django.db import transaction





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
        self.btn_save = CustomIconButton(icon=ft.Icons.SAVE, on_click=lambda e: self.handle_btn_save(), bgcolor=ft.Colors.PRIMARY_CONTAINER)
        self.btn_exit = CustomButtonCupertino("Salir", ft.Icons.CLOSE, lambda e: self.handle_btn_exit(), ft.Colors.SECONDARY_CONTAINER, ft.Colors.ON_SURFACE)
        self.related_tables = []
        self.container_buttons = ft.Container(
            content=ft.Row([
                    self.btn_save,
                    self.btn_exit,
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
        
        
    def handle_btn_save(self):
        try:
            with transaction.atomic():  # Inicia un bloque transaccional
                # Guardar el objeto padre
                is_save_correctly = self.form.save()
                if not is_save_correctly:
                    raise Exception("Error al guardar el objeto padre.")
    
                # Actualizar el objeto padre después de guardar
                self.obj = self.form.obj
    
                # Guardar los objetos relacionados (hijos)
                for related_table in self.related_tables:
                    related_table.parent_obj = self.obj  # Asociar el objeto padre
                    is_save_correctly = related_table.save(parent_obj=self.obj, parent_field_name=self.obj._meta.model_name)
                    if not is_save_correctly:
                        raise Exception("Error al guardar los objetos relacionados.")
    
            # Si todo se guarda correctamente, mostrar un mensaje de éxito
            DlgAlert(page=self.page, title="Registro guardado correctamente")
            # self.page.custom_go(self.params["origin"], self.params["returns_params"] if "returns_params" in self.params else {})
    
        except Exception as e:
            # Manejar errores y mostrar un mensaje al usuario
            DlgAlert(page=self.page, title=f"Error al guardar: {str(e)}")
        
    def build_page(self):
        if '_obj' in self.params:
            self.obj = self.params['_obj']
        else:
            self.obj = self._model()
            
        # obj = self.obj if self.obj else self._model()
        
        self.form: FieldBuilder = FieldBuilder(self.obj, layout_mode=LayoutMode.HORIZONTAL_WRAP, conditions = self.conditions, page=self.page)
    
        related_objects = self.get_related_objects(self.obj)
        
        # Crear tablas para objetos relacionados
        self.related_tables = []
        for related_name, related_queryset in related_objects.items():
            ro_conditions = Conditions()
            ro_conditions.init_from_dict(self.conditions.related_objects.get(related_name, {}))
            related_table = NotDataTable(is_chk_column_enabled=False, is_editable=True, conditions=ro_conditions, 
                                         page=self.page, get_parent=self.get_parent)
            related_table.set_model(related_queryset.model)
            related_table.set_data(related_queryset)
            related_table.create_table()
            self.related_tables.append(related_table)
        
        principal_column = ft.Column(controls=[
            self.container_header,
            ft.Divider(),
            self.form,
            ft.Divider(),
            *self.related_tables,
            ft.Divider(),
        ])
        
        self.content= principal_column
        # self.update()
        
    def get_parent(self):
        return self.form, self.obj
    
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
    
    def handle_btn_exit(self):
        is_dirty = self.form.check_is_dirty()
        if not is_dirty:
            for related_table in self.related_tables:
                if related_table.check_is_dirty():
                    is_dirty = True
                    break
        # validar si se modificó
        if is_dirty:
            # Si se modificó, preguntar si desea salir sin guardar
            DlgConfirm(page=self.page,title="Desea salir sin guardar?", fn_yes=self.confirm_exit)
        else:
            self.page.custom_go(self.params["origin"], self.params["returns_params"] if "returns_params" in self.params else {})

    def confirm_exit(self):
        self.page.custom_go(self.params["origin"], self.params["returns_params"] if "returns_params" in self.params else {})