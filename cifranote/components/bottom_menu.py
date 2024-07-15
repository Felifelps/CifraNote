import flet as ft

from cifranote.control import Control 

def create_bottom_menu_bar(page: ft.Page):
    page.add(ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(icon="undo", on_click=lambda _: Control.undo()),
                ft.IconButton(icon="redo", on_click=lambda _: Control.redo()),
                ft.TextButton(text="b", width=42, on_click=lambda _: Control.change_tone(False)),
                ft.TextButton(text="#", width=42, on_click=lambda _: Control.change_tone()),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            height=40
        ),
        bgcolor=ft.colors.SURFACE_VARIANT,
        border_radius=10,
        padding=5,
    ))
