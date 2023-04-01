import webbrowser

from kivymd.app import MDApp 
from kivy.lang import Builder 
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.button import MDFlatButton
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivy.properties import StringProperty

#from kivy.core.window import Window
#from kivy.metrics import dp
#Window.size = (dp(400), dp(700))

from model.tonechanger import TONECHANGER
from model.filemanager import FILEMANAGER

kv = '''

#:import colors kivymd.color_definitions

<NamingDialogContent>:
    orientation: "vertical"
    size_hint_y: None
    height: textfield.minimum_height
    MDTextField:
        id: textfield
        hint_text: "Nomeie a nota"

<RenamingDialogContent>:
    orientation: "vertical"
    size_hint_y: None
    height: textfield.minimum_height
    MDTextField:
        id: textfield
        hint_text: "Renomeie a nota"
        
<Tab>:
    id: _self
    ScrollView:
        size_hint: 1, 1
        pos_hint: {"center_x": .5, "top": 1}
        MDTextFieldRect:
            id: textfield
            hint_text: "Digite aqui"
            font_size: app.font_size
            line_anim: False
            size_hint: 1, None
            multiline: True
            height: app.root.height * 0.825 if self.minimum_height < app.root.height * 0.825 else self.minimum_height
            padding_x: [dp(10)]
            padding_y: [dp(10)]
            background_color: 0, 0, 0, 0
            foreground_color: 1, 1, 1, 1
            on_text: app.save_changes(_self.title, self.text)

<NoNotesLabel@MDLabel>:
    text: "Sem notas no momento"
    font_size: "20sp"
    theme_text_color: "Custom"
    text_color: 1, 1, 1, 0
    halign: "center"
                
MDScreen:
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            size_hint: 1, .1
            title: "CifraNote"
            right_action_items: 
                [
                ["music-accidental-flat", lambda button: app.actionbarbutton(button)], 
                ["music-accidental-sharp", lambda button: app.actionbarbutton(button)], 
                ["undo", lambda button: app.actionbarbutton(button)], 
                ["redo", lambda button: app.actionbarbutton(button)], 
                ["dots-vertical", lambda button: app.actionbarbutton(button)],
                ]
        
        MDRelativeLayout:
            size_hint: 1, .9
            
            MDTabs:
                id: tabs
                text_color_normal: 1, 1, 1, 1
                text_color_active: 1, 1, 1, 1
                on_tab_switch: app.on_tab_switch(*args)
                tab_indicator_height: dp(4)
            
            MDFloatingActionButtonSpeedDial:
                id: floating
                icon: "pencil"
                root_button_anim: True
                data: {"Nova nota": ["plus", "on_press", lambda x: self.close_stack() == app.naming_dialog.open()], "Renomear nota atual": ["rename-box", "on_press", lambda x: self.close_stack() == app.renaming_dialog.open()], "Excluir nota atual": ["delete", "on_press", lambda x: self.close_stack() == app.deleting_dialog.open()]}
'''

class NamingDialogContent(MDBoxLayout):
    """Content of naming dialog"""
    
class RenamingDialogContent(MDBoxLayout):
    """Content of renaming dialog"""

class Tab(MDRelativeLayout, MDTabsBase):
    """The notes"""

class CifraNoteApp(MDApp):
    notes = ["Nota Geral"]
    print(FILEMANAGER.get_conf("font_size"))
    font_size = StringProperty(FILEMANAGER.get_conf("font_size"))
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Brown"
        return Builder.load_string(kv)

    def save_changes(self, title, text):
        if hasattr(self, "tabs"): FILEMANAGER.save(title, text)
        
    def change_font_size(self, increase=True):
        number = self.font_size.replace("sp", "")
        if increase and int(number) <= 75:
            self.font_size = self.font_size.replace(number, str(int(number) + 1))
        elif not increase and int(number) >= 10:
            self.font_size = self.font_size.replace(number, str(int(number) - 1))
        FILEMANAGER.save_conf("font_size", self.font_size)
    
    def actionbarbutton(self, button):
        if "dots" in button.icon:
            self.menu.caller = button
            self.menu.open()
        elif "music" in button.icon:
            self.change_tone(1 if "sharp" in button.icon else -1)
        elif "undo" in button.icon:
            self.tabs.get_current_tab().ids.textfield.do_undo()
        elif "redo" in button.icon:
            self.tabs.get_current_tab().ids.textfield.do_redo()
    
    def on_font_size(self, instance, value):
        Snackbar(text="Fonte atual: " + self.font_size.replace("sp", ""), duration=0.5).open()
        
    def __create_tabs(self):
        for tab in self.tabs.get_tab_list():
            self.tabs.remove_widget(tab)
        for i in FILEMANAGER.files:
            tab = Tab(title=i)
            print(tab.ids.textfield.font_size)
            tab.ids.textfield.text = FILEMANAGER.load(i)
            self.tabs.add_widget(tab)
    
    def on_start(self):
        for i in self.root.ids: 
            exec(f"self.{i} = self.root.ids[i]")
        self.__create_tabs()
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
        self.menu = MDDropdownMenu(
            items=[
                {
                    "text": "Aumentar fonte",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda: self.change_font_size(),
                },
                {
                    "text": "Diminuir fonte",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda: self.change_font_size(False),
                },
                {
                    "text": "Sobre",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda: webbrowser.open("https://github.com/Felifelps"),
                }
            ],
            width_mult=4
        )
        return super().on_start()
        
    def menu_callback(self, item):
        self.menu.dismiss()
        
    def create_new_note(self, title):
        if title == "": Snackbar(text="Nome vazio!").open()
        elif title in FILEMANAGER.files: Snackbar(text="Nota já existente!").open()
        else:
            self.tabs.add_widget(Tab(title=title))
            self.tabs.switch_tab(title)
            Snackbar(text="Nota criada!").open()
            self.naming_dialog.content_cls.ids.textfield.text = ""
            FILEMANAGER.save(title, "")
            self.__create_tabs()
    
    def rename_note(self, title):
        if title == "": Snackbar(text="Nome vazio!").open()
        elif title in FILEMANAGER.files: Snackbar(text="Nota já existente!").open()
        elif FILEMANAGER.files == []: Snackbar(text="Não há notas para renomear").open()
        else:
            old_title = self.tabs.get_current_tab().title
            self.tabs.get_current_tab().title = title
            Snackbar(text="Nota renomeada!").open()
            self.naming_dialog.content_cls.ids.textfield.text = ""
            FILEMANAGER.rename(old_title, title)
            self.__create_tabs()
            
    def delete_note(self):
        if len(FILEMANAGER.files) <= 1: return Snackbar(text="Deve haver pelo menos uma nota!").open()
        FILEMANAGER.delete(self.tabs.get_current_tab().title)
        self.tabs.remove_widget(self.tabs.get_current_tab())
        Snackbar(text="Nota excluida!").open()
            
    def on_tab_switch(self, *args):
        pass
    
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
        
CifraNoteApp().run()
