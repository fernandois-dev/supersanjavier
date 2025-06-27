from typing import Callable
import flet as ft


    
class DlgConfirm(ft.AlertDialog):
    def __init__(self, page: ft.Page,title: str = "", fn_yes: Callable = None, fn_no: Callable = None) -> None:
        super().__init__()
        self.modal=True
        self.page = page
        self.title=ft.Text(title)
        self.actions_alignment=ft.MainAxisAlignment.END
        self.actions=[
            ft.TextButton("Si", on_click= lambda e : self.handle_yes()),
            ft.TextButton("No", on_click= lambda e : self.handle_no()),
        ]
        self.fn_yes = fn_yes
        self.fn_no = fn_no
        self.on_dismiss=lambda e: self.handle_no()   
        self.set_open()
        
    
    def set_open(self):
        self.page.open(self)
        
    def handle_no(self):
        if self.fn_no:
            self.fn_no()
        self.page.close(self)
        
    def handle_yes(self):
        self.fn_yes()
        self.page.close(self)
        
class DlgAlert(ft.AlertDialog):
    def __init__(self, page: ft.Page,title: str = "", content = None) -> None:
        super().__init__()
        self.page = page
        self.title=ft.Text(title)
        self.content = content
        self.page.open(self)