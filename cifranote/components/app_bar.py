import flet as ft

from cifranote.control import Control

def create_appbar(page: ft.Page):
    def change_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        e.control.icon = "light_mode" if page.theme_mode == "dark" else "dark_mode"
        page.client_storage.set('theme_mode', page.theme_mode)
        page.update()

    page.appbar = ft.AppBar(
        title=ft.Text("CifraNote"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
                ft.IconButton(icon="light_mode" if page.theme_mode == "dark" else "dark_mode", on_click=change_theme),
                ft.IconButton(icon="add", on_click=lambda _: Control.new_dialog.open_dialog()),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            text="Ver notas",
                            on_click=lambda _: Control.notes_dialog.open_dialog()),
                        ft.PopupMenuItem(
                            text="Tamanho do texto",
                            on_click=lambda _: Control.font_dialog.open_dialog()),
                        ft.PopupMenuItem(
                            text="Reportar falhas",
                            on_click=lambda _: page.launch_url('mailto:felipefelipe23456@gmail.com')
                        ),
                        ft.PopupMenuItem(
                            text="Sobre",
                            on_click=lambda _: page.launch_url('https://github.com/Felifelps'),
                        )
                    ]
                ),
            ],
    )
