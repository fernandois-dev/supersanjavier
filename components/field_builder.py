import copy
import flet as ft
from django.core.exceptions import ValidationError

from components.custom_input import DisplayMode, LayoutMode, ManagerField
from pages.conditions import Conditions



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


class FieldFactory(ft.Container):
    def __init__(self, obj, layout_mode=LayoutMode.VERTICAL, conditions = Conditions(), diplay_mode = DisplayMode.EDIT, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = None
        self.init_values = {}
        self.list_fields = []
        self.conditions = conditions
        self.is_dirty = False
        
        self.obj = obj
        self.original_obj = copy.deepcopy(obj)
        self.layout_mode = layout_mode
        self.display_mode=diplay_mode
        self.expand = 1
        
        self.create_fields()
        
        
    def create_fields(self):
        self.init_values = {}
        self.content = []
        list_fields = []
        
        fields_order = self.conditions.fields_order or [field.name for field in self.obj._meta.fields]
        
        for field_name in fields_order:
            field = next((field for field in self.obj._meta.fields if field.name == field_name), None)
            if not field: continue
            if field.name in self.conditions.fields_excluded: continue
            
            value = getattr(self.obj, field.name, None)
            # instancia el manejo de los campos
            manager_field = ManagerField(display_mode=self.display_mode, input_type=type(field).__name__, layout_mode=self.layout_mode)
            manager_field.build_field(label=field.verbose_name, on_change=self.create_on_change_handler(field), value=value, field=field)
            
            list_fields.append(manager_field)
        self.list_fields = list_fields        
           
        for field in self.list_fields:
            if "ForeignKey" in type(field).__name__ :
                self.init_values[field.name] = field.related_model(id=field.value) if field.value else " "
            else:
                self.init_values[field.name] = field.value
        
        if self.layout_mode == LayoutMode.VERTICAL:
            self.content = ft.Column(controls=self.list_fields)
        elif self.layout_mode == LayoutMode.HORIZONTAL_WRAP:
            self.content = ft.Row(controls=self.list_fields, wrap=True, spacing=10, run_spacing=10)
        else:
            self.content = ft.Row(controls=self.list_fields, spacing=10)
    
        # self.content = [ft.Column(controls=self.list_fields)  
        #                  if self.orientation == "vertical" 
        #                  else ft.Row(controls=self.list_fields, wrap=True, spacing=10, run_spacing=10)]
        
    def get_fields(self):
        return self.list_fields
    
    def create_on_change_handler(self, col):
        def on_change(e, value = None):
            def update_depentents(obj, col_name):
                for field, depend_calculation in self.conditions.fields_calculations.items():
                    depends = depend_calculation.get("depends", [])
                    calculation = depend_calculation.get("calculation", None)
                    if col_name in depends:  # Evitar recalcular el mismo campo
                        new_value = calculation(obj)
                        setattr(obj, field, new_value)
                        
                        # Actualizar el control correspondiente
                        for control in self.controls:
                            if control.data == field:
                                if isinstance(control.content, ft.TextField):
                                    control.content.value = new_value
                                elif isinstance(control.content, ft.Checkbox):
                                    control.content.value = bool(new_value)
                                control.update()
                        
                        update_depentents(obj, field)
             # Actualizar el valor del campo
            setattr(self.obj, col.name, e.control.value if e else value)
            update_depentents(self.obj, col.name) # Actualizar los campos dependientes
            self.is_dirty = not self.compare_objects(self.obj, self.original_obj)
             
        return on_change
    
    def compare_objects(self, obj1, obj2):
        for field in obj1._meta.fields:
            value1 = getattr(obj1, field.name, None)
            value2 = getattr(obj2, field.name, None)
            if value1 != value2:
                return False
        return True
    
    def check_is_dirty(self):
        return not self.is_dirty
    

class FieldBuilder(ft.Column):
    def __init__(self, obj, layout_mode=LayoutMode.VERTICAL, diplay_mode=DisplayMode.EDIT,  conditions = Conditions(), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controls = []
        self.layout_mode = layout_mode
        self.expand = 1
        self.conditions = conditions
        
        self.obj = obj
        self.form_fields = FieldFactory(obj=self.obj, layout_mode=layout_mode, diplay_mode=diplay_mode, conditions = self.conditions)
        self.form_buttons = FormButtons()
        
        self.controls = [self.form_fields, self.form_buttons]
        
    def create_button(self, *args, **kwargs):
        self.form_buttons.create_button(*args, **kwargs)
    
    def validate(self):
        is_valid: bool = True
        for field in self.form_fields.get_fields():
            if hasattr(field, 'validate'):
                if not field.validate():
                    is_valid = False
        return is_valid
    
    def check_is_dirty(self):
        return not self.form_fields.check_is_dirty()
    
    def set_errors(self, errors):
        for manager in self.form_fields.get_fields():
            field = manager.get_field()
            if field.name in errors.message_dict:
                field.helper_text = ' - '.join(errors.message_dict[field.name])
                field.helper_style = ft.TextStyle(color="red")
                field.border_color = "red"
               
            else:
                field.helper_text = None
                field.border_color = None
            field.update()

    def save(self):
        try:
            self.obj.full_clean()
            self.obj.save()
            return True
        except ValidationError as ex:
            self.set_errors(ex)
            return False
    
    
    def get_values(self):
        ret = {}
        for field in self.form_fields.get_fields():
            if field.name == "id":
                if f"{field.name}".isdigit():
                    ret[field.name] = field.value
            else:
                if self.form_fields.init_values[field.name] != field.value:
                    ret[field.name] = field.value
        return ret
            
   
    
        

