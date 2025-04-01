import flet as ft
from components.custom_buttons import CustomButtonCupertino
from components.custom_input import DisplayMode
from components.field_builder import FieldBuilder
from components.custom_dialogs import DlgConfirm, DlgAlert




class GenericPageFormStandar(ft.Container):
    def __init__(self, page: ft.Page, _model, fn_acept= None, fn_cancel=None, _obj = None, params = {}):
        super().__init__()
        self._model = _model
        self.content = None
        self.page = page
        self.fn_acept = fn_acept
        self.fn_cancel = fn_cancel
        self.obj = _obj
        self.params = params
        self.build_page()
    
    def build_page(self):
        if '_obj' in self.params:
            self.obj = self.params['_obj']
        else:
            self.obj = self._model()
            
        obj = self.obj if self.obj else self._model()
        
        self.form = FieldBuilder(obj, diplay_mode=DisplayMode.EDIT)
        self.btn_aceptar = CustomButtonCupertino("Aceptar", "save", lambda e: self.handle_btn_aceptar(), ft.Colors.PRIMARY, ft.Colors.ON_PRIMARY)
        self.btn_cancelar = CustomButtonCupertino("Cancelar", "cancel", lambda e: self.handle_btn_cancelar(), ft.Colors.SECONDARY_CONTAINER, ft.Colors.ON_SURFACE)
        self.container_buttons = ft.Container(
            content=ft.Row([
                    self.btn_cancelar,
                    self.btn_aceptar,
                ],
                alignment=ft.MainAxisAlignment.END,
                width=350,
            ),
        )
        
        titulo = f"{  "Editar" if self.obj else "Agregar" } {self._model._meta.object_name}"
        
        contenedor = ft.Column(controls=[
            ft.Text(titulo,  size=18),
            ft.Divider(height=5),
            self.form,
            self.container_buttons
        ])
        
        self.content= contenedor
        # self.update()
    
    def handle_btn_aceptar(self):
        
        is_save_correctly = self.form.save()
        if is_save_correctly:
            DlgAlert(page=self.page, title="Registo guardado correctamente")
            self.page.custom_go(self.params["origin"], self.params["returns_params"] if "returns_params" in self.params else {})
     
        
    def handle_btn_cancelar(self):
        # validar si se modificó
        if self.form.check_is_dirty():
            DlgConfirm(page=self.page,title="Desea salir sin guardar?", fn_yes=self.confirma_salir)
        else:
            self.page.custom_go(self.params["origin"], self.params["returns_params"] if "returns_params" in self.params else {})

    def confirma_salir(self):
        self.page.custom_go(self.params["origin"], self.params["returns_params"] if "returns_params" in self.params else {})