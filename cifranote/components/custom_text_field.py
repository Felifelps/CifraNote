import time
import flet as ft

from cifranote.control import Control

class CustomTextField(ft.TextField):
    def __init__(self, note_title, **kwargs):
        super().__init__(**kwargs)
        self.note_title = note_title
        self.__changes = [self.value]
        self.__last_change = 1
        self.on_change = lambda _: self.__on_change()

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
