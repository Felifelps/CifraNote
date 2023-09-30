import webbrowser, platform, configparser

from kivymd.app import MDApp 
from kivy.lang import Builder 
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.button import MDFlatButton, MDTextButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextFieldRect, MDTextField
from kivymd.uix.snackbar import Snackbar
from kivy.properties import StringProperty, DictProperty, ObjectProperty
from kivy.core.window import Window

from tonechanger import TONECHANGER

if platform.system() == 'Windows':
    from kivy.metrics import dp
    Window.size = (dp(400), dp(700))

TUTORIAL = """###TUTORIAL###
Seja bem-vindo ao CifraNote!!

Esse é um app para músicos, então se você se sentir um pouco perdido já sabe para quem perguntar. 

A principal função desse app é facilitar a troca de tom de cifras. Você pode fazer isso apenas colando uma cifra aqui, ou a escrevendo por si só, e usando os botões "b" e "#" abaixo para diminuir ou aumentar, respectivamente, meio-tom da cifra.

Faça um teste (clique em "b" ou "#" abaixo):
C G Am F

Ademais, mantenha as cifras salvas aqui (enquanto mantiver o app instalado) e tenha controle sobre o tamanho do texto (menu no canto superior direito).

Divirta-se!!###TUTORIAL###
Seja bem-vindo ao CifraNote!!

Esse é um app para músicos, então se você se sentir um pouco perdido já sabe para quem perguntar. 

A principal função desse app é facilitar a troca de tom de cifras. Você pode fazer isso apenas colando uma cifra aqui, ou a escrevendo por si só, e usando os botões "b" e "#" abaixo para diminuir ou aumentar, respectivamente, meio-tom da cifra.

Faça um teste (clique em "b" ou "#" abaixo):
C G Am F

Ademais, mantenha as cifras salvas aqui (enquanto mantiver o app instalado) e tenha controle sobre o tamanho do texto (menu no canto superior direito).

Divirta-se!!
"""

