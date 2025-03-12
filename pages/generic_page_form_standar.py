import flet as ft
from components.custom_standard_form import Form
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
        
        self.form = Form(obj)
        self.form.create_fields()
        self.form.create_button(
            nombre="Cancelar", 
            fn=self.btn_cancelar,
            bgcolor=ft.Colors.SECONDARY, 
            color=ft.Colors.ON_SECONDARY
        )
        self.form.create_button(
            nombre="Aceptar", 
            fn=self.btn_aceptar
        )
        self.form.update_controls()
        
        titulo = f"{  "Editar" if self.obj else "Agregar" } {self._model._meta.object_name}"
        
        contenedor = ft.Column(controls=[
            ft.Text(titulo,  size=18),
            ft.Divider(height=5),
            self.form
        ])
        
        self.content= contenedor
        # self.update()
    
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