from components.custom_input import SearchField
from modules.pos.pages.cash_register_page import CashRegisterPage
import flet as ft

from modules.pos.pages.pos_config_page import POSConfigPage
from pages.conditions import Conditions
from utilities.utilities import num_or_zero



def pos(page: ft.Page, params: dict):
    view = CashRegisterPage(page=page)
    return view

def pos_config(page: ft.Page, params: dict):
    view = POSConfigPage(page=page)
    return view
