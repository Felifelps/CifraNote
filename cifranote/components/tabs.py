import flet as ft

from cifranote.control import Control
from .custom_tab import CustomTab

class CustomTabs(ft.Tabs):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_change = self._on_change

    def _on_change(self, _):
        self.page.client_storage.set('last_opened', self.selected_index)
        Control.current_textfield = self.tabs[self.selected_index].text_field

    def open(self, text="", index=0):
        if text:
            for i, tab in enumerate(self.tabs):
                if tab.text == text:
                    index = i
                    break
        if len(self.tabs) > index:
            index = 0
        self.selected_index = index
        self.update()
        Control.current_textfield = self.tabs[index].text_field

    def add_tab(self, text, value="", **kwargs):
        tab = CustomTab(self, text, value, **kwargs)
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


def create_tabs(page: ft.Page):
    tabs = CustomTabs(
        animation_duration=300,
        scrollable=True,
        tabs=[],
        expand=1
    )
    page.add(tabs)
    Control.set_tabs(tabs)

    index = page.client_storage.get('last_opened')
    tabs.open(index)
