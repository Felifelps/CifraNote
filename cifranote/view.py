import flet as ft

from .components import *

def main(page: ft.Page):

    page.title = "CifraNote"

    page.scroll = False

    page.splash = ft.ProgressBar(visible=False)

    page.theme = ft.Theme(color_scheme_seed="brown")

    page.theme_mode = "dark"

    new_dialog = create_new_dialog(page)

    rename_dialog = create_rename_dialog(page)

    delete_dialog = create_delete_dialog(page)

    page.appbar = create_appbar(page)

    page.add(create_tabs(page))

    page.add(create_bottom_menu_bar(page))
