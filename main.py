import webbrowser, platform

from control import Control, RenamingDialogContent, NamingDialogContent
from kivymd.app import MDApp 
from kivy.lang import Builder 
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivy.properties import StringProperty, DictProperty

if platform.system() == 'Windows':
    from kivy.core.window import Window
    from kivy.metrics import dp
    Window.size = (dp(400), dp(700))

class CifraNoteApp(MDApp, Control):
    font_size = StringProperty(Control.filemanager.get_conf("font_size"))
    file_data = DictProperty({})
    undo_data = DictProperty({})
    
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Brown"
        return Builder.load_file('style.kv')
    
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
    
    def new_note(self, title):
        self.file_data[title] = ''
        self.undo_data[title] = []
    
    def delete_note_data(self, title):
        data = {key: value for key, value in self.file_data.items() if key != title}
        self.file_data = data
        data = {key: value for key, value in self.undo_data.items() if key != title}
        self.undo_data = data
    
    def on_font_size(self, instance, value):
        Snackbar(text="Fonte atual: " + self.font_size.replace("sp", ""), duration=0.5).open()
    
    def switch_note(self, title, saves_current=True):
        #Saves the current note
        if saves_current: self.save_note_data(self.notes.selected)
        #Changes
        self.notes.selected = title
        self.filemanager.save_conf('last_opened', title)
        self.textfield._undo = self.undo_data[title]
        self.update_selected()
            
    def change_font_size(self, increase=True):
        number = self.font_size.replace("sp", "")
        if increase and int(number) <= 75:
            self.font_size = self.font_size.replace(number, str(int(number) + 1))
        elif not increase and int(number) >= 10:
            self.font_size = self.font_size.replace(number, str(int(number) - 1))
        self.filemanager.save_conf("font_size", self.font_size)
    
    def on_start(self):
        self.link = lambda: webbrowser.open("https://github.com/Felifelps")
        self.file_data = {title: self.filemanager.load(title) for title in self.get_files_order()}
        self.undo_data = {title: [] for title in self.get_files_order()}
        self.notes, self.textfield = self.root.ids._notes, self.root.ids._textfield
        self.textfield.text = self.file_data[self.notes.selected]
        self.switch_note(self.notes.selected)
        self.naming_dialog = MDDialog(
            title="Criar nota",
            type="custom",
            content_cls=NamingDialogContent(),
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
        return super().on_start()

    def on_stop(self):
        self.save_note_data(self.notes.selected)
        self.filemanager.save_conf('last_opened', self.notes.selected)
        for title, data in self.file_data.items():
            self.filemanager.save(title, data)
        return super().on_stop()

    def on_pause(self):
        self.on_stop()
        return super().on_pause()

    def on_resume(self):
        self.stopped = Snackbar(text='Carregando dados salvos...')
        self.stopped.open()
        return super().on_resume()

#try:
CifraNoteApp().run()
#except Exception as e:
#    input(e)