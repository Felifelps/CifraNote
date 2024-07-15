import flet as ft

from cifranote.control import Control

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
