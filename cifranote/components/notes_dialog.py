import flet as ft

from cifranote.control import Control
from .custom_modal import CustomModal, CustomListView

def create_notes_dialog(page: ft.Page):
    lv = CustomListView(spacing=5)

    dialog = CustomModal(
        modal=True,
        title=ft.Text("Ver notas"),
        content=lv,
        actions=[
            ft.TextButton("Sair", on_click=lambda _: dialog.close()),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
    dialog.page_ref = page
    Control.notes_dialog = dialog
    Control.set_notes_list(lv)