class CifraNoteApp(MDApp):
    font_size = StringProperty('15sp')
    file_data = DictProperty({})
    undo_data = DictProperty({})
    redo_data = DictProperty({})
    
    def build(self):
        self.conf = configparser.ConfigParser()
        self.conf.read('config.ini')
        self.files = JsonStore('files.json')
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Brown"
        return Builder.load_file('style.kv')
    
    def on_textinput_focus(self, **args):
        print('Focus')
        
    def actionbarbutton(self, button):
        if "menu" in button.icon:
            self.root.lm.rv.data = [{'text': i, 'selected': i == self.notes.selected} for i in self.get_files_order()]
            self.root.lm.open()
        elif "music" in button.icon:
            self.change_tone(1 if "sharp" in button.icon else -1)
        elif "undo" in button.icon:
            self.root.textfield.do_undo()
        elif "redo" in button.icon:
            self.root.textfield.do_redo()
        elif 'plus' in button.icon:
            self.naming_dialog.open() 
        elif 'form' in button.icon:
            self.renaming_dialog.open()
        elif 'trash' in button.icon:
            self.deleting_dialog.open()
    
    def update_selected(self):
        self.notes.data = [{'text': title, 'selected': title == self.notes.selected} for title in self.get_files_order()]
        
    def save_note_data(self, title, data=False):
        self.file_data[title] = self.textfield.text if data == False else data
        self.undo_data[title] = self.textfield._undo
        self.redo_data[title] = self.textfield._redo
    
    def new_note(self, title):
        self.file_data[title] = ''
        self.undo_data[title] = []
        self.redo_data[title] = []
    
    def delete_note_data(self, title):
        data = {key: value for key, value in self.file_data.items() if key != title}
        self.file_data = data
        data = {key: value for key, value in self.undo_data.items() if key != title}
        self.undo_data = data
        data = {key: value for key, value in self.redo_data.items() if key != title}
        self.redo_data = data
    
    def switch_note(self, title, saves_current=True):
        #Saves the current note
        if saves_current: self.save_note_data(self.notes.selected)
        #Changes
        self.conf['options']['last_opened'] = title
        self.textfield._undo = self.undo_data[title]
        self.textfield._redo = self.redo_data[title]
        self.notes.selected = title
        self.update_selected()
            
    def change_font_size(self, increase=True):
        number = self.font_size.replace("sp", "")
        if increase and int(number) <= 75:
            self.font_size = self.font_size.replace(number, str(int(number) + 1))
        elif not increase and int(number) >= 10:
            self.font_size = self.font_size.replace(number, str(int(number) - 1))
        self.conf["options"]['font_size'] = self.font_size
    
    def advice(self, text):
        self.dialog.text = text
        self.dialog.open()
    
    def adjust_bottombar_height(self, instance, keyboard, keycode, text, modifiers):
        if keyboard:
            Snackbar(text=str(keycode)).open()
            #keyboard down
            if keycode == 40:
                self.root.bottombar.y = 0
            #keyboard up
            elif keycode == 41:
                self.root.bottombar.y = self.root_window.keyboard_height
        
    def on_start(self):
        self.dialog = MDDialog(title='Atenção!', text='')
        self.link = lambda: webbrowser.open("https://github.com/Felifelps")
        self.font_size = self.conf['options']['font_size']
        self.file_data = {title: self.files.get(title)['data'] for title in self.get_files_order()}
        self.undo_data = {title: [] for title in self.get_files_order()}
        self.redo_data = {title: [] for title in self.get_files_order()}
        self.notes, self.textfield = self.root.notes, self.root.textfield
        self.textfield.text = self.file_data[self.notes.selected]
        self.dialogs()
        self.switch_note(self.notes.selected)
        
        keyboard = Window.request_keyboard(lambda *args: print('Hi', args), self.root)
        if keyboard.widget:
            self.vkeyboard = keyboard.widget
            self.textfield.text = str(dir(self.vkeyboard))
        Window.bind(on_keyboard=self.adjust_bottombar_height)
        return super().on_start()
    
    def dialogs(self):
        self.naming_dialog = MDDialog(
            title="Criar nota",
            type="custom",
            content_cls=NamingDialogContent(),
            size_hint=(.8, None),
            buttons=[
                MDFlatButton(
                    text="Sair",
                    on_press=lambda x: self.naming_dialog.dismiss()
                ),
                MDFlatButton(
                    text="Criar",
                    on_press=lambda x: self.create_new_note(self.naming_dialog.content_cls.ids.textfield.text) == self.naming_dialog.dismiss() 
                )
            ]
        )
        self.renaming_dialog = MDDialog(
            title="Renomear nota atual para:",
            type="custom",
            content_cls=RenamingDialogContent(),
            size_hint=(.8, None),
            buttons=[
                MDFlatButton(
                    text="Sair",
                    on_press=lambda x: self.renaming_dialog.dismiss()
                ),
                MDFlatButton(
                    text="Renomear",
                    on_press=lambda x: self.rename_note(self.renaming_dialog.content_cls.ids.textfield.text) == self.renaming_dialog.dismiss() 
                )
            ]
        )
        self.deleting_dialog = MDDialog(
            title="Excluir nota atual?",
            size_hint=(.8, None),
            buttons=[
                MDFlatButton(
                    text="Sair",
                    on_press=lambda x: self.deleting_dialog.dismiss()
                ),
                MDFlatButton(
                    text="Excluir",
                    on_press=lambda x: self.delete_note() == self.deleting_dialog.dismiss() 
                )
            ]
        )

    def on_stop(self):
        self.save_note_data(self.notes.selected)
        self.conf['options']['last_opened'] = self.notes.selected
        for title, data in self.file_data.items():
            self.files.put(title, data=data)
        with open('config.ini', 'w') as file:
            self.conf.write(file)
        return super().on_stop()

    def on_pause(self):
        self.on_stop()
        return super().on_pause()

    def create_new_note(self, title):
        self.naming_dialog.content_cls.ids.textfield.text = ""
        if title == "": self.advice("Nome vazio!")
        elif title in self.file_data: self.advice("Nota já existente!")
        else:
            self.files.put(title, data="")
            self.conf['options']['order'] = self.conf['options']['order'] + ',' + title
            self.new_note(title)
            self.switch_note(title)
            Snackbar(text="Nota criada!").open()
    
    def rename_note(self, title):
        self.renaming_dialog.content_cls.ids.textfield.text = ""
        if title == "": self.advice("Nome vazio!")
        elif title in self.file_data: self.advice("Nota já existente!")
        else:
            #Order
            new_order =  self.conf['options']['order'].split(',')
            index = new_order.index(self.notes.selected)
            new_order.pop(index)
            new_order.insert(index, title)
            self.conf['options']['order'] = ','.join(new_order)
            #File
            self.files.put(title, data=self.files.get(self.notes.selected)['data'])
            self.files.delete(self.notes.selected)
            self.save_note_data(title)
            self.delete_note_data(self.notes.selected)
            self.switch_note(title, False)
            Snackbar(text="Nota renomeada!").open()
            
    def delete_note(self):
        if len(self.get_files_order()) < 2: return self.advice("Deve haver pelo menos uma nota!")
        new_order = self.conf['options']['order'].split(',')
        index = new_order.index(self.notes.selected)
        new_order.pop(index)
        self.conf['options']['order'] = ','.join(new_order)
        self.delete_note_data(self.notes.selected)
        self.files.delete(self.notes.selected)
        self.switch_note(new_order[index + ((1 if len(new_order) > 1 else 0) if index == 0 else -1)])
        Snackbar(text="Nota excluida!").open()
        
    def change_tone(self, how_much):
        self.textfield._undo.append(
            {
                'undo_command': (
                    'delsel', 
                    0, 
                    self.textfield.text
                ), 
                'redo_command': (
                    0,
                    len(self.textfield.text)
                )
            }
        )
        lyric = TONECHANGER.semitone_lyric(self.textfield.text, how_much)
        self.textfield.text = ""
        self.textfield.insert_text(lyric)
        
    def get_files_order(self):
        return self.conf['options']['order'].split(',')
    
class LimitTextInput(MDTextField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.to_widget
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

if __name__ == '__main__':
    CifraNoteApp().run()