import time
import webbrowser

import flet as ft

from .control import Control

class CustomSnackBar(ft.SnackBar):
    def popup(self, text, action="Ok"):
        self.content.value = text
        self.action = action
        self.open = True
        self.update()

class CustomListView(ft.ListView):
    def add_note(self, text):
        def open_note():
            Control.tabs.open(text)
            self.page.dialog.close()

        self.controls.append(ft.OutlinedButton(
            text=text,
            on_click=lambda _: open_note(),
        ))

    def rename_note(self, old_text, new_text):
        for note in self.controls:
            if note.text == old_text:
                note.text = new_text
                return self.update()

    def remove_note(self, text):
        for note in self.controls:
            if note.text == text:
                self.controls.remove(note)

class CustomTextField(ft.TextField):
    def __init__(self, note_title, **kwargs):
        super().__init__(**kwargs)
        self.note_title = note_title
        self.__changes = [self.value]
        self.__last_change = 1
        self.on_change = lambda _: self.__on_change()
        self.on_focus = lambda _: self.__on_focus()
        self.on_blur = lambda _: self.__on_blur()

    def __on_blur(self):
        Control.current_textfield = None

    def __on_focus(self):
        Control.current_textfield = self

    def __on_change(self):
        Control.save_current_note()
        time.sleep(0.2)
        if self.value not in self.__changes:
            self.__changes = self.__changes[:self.__last_change + 1]
            self.__changes.append(self.value)
            self.__last_change = len(self.__changes) - 1

    def load_change(self):
        self.__on_change()

    def undo(self):
        self.__last_change -= 1
        if self.__last_change < 1:
            self.__last_change = 0
        self.value = self.__changes[self.__last_change]
        self.update()

    def redo(self):
        self.__last_change += 1
        if self.__last_change >= len(self.__changes):
            self.__last_change = len(self.__changes) - 1
        self.value = self.__changes[self.__last_change]
        self.update()

class CustomTabs(ft.Tabs):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_change = lambda _: self._on_change()

    def _on_change(self):
        self.page.client_storage.set('last_opened', self.selected_index)
        print(self.tabs[self.selected_index].text, self.selected_index)

    def open(self, text="", index=0):
        if text:
            for i, tab in enumerate(self.tabs):
                if tab.text == text:
                    index = i
                    break
        self.selected_index = index
        return self.update()

    def add_tab(self, text, value="", **kwargs):
        tab = ft.Tab(
            text=text,
            tab_content=ft.Row(
                controls=[
                    ft.Text(value=text),
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(
                                text="Renomear",
                                icon="drive_file_rename_outline",
                                on_click=lambda _: Control.rename_dialog.open_dialog(text=tab.text)
                            ),
                            ft.PopupMenuItem(
                                text="Excluir",
                                icon='delete',
                                on_click=lambda _: Control.delete_dialog.open_dialog(text=tab.text),
                            ),
                        ]
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=0
            ),
            content=ft.ResponsiveRow(
                controls=[
                    CustomTextField(
                        text,
                        value=value,
                        multiline=True,
                        min_lines=550,
                        text_size=self.page.client_storage.get('font_size'),
                        bgcolor=ft.colors.BACKGROUND
                    )
                ],
            ),
            **kwargs
        )
        self.tabs.append(tab)
        self.selected_index = len(self.tabs) - 1
        self.update()

    def rename_tab(self, old_text, new_text):
        for index, tab in enumerate(self.tabs):
            if tab.text == old_text:
                tab.text = new_text
                tab.content.controls[0].note_title = new_text
                tab.tab_content.controls[0].value = new_text
                self.selected_index = index
                return self.update()

    def remove_tab(self, text):
        for tab in self.tabs:
            if tab.text == text:
                self.tabs.remove(tab)
                return self.update()

    def set_font_size(self, size):
        for tab in self.tabs:
            textfield = tab.content.controls[0]
            textfield.text_size = size
            textfield.update()

class CustomModal(ft.AlertDialog):
    page_ref = None
    text = ''
    def open_dialog(self, text=''):
        self.text = text
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
                            on_click=lambda _: webbrowser.open_new('mailto:felipefelipe23456@gmail.com')),
                        ft.PopupMenuItem(
                            text="Sobre",
                            on_click=lambda _: webbrowser.open_new('https://github.com/Felifelps')),
                    ]
                ),
            ],
    )

def create_tabs(page: ft.Page):
    tabs = CustomTabs(
        animation_duration=300,
        scrollable=True,
        tabs=[],
        expand=1,
    )
    page.add(tabs)
    Control.set_tabs(tabs)
    tabs.open(index=page.client_storage.get('last_opened'))

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

def create_page_snackbar(page: ft.Page):
    snack_bar = CustomSnackBar(
        content=ft.Text(""),
        action="Ok!"
    )
    page.snack_bar = snack_bar
