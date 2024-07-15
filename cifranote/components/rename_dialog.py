import flet as ft

from cifranote.control import Control
from .custom_modal import CustomModal

def create_rename_dialog(page: ft.Page):
    text = ft.TextField(
        hint_text="Renomeie a nota",
        autofocus=True,
        on_focus=lambda _: setattr(text, 'value', '') == text.update()
    )

    def dialog_function():
        dialog.close()
        if text.value == "":
            return page.snack_bar.popup('Campo vazio!')
        for tab in Control.tabs.tabs:
            if tab.text == text.value:
                return page.snack_bar.popup('Essa nota já existe!')
        return Control.rename_note(dialog.text, text.value)

    dialog = CustomModal(
        modal=True,
        title=ft.Text("Renomear nota"),
        content=text,
        actions=[
            ft.TextButton("Renomear", on_click=lambda _: dialog_function()),
            ft.TextButton("Cancelar", on_click=lambda _: dialog.close()),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
    dialog.page_ref = page
    Control.rename_dialog = dialog