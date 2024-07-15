import flet as ft

from cifranote.control import Control
from .custom_modal import CustomModal

def create_delete_dialog(page: ft.Page):
    def dialog_function():
        dialog.close()
        if len(Control.tabs.tabs) < 2:
            return page.snack_bar.popup('Você precisa ter ao menos uma nota')
        return Control.delete_note(dialog.text)

    dialog = CustomModal(
        modal=True,
        title=ft.Text("Excluir nota?"),
        actions=[
            ft.TextButton("Excluir", on_click=lambda _: dialog_function()),
            ft.TextButton("Cancelar", on_click=lambda _: dialog.close()),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
    dialog.page_ref = page
    Control.delete_dialog = dialog
