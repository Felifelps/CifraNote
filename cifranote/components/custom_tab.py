import flet as ft

from cifranote.control import Control
from .custom_text_field import CustomTextField

class CustomTab(ft.Tab):
    def __init__(self, tab, text, value="", **kwargs):
        super().__init__(**kwargs)
        self.tab = tab
        self.text = text
        self.value = value
        self.tab_content = ft.Row(
            controls=[
                ft.Text(value=text),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            text="Renomear",
                            icon="drive_file_rename_outline",
                            on_click=lambda _: Control.rename_dialog.open_dialog(text=self.tab.text)
                        ),
                        ft.PopupMenuItem(
                            text="Excluir",
                            icon='delete',
                            on_click=lambda _: Control.delete_dialog.open_dialog(text=self.tab.text),
                        ),
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=0
        )

        self.text_field = CustomTextField(
            self.text,
            value=self.value,
            multiline=True,
            min_lines=550,
            text_size=self.tab.page.client_storage.get('font_size'),
            bgcolor=ft.colors.BACKGROUND
        )

        self.content=ft.ResponsiveRow(
            controls=[
                self.text_field
            ],
        )
