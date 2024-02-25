import flet as ft

from .control import Control

class CustomTabs(ft.Tabs):
    def add_tab(self, text, content, **kwargs):
        self.tabs.append(ft.Tab(
            text=text,
            content=content,
            **kwargs
        ))
        self.update()

    def remove_tab(self, text):
        for index, tab in enumerate(self.tabs):
            if tab.text == text:
                self.tabs.pop(index)

class CustomModal(ft.AlertDialog):
    page_ref = None
    def open_dialog(self):
        self.page_ref.dialog = self
        self.open = True
        self.page_ref.update()

    def close(self):
        self.open = False
        self.page_ref.update()

def create_appbar(page: ft.Page):
    def change_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        e.control.icon = "light_mode" if page.theme_mode == "dark" else "dark_mode"
        page.update()

    def open_drawer(e):
        page.drawer.open = True
        page.drawer.update()

    return ft.AppBar(
        title=ft.Text("CifraNote"),
        center_title=False,
        leading=ft.IconButton(icon="menu"),
        leading_width=40,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
                ft.IconButton(icon="light_mode" if page.theme_mode == "dark" else "dark_mode", on_click=change_theme),
                ft.IconButton(icon="add", on_click=lambda _: Control.new_dialog.open_dialog()),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Light"),
                        ft.PopupMenuItem()
                    ]
                ),
            ],
    )

def create_navigaton_drawer(page: ft.Page):
    return ft.NavigationDrawer(
        controls=[
            ft.NavigationDrawerDestination(
                label="Item 1",
                icon=ft.icons.DOOR_BACK_DOOR_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.DOOR_BACK_DOOR, ),
            ),
        ]
    )

def create_tabs(page: ft.Page):
    tabs = CustomTabs(
        selected_index=0,
        animation_duration=300,
        scrollable=True,
        tabs=[
            ft.Tab(
                text="tab 1",
                content=ft.ResponsiveRow(
                    controls=[
                        ft.TextField(
                            multiline=True,
                            min_lines=550,
                            text_size=20,
                        )
                    ],
                )
            )],
        expand=1,
    )
    Control.tabs = tabs
    return tabs


def create_new_dialog(page: ft.Page):
    text = ft.TextField(
        hint_text="Nomeie a nota",
        autofocus=True,
        on_focus=lambda _: setattr(text, 'value', '') == text.update()
    )
    dialog = CustomModal(
        modal=True,
        title=ft.Text("Nova nota"),
        content=text,
        actions=[
            ft.TextButton("Criar", on_click=lambda _: Control.add_new_note(text.value) == dialog.close()),
            ft.TextButton("Cancelar", on_click=lambda _: dialog.close()),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
    dialog.page_ref = page
    Control.new_dialog = dialog
    return dialog

def create_rename_dialog(page: ft.Page):
    text = ft.TextField(
        hint_text="Renomeie a nota",
        autofocus=True,
        on_focus=lambda _: setattr(text, 'value', '') == text.update()
    )
    dialog = CustomModal(
        modal=True,
        title=ft.Text("Renomear nota"),
        content=text,
        actions=[
            ft.TextButton("Renomear"),
            ft.TextButton("Cancelar", on_click=lambda _: dialog.close()),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
    dialog.page_ref = page
    return dialog

def create_delete_dialog(page: ft.Page):
    dialog = CustomModal(
        modal=True,
        title=ft.Text("Excluir nota?"),
        actions=[
            ft.TextButton("Excluir"),
            ft.TextButton("Cancelar", on_click=lambda _: dialog.close()),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
    dialog.page_ref = page
    return dialog

def create_bottom_menu_bar(page: ft.Page):
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(icon="undo"),
                ft.IconButton(icon="redo"),
                ft.TextButton(text="b", width=42),
                ft.TextButton(text="#", width=42),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND
            
        ),
        bgcolor=ft.colors.SURFACE_VARIANT,
        border_radius=10,
        padding=5,
        
    )