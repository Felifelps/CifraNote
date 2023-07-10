from model.tonechanger import TONECHANGER
from model.filemanager import FILEMANAGER

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.textfield import MDTextFieldRect, MDTextField
from kivy.properties import ObjectProperty

class LimitTextInput(MDTextField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limit_snack = Snackbar(text='Limite de caracteres atingido')
        
    def insert_text(self, substring, from_undo=False):
        if len(self.text + substring) > 26: 
            self.limit_snack.open()
            return False
        return super().insert_text(substring, from_undo)
        
class TabTextField(MDTextFieldRect):
    """The tab textfield"""
    _bubble = ObjectProperty(None)
    def on__bubble(self, value, instance):
        self._bubble.but_cut.text = "Recortar"
        self._bubble.but_copy.text = "Copiar"
        self._bubble.but_paste.text = "Colar"
        self._bubble.but_selectall.text = "Selecionar\n     tudo"
        self._bubble.but_cut.font_size = "12sp"
        self._bubble.but_copy.font_size = "12sp"
        self._bubble.but_paste.font_size = "12sp"
        self._bubble.but_selectall.font_size = "12sp"

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
            self.naming_dialog.content_cls.ids.textfield.text = ""
            self.filemanager.save(title, "")
            self.filemanager.save_conf('order', self.filemanager.get_conf('order') + ',' + title)
            self.switch_note(title)
            Snackbar(text="Nota criada!").open()
    
    def rename_note(self, title):
        if title == "": Snackbar(text="Nome vazio!").open()
        elif title in self.filemanager.files: Snackbar(text="Nota já existente!").open()
        elif self.filemanager.files == []: Snackbar(text="Não há notas para renomear").open()
        else:
            self.naming_dialog.content_cls.ids.textfield.text = ""
            new_order = self.filemanager.get_conf('order').split(',')
            index = new_order.index(self.root.notes.selected)
            new_order.pop(index)
            new_order.insert(index, title)
            self.filemanager.save_conf('order', ','.join(new_order))
            self.filemanager.rename(self.root.notes.selected, title)
            self.switch_note(title)
            Snackbar(text="Nota renomeada!").open()
            
    def delete_note(self):
        if len(self.filemanager.files) <= 1: return Snackbar(text="Deve haver pelo menos uma nota!").open()
        new_order = self.filemanager.get_conf('order').split(',')
        index = new_order.index(self.root.notes.selected)
        new_order.pop(index)
        self.filemanager.save_conf('order', ','.join(new_order))
        self.filemanager.delete(self.root.notes.selected)
        self.switch_note(new_order[index + (1 if index == 0 else -1)])
        Snackbar(text="Nota excluida!").open()
        
    def change_tone(self, how_much):
        self.root.textfield._undo.append(
            {
                'undo_command': (
                    'delsel', 
                    0, 
                    self.root.textfield.text
                ), 
                'redo_command': (
                    0,
                    len(self.root.textfield.text)
                )
            }
        )
        lyric = TONECHANGER.semitone_lyric(self.root.textfield.text, how_much)
        self.root.textfield.text = ""
        self.root.textfield.insert_text(lyric)
        
    def save_changes(self, title, text):
        self.filemanager.save(title, text)
        
    def get_files_order(self):
        return self.filemanager.get_conf('order').split(',')