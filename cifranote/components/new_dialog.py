import flet as ft

from cifranote.control import Control
from .custom_modal import CustomModal

def create_new_dialog(page: ft.Page):
    text = ft.TextField(
        hint_text="Nomeie a nota",
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
        return Control.add_new_note(text.value)

    dialog = CustomModal(
        modal=True,
        title=ft.Text("Nova nota"),
        content=text,
        actions=[
            ft.TextButton("Criar", on_click=lambda _: dialog_function()),
            ft.TextButton("Cancelar", on_click=lambda _: dialog.close()),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
    dialog.page_ref = page
    Control.new_dialog = dialog