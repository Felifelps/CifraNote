import flet as ft

from cifranote.control import Control
from .custom_modal import CustomModal

def create_font_dialog(page: ft.Page):
    text = ft.Text(
        value='Tamanho do texto',
        text_align=ft.TextAlign.CENTER,
        size=15
    )

    def slider_changed(e):
        text.size = int(e.control.value)
        text.update()

    slider = ft.Slider(
        min=1,
        max=60,
        value=page.client_storage.get('font_size'),
        divisions=59,
        label="{value}",
        on_change=slider_changed
    )

    def dialog_function():
        dialog.close()
        Control.tabs.set_font_size(int(slider.value))
        page.client_storage.set('font_size',  int(slider.value))
        page.snack_bar.popup('Fonte alterada!')

    dialog = CustomModal(
        modal=True,
        title=ft.Text("Alterar"),
        content=ft.ResponsiveRow([
            slider,
            text
        ]),
        actions=[
            ft.TextButton("Selecionar", on_click=lambda _: dialog_function()),
            ft.TextButton("Cancelar", on_click=lambda _: dialog.close()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    dialog.page_ref = page
    Control.font_dialog = dialog
