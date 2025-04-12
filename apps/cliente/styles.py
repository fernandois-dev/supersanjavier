import flet as ft

from utilities.style_keys import StyleKeys as SK

STYLES = {
    "table_header_bg_color": ft.Colors.SECONDARY_CONTAINER,
    "table_row_bg_color_odd": "#ffffff",
    "table_row_bg_color_even": "#f9f9f9",
    SK.TABLE_ROW_HEIGHT:45,
    "title_style": {
        "size": 24,
        "weight": ft.FontWeight.BOLD,
        "color": ft.Colors.PRIMARY,
    },
    "subtitle_style": {
        "size": 18,
        "weight": ft.FontWeight.NORMAL,
        "color": ft.Colors.PRIMARY,
    },
    "text_style": {
        "size": 14,
        "weight": ft.FontWeight.NORMAL,
        "color": ft.Colors.PRIMARY,
    },
}