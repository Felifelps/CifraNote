from model.tonechanger import TONECHANGER
from model.filemanager import FILEMANAGER

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.clock import Clock

class Tab(MDRelativeLayout, MDTabsBase):
    """The notes"""

class NamingDialogContent(MDBoxLayout):
    """Content of naming dialog"""
    
class RenamingDialogContent(MDBoxLayout):
    """Content of renaming dialog"""
    
class Control:
    filemanager = FILEMANAGER
    def menu_callback(self, item):
        self.menu.dismiss()
        
    def create_new_note(self, title):
        if title == "": Snackbar(text="Nome vazio!").open()
        elif title in self.filemanager.files: Snackbar(text="Nota já existente!").open()
        else:
            self.tabs.add_widget(Tab(title=title))
            self.tabs.switch_tab(title)
            Snackbar(text="Nota criada!").open()
            self.naming_dialog.content_cls.ids.textfield.text = ""
            self.filemanager.save(title, "")
            self.save_tabs_order()
    
    def rename_note(self, title):
        if title == "": Snackbar(text="Nome vazio!").open()
        elif title in self.filemanager.files: Snackbar(text="Nota já existente!").open()
        elif self.filemanager.files == []: Snackbar(text="Não há notas para renomear").open()
        else:
            old_title = self.tabs.get_current_tab().title
            self.tabs.get_current_tab().title = title
            Snackbar(text="Nota renomeada!").open()
            self.naming_dialog.content_cls.ids.textfield.text = ""
            self.filemanager.rename(old_title, title)
            self.save_tabs_order()
            
    def delete_note(self):
        if len(self.filemanager.files) <= 1: return Snackbar(text="Deve haver pelo menos uma nota!").open()
        self.filemanager.delete(self.tabs.get_current_tab().title)
        self.tabs.remove_widget(self.tabs.get_current_tab())
        Snackbar(text="Nota excluida!").open()
        self.save_tabs_order()
            
    def on_tab_switch(self, *args):
        Clock.schedule_once(lambda dt: self.filemanager.save_conf("last_opened", self.tabs.get_current_tab().title), 0.5)
    
    def save_tabs_order(self):
        order = []
        for i in self.tabs.get_slides():
            order.append(i.title)
        self.filemanager.save_conf("order", ",".join(order))
        
    def change_tone(self, how_much):
        tab = self.tabs.get_current_tab()
        tab.ids.textfield._undo.append(
            {
                'undo_command': (
                    'delsel', 
                    0, 
                    tab.ids.textfield.text
                ), 
                'redo_command': (
                    0,
                    len(tab.ids.textfield.text)
                )
            }
        )
        lyric = TONECHANGER.semitone_lyric(tab.ids.textfield.text, how_much)
        tab.ids.textfield.text = ""
        tab.ids.textfield.insert_text(lyric)
        
    def save_changes(self, title, text):
        if hasattr(self, "tabs"): self.filemanager.save(title, text)
        
    