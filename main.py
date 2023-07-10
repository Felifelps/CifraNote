import webbrowser, platform

from control import Control, RenamingDialogContent, NamingDialogContent
from kivymd.app import MDApp 
from kivy.lang import Builder 
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivy.properties import StringProperty

if platform.system() == 'Windows':
    from kivy.core.window import Window
    from kivy.metrics import dp
    Window.size = (dp(400), dp(700))

class CifraNoteApp(MDApp, Control):
    font_size = StringProperty(Control.filemanager.get_conf("font_size"))
    save_when_stop = []
    file_data = {}
    
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Brown"
        return Builder.load_file('style.kv')
    
    def actionbarbutton(self, button):
        if "menu" in button.icon:
            self.root.lm.rv.data = [{'text': i, 'selected': i == self.root.notes.selected} for i in self.get_files_order()]
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
    
    def update_notes(self):
        self.root.notes.data = []
        for i in self.get_files_order():
            self.root.notes.data.append({'text': i, 'selected': i == self.root.notes.selected})
            if i not in self.file_data: self.file_data[i] = self.filemanager.load(i)
        self.filemanager.save_conf('order', ','.join(self.get_files_order()))
    
    def on_font_size(self, instance, value):
        Snackbar(text="Fonte atual: " + self.font_size.replace("sp", ""), duration=0.5).open()
    
    def switch_note(self, title):
        self.file_data[self.root.notes.selected] = self.root.textfield.text
        self.root.notes.selected = title
        self.update_notes()
        self.root.textfield.text = self.file_data[title]
        self.root.textfield_scroll.scroll_y = 1
        self.filemanager.save_conf("last_opened", title)
            
    def change_font_size(self, increase=True):
        number = self.font_size.replace("sp", "")
        if increase and int(number) <= 75:
            self.font_size = self.font_size.replace(number, str(int(number) + 1))
        elif not increase and int(number) >= 10:
            self.font_size = self.font_size.replace(number, str(int(number) - 1))
        self.filemanager.save_conf("font_size", self.font_size)
    
    def on_start(self):
        self.link = lambda: webbrowser.open("https://github.com/Felifelps")
        self.update_notes()
        self.switch_note(self.filemanager.get_conf('last_opened'))
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
        self.file_data[self.root.notes.selected] = self.root.textfield.text
        for title, data in self.file_data.items():
            if title in self.get_files_order():
                self.save_changes(title, data)
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