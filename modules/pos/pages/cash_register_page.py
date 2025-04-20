import copy
import flet as ft
from components.custom_dialogs import DlgAlert
from modules.ventas.models import DetalleVenta, Venta
from components.custom_buttons import CustomButtonCupertino, CustomIconButton
from components.custom_input import CustomIntegerField, CustomMoneyField, CustomMoneyView, DisplayMode, LayoutMode, ManagerField, SearchField
from components.field_builder import FieldBuilder
from components.not_data_table import NotDataTable
from pages.conditions import Conditions
from utilities.utilities import num_or_zero, to_number_or_zero
from django.db import transaction
from django.core.exceptions import ValidationError




class CashRegisterPage(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.on_keyboard_event = self.handle_keypress
        
        self.add_button = CustomIconButton(
            icon=ft.icons.ADD_CIRCLE_OUTLINE,
            tooltip="Agregar",
            on_click=lambda e: self.handle_btn_add(),
            bgcolor=ft.Colors.PRIMARY_CONTAINER,
            icon_color=ft.Colors.ON_PRIMARY_CONTAINER,
        )
            
        conditions = Conditions(
            fields_excluded=["id", "venta"],
            
        )
        
        
        # Resumen inicial
        self.subtotal = 0
        self.descuento = 0
        self.total = 0
        
        self.txt_subtotal = CustomMoneyView(value=self.subtotal)
        self.txt_descuento = CustomMoneyView(value=self.descuento)
        self.txt_total = CustomMoneyView(value=self.total, size=20)
        
        self.btn_pagar = CustomButtonCupertino(
            text="F12 Pagar",
            icon=ft.icons.PAYMENT,
            on_click=self.generate_payment,
            bgcolor=ft.Colors.PRIMARY_CONTAINER,
            color=ft.Colors.ON_PRIMARY_CONTAINER,
        )
        self.btn_reset = CustomButtonCupertino(
            text="F7 Limpiar",
            icon=ft.icons.CANCEL,
            on_click=lambda e: self.clean_fields(),
            bgcolor=ft.Colors.TERTIARY_CONTAINER,
            color=ft.Colors.ON_PRIMARY_CONTAINER,
        )
        
        # Contenedor del resumen
        self.build_table_resumen()
        self.resume_container = ft.Column(
            controls=[
                ft.Text("Resumen", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.ON_BACKGROUND),
                self.table_resumen,
                ft.Divider(height=1),
                ft.Divider(height=1),
                ft.Container(
                    ft.Row(
                        controls=[
                            self.btn_reset,
                            self.btn_pagar,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        expand=True,
                    ),
                    padding=ft.Padding(0, 10, 0, 0),
                )
            ],
            spacing=10,
            width=300,
        )
        
        self.detalles_venta = []
        
        self.new_obj = DetalleVenta()
        
        self.mode = "short"
        
        self.table = NotDataTable(is_chk_column_enabled=False, is_editable=False, page=self.page, conditions=conditions)
        self.table.set_model(self.new_obj)
        self.table.set_data([])
        self.table.create_table()
        
        for field in self.new_obj._meta.fields:
            if field.name == "producto":
                self.orm_field_producto = field
            if field.name == "cantidad":
                self.orm_field_cantidad = field
            if field.name == "precio":
                self.orm_field_precio = field
            if field.name == "descuento":
                self.orm_field_descuento = field
            if field.name == "total":
                self.orm_field_total = field
                
                
        
        self.container_fields = ft.Container()        
        # self.build_row_fields_large()
        self.build_row_fields_short()
        self.content = ft.Column(
            controls=[
                self.container_fields,
                ft.Row(
                    controls=[
                        self.table,
                        self.resume_container,
                    ],
                    expand=True,
                    vertical_alignment = ft.CrossAxisAlignment.START
                ),  
            ],
        )
        try:
            self.set_short_mode()
        except Exception as e:
            pass
    def build_table_resumen(self):
        self.table_resumen = ft.DataTable(
            columns=[ft.DataColumn(ft.Text("")),ft.DataColumn(ft.Text(""))],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Subtotal:", size=16, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(self.txt_subtotal),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Descuento:", size=16, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(self.txt_descuento),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Total:", size=16, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(self.txt_total),
                    ],
                ),
            ],
            width=300,
        )
        
    def update_resume(self):
        """Actualiza el resumen con el total y el descuento."""
        self.subtotal = sum(item.precio * item.cantidad for item in self.detalles_venta)
        self.descuento = sum(item.descuento for item in self.detalles_venta)
        self.total = sum(item.total for item in self.detalles_venta)
        
        self.txt_subtotal.value = self.subtotal
        self.txt_descuento.value = self.descuento
        self.txt_total.value = self.total
        
        # Actualizar los textos en el resumen
        self.txt_descuento.update()
        self.txt_subtotal.update()
        self.txt_total.update()

    def generate_payment(self, e):
        """Lógica para generar el pago."""
        print(f"Generando pago por un total de ${self.total:.2f} con un descuento de ${self.descuento:.2f}")
        
        #si page.caja no existe no se ejecuta el pago
        if not self.page.caja:
            DlgAlert(self.page, title="Caja no establecida, favor configurar y reiniciar la aplicación")
            return
        
        if self.total > 0:
            with transaction.atomic():
            # Delete all existing products before synchronization
                try:
                    # se crea el objeto de venta
                    venta = Venta()
                    venta.caja = self.page.caja
                    venta.total = self.total
                    venta.state = "CR"
                    venta.full_clean()
                    venta.save()
                    
                    #se recorre la lista de detalles de venta y se guardan
                    for detalle in self.detalles_venta:
                        detalle.venta = venta
                        detalle.full_clean()
                        detalle.save()
                        
                    # se imprime la boleta
                    self.print_boleta()
                    
                    # se limpia la tabla y los campos
                    self.clean_fields()
                    
                    self.table.set_data([])
                    self.update_resume()
                    
                
                except ValidationError as ex:
                    DlgAlert(self.page, title="Error", content=str(ex))
                       
    def print_boleta(self):
        """Lógica para imprimir la boleta en pdf"""
        DlgAlert(self.page, title="Imprimiendo boleta")
        pass
        
    def build_row_fields_large(self):
        self.mode = "large"
        self.field_producto_large = SearchField(
            label="Producto",
            name="producto",
            field=self.orm_field_producto,
            value=None,
            on_change=self.on_change_producto_large,
            page=self.page,
            width=450,
        )
        self.field_producto_large.text_field.autofocus = True
        self.field_cantidad = CustomMoneyField(
            label="Producto",
            field=self.orm_field_cantidad,
            value=None,
            on_change=self.on_change_cantidad,
            width=150,
        )
        self.field_precio = CustomMoneyField(
            label="Producto",
            field=self.orm_field_precio,
            value=None,
            on_change=self.on_change_precio,
            width=200,
            disabled=True,
            color=ft.colors.ON_BACKGROUND,
        )
        self.field_precio.read_only = True
        self.field_descuento = CustomMoneyField(
            label="Descuento",
            field=self.orm_field_descuento,
            value=0,
            on_change=self.on_change_descuento,
            on_submit=self.on_submit_descuento,
            width=200,
        )
        self.field_total = CustomMoneyField(
            label="Total",
            field=self.orm_field_total,
            value=0,
            width=200,
            disabled=True,
            color=ft.colors.ON_BACKGROUND,
        )
        
        self.row_fields_large = ft.Container(
            ft.Row(controls=[ self.field_producto_large,self.field_cantidad, self.field_precio,self.field_descuento, self.field_total, self.add_button]),
            border=ft.Border(bottom = ft.BorderSide(width=4, color=ft.colors.TERTIARY)),
            padding=ft.Padding(0, 0, 0, 8),
            expand=True,
            )
        self.container_fields.content = self.row_fields_large
    
    def build_row_fields_short(self):
        self.mode = "short"
        self.field_producto_short = SearchField(
            label="Producto",
            name="producto",
            field=self.orm_field_producto,
            value=None,
            on_change=self.on_change_producto_short,
            page=self.page,
            width=450,
        )
        self.field_producto_short.text_field.autofocus = True
        self.row_fields_short = ft.Container(
            ft.Row(controls=[ self.field_producto_short]),
            border=ft.Border(bottom = ft.BorderSide(width=4, color=ft.colors.PRIMARY_CONTAINER)),
            padding=ft.Padding(0, 0, 0, 8),
            )
        self.container_fields.content = self.row_fields_short
        
    def handle_keypress(self, e: ft.KeyboardEvent):
        """
        Handles keypress events to toggle between field layouts.
        """
        
        if type(self).__name__ == "CashRegisterPage":
            if e.key == "F1":
                self.close_dialog()
                self.build_row_fields_short()
            elif e.key == "F2":
                self.close_dialog()
                self.build_row_fields_large()
            # elif e.key == "F12":
            #     self.generate_payment(e)
            elif e.key == "F7":
                self.clean_fields()
            elif e.key == "F8":
                # go to config page
                self.page.on_keyboard_event = None
                self.page.go("/config")
        
            self.container_fields.update()
        
    def close_dialog(self):
        to_remove = []
        """Close the dialog and reset the form."""
        for overlay in self.page.overlay:
                # eliminar el dialogo de la pagina
                if isinstance(overlay, ft.AlertDialog):
                    self.page.close(overlay)
                    
                
        
        # self.page.overlay = []
        self.page.update()
            
    def set_short_mode(self):
        self.mode = "short"
        self.row_fields_large.visible = False
        self.row_fields_large.update()
        self.row_fields_short.visible = True
        self.row_fields_short.update()
        self.clean_fields_short()
        self.field_producto_short.focus()
        
    def set_large_mode(self):
        self.mode = "large"
        self.row_fields_short.visible = False
        self.row_fields_short.update()
        self.row_fields_large.visible = True
        self.row_fields_large.update()
        self.clean_fields_large()
        self.field_producto_large.focus()
        self.field_producto_large.update()
    
    def on_change_producto_short(self, e, value=None):
        if value:
            self.new_obj.producto = value
            self.new_obj.precio = value.precio_venta
            self.new_obj.cantidad = 1
            self.new_obj.descuento = 0
            self.new_obj.total = value.precio_venta
            self.add_to_table()
      
    def on_change_producto_large(self, e, value=None):
        
        if value:
            # Buscar producto en detalles_venta
            for register in self.detalles_venta:
                if register.producto == value:
                    self.field_cantidad.value = register.cantidad
                    self.field_precio.value = register.precio
                    self.field_descuento.value = register.descuento
                    self.field_total.value = register.total
                    self.new_obj.producto = register.producto
                    self.new_obj.precio = register.precio
                    self.new_obj.cantidad = register.cantidad
                    self.new_obj.descuento = register.descuento
                    self.new_obj.total = register.total
                    break
            else:
                # Si no se encuentra, asignar valores por defecto
                self.field_cantidad.value = 1
                self.field_precio.value = value.precio_venta
                self.field_descuento.value = 0
                self.field_total.value = value.precio_venta
                self.new_obj.producto = value
                self.new_obj.precio = value.precio_venta
                self.new_obj.cantidad = 1
                self.new_obj.descuento = 0
                self.new_obj.total = value.precio_venta
                
            self.field_producto_large.update()
            self.field_cantidad.update()
            self.field_precio.update()
            self.field_descuento.update()
            self.field_total.update()
            self.field_cantidad.focus()
            # self.set_short_mode()
        else:
            # self.field_producto_large.value = None
            self.field_cantidad.value = None
            self.field_precio.value = None
            self.field_descuento.value = 0
            self.field_total.value = 0
            
        self.calculate_total()
            
    def on_change_cantidad(self, e, value=None):
        if isinstance(value, int):
            self.new_obj.cantidad = value
            self.calculate_total()
            self.field_descuento.focus()
        else:
            self.field_cantidad.focus()
            
    def on_change_precio(self, e, value=None):
        self.field_descuento.focus()
    
    def on_change_descuento(self, e, value=None):
        # self.new_obj.descuento = num_or_zero(e.data)
        # self.calculate_total()
        pass
        
    def on_submit_descuento(self, e, value=None):
        self.new_obj.descuento = to_number_or_zero(e.data)
        # validar que el objeto sea valido para agregarlo a la tabla
        if self.new_obj.producto and isinstance(self.new_obj.cantidad, int):
            self.calculate_total()
            self.add_to_table()
        
    def calculate_total(self):
        self.new_obj.total = num_or_zero(self.new_obj.cantidad) * ((num_or_zero(self.new_obj.precio)-num_or_zero(self.new_obj.descuento)))
        
    def handle_btn_add(self):
        if self.field_producto.value and self.field_cantidad.value and self.field_precio.value:
            self.new_obj.producto = self.field_producto.value
            self.new_obj.cantidad = self.field_cantidad.value
            self.new_obj.precio = self.field_precio.value
            
            # Limpiar los campos
            self.field_producto.value = None
            self.field_cantidad.value = None
            self.field_precio.value = None
            
            # Actualizar la tabla y el resumen
            self.update_table()
            self.update_resume()
            
    def clean_fields(self):
        self.new_obj = DetalleVenta()
        if self.mode == "large":
            self.clean_fields_large()
        else:
            self.clean_fields_short()
            
        # Limpiar la tabla y el resumen
        self.detalles_venta = []
        self.update_table()
        self.update_resume()
            
    def clean_fields_short(self):
        self.field_producto_short.value = ""
        self.field_producto_short.update()
        
    def clean_fields_large(self):
        self.field_producto_large.value = ""
        self.field_cantidad.value = 0
        self.field_precio.value = 0
        self.field_descuento.value = 0
        self.field_total.value = 0
        self.field_producto_large.update()
        self.field_cantidad.update()
        self.field_precio.update()
        self.field_descuento.update()
        self.field_total.update()
            
    def add_to_table(self):
        obj_to_table = copy.copy(self.new_obj)
        for register in self.detalles_venta:
            if register.producto == obj_to_table.producto:
                if self.mode == "short":
                    register.cantidad += obj_to_table.cantidad
                else:
                    register.cantidad = obj_to_table.cantidad
                    register.descuento = obj_to_table.descuento
                # si cantidad es 0 o menor que ceero, eliminar el registro
                if register.cantidad <= 0:
                    self.detalles_venta.remove(register)
                    self.update_table()
                    self.update_resume()
                    self.build_row_fields_short()
                    self.container_fields.update()
                    return
                register.total = register.cantidad * (register.precio - register.descuento)
                self.update_table()
                self.update_resume()
                self.build_row_fields_short()
                self.container_fields.update()
                return
        # si la cantidad es 0 salemos de la funcion
        if obj_to_table.cantidad <= 0:
            return
        self.detalles_venta.append(obj_to_table)
        # Actualizar la tabla con los nuevos datos
        self.update_table()
        self.update_resume()
        # Limpiar los campos después de agregar a la tabla
        self.build_row_fields_short()
        self.container_fields.update()
        
    def update_table(self):
        """Actualiza la tabla con los nuevos datos."""
        self.table.set_data(self.detalles_venta)
        self.table.create_table()
        self.table.update()