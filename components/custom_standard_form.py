import flet as ft
from django.core.exceptions import ValidationError

from components.custom_input import CustomCheckbox, CustomDropdown, CustomTextField
from data.custom_fields import CustomDateTimeField


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

class FormFields(ft.Column):
    def __init__(self, obj, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alignment=ft.MainAxisAlignment.END
        self.controls = []
        self.init_values = {}
        self.width=350
        self.obj = obj
        
        
    def create_fields(self):
        self.init_values = {}
        self.controls = []
        for field in self.obj._meta.fields:
            if "BooleanField" in type(field).__name__ :
                self.controls.append(CustomCheckbox(label=field.verbose_name, name=field.name, value=getattr(self.obj, field.name)))
            if "CharField" in type(field).__name__ :
                self.controls.append(CustomTextField(label=field.verbose_name, name=field.name, value=getattr(self.obj, field.name),is_required=not field.null, input_type="str"))
            if "EmailField" in type(field).__name__ :
                self.controls.append(CustomTextField(label=field.verbose_name, name=field.name, value=getattr(self.obj, field.name),is_required=not field.null, input_type="str"))
            if "DateTimeField" in type(field).__name__ :
                self.controls.append(CustomDateTimeField(label=field.verbose_name, name=field.name, value=getattr(self.obj, field.name)))
            if "AutoField" in type(field).__name__ :
                self.controls.append(CustomTextField(label=field.verbose_name, name=field.name, value=getattr(self.obj, field.name), disabled=True, input_type="str"))
            if "IntegerField" in type(field).__name__ :
                self.controls.append(CustomTextField(label=field.verbose_name, name=field.name, value=getattr(self.obj, field.name), input_type="int"))    
            if "ForeignKey" in type(field).__name__ :
                self.controls.append(
                    CustomDropdown(label=field.verbose_name, name=field.name, value=getattr(self.obj, f"{field.name}_id") ,
                        options=[ft.dropdown.Option("", text=" ", data=None)] + [ ft.dropdown.Option(str(opt.id), text=str(opt), data=opt) for opt in field.related_model.objects.all()],)
                )
                
            # INIT VALUES, COMPARE TO SAVE
        for field in self.controls:
            if "ForeignKey" in type(field).__name__ :
                self.init_values[field.name] = field.related_model(id=field.value) if field.value else " "
            else:
                self.init_values[field.name] = field.get_value()
            
        

class Form(ft.Column):
    def __init__(self, obj, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controls = []
        self.width=350
        self.obj = obj
        self.form_fields = FormFields(self.obj)
        self.form_buttons = FormButtons()

    def create_fields(self):
        self.form_fields.create_fields()
        
    def create_button(self, *args, **kwargs):
        self.form_buttons.create_button(*args, **kwargs)
        
    def update_controls(self):
        self.controls = [self.form_fields, self.form_buttons]
    
    def validate(self):
        is_valid: bool = True
        for field in self.form_fields.controls:
            if hasattr(field, 'validate'):
                if not field.validate():
                    is_valid = False
        return is_valid
    
    def set_errors(self, errors):
        for field in self.form_fields.controls:
            if field.name in errors.message_dict:
                field.helper_text = ' - '.join(errors.message_dict[field.name])
                field.helper_style = ft.TextStyle(color="red")
                field.border_color = "red"
               
            else:
                field.helper_text = None
                field.border_color = None
            field.update()

    def save(self):
        form_values = self.get_values()
        # VALIDATION 
        obj_validation = self.obj
        for atributo in form_values: setattr(obj_validation, atributo, form_values[atributo])
        try:
            self.obj.full_clean()
            # SAVE
            for atributo in form_values: setattr(self.obj, atributo, form_values[atributo])
            self.obj.save()
            return True
        except ValidationError as ex:
            self.set_errors(ex)
            return False
    
    
    def get_values(self):
        ret = {}
        for field in self.form_fields.controls:
            if field.name == "id":
                if f"{field.name}".isdigit():
                    ret[field.name] = field.get_value()
            else:
                if self.form_fields.init_values[field.name] != field.get_value():
                    ret[field.name] = field.get_value()
        return ret
            
    def validate_form_change(self):
        is_valid: bool = True
        for field in self.form_fields.controls:
            if field.name != "id" and self.form_fields.init_values[field.name] != field.get_value():
                is_valid = False
        return is_valid
   

        

