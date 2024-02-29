import flet as ft

from .components import (
    Control,
    create_appbar,
    create_bottom_menu_bar,
    create_delete_dialog,
    create_font_dialog,
    create_new_dialog,
    create_page_snackbar,
    create_rename_dialog,
    create_tabs
)

def main(page: ft.Page):

    page.title = "CifraNote"

    page.scroll = False

    page.splash = ft.ProgressBar(visible=False)

    page.theme = ft.Theme(color_scheme_seed="brown")

    page.theme_mode = "dark"

    if not page.client_storage.get('font_size'):
        page.client_storage.set('font_size', 15)

    create_new_dialog(page)

    create_rename_dialog(page)

    create_delete_dialog(page)

    create_page_snackbar(page)

    create_font_dialog(page)

    create_appbar(page)

    create_tabs(page)

    create_bottom_menu_bar(page)