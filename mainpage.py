import kivy
kivy.require("1.9.0")

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button, Label
from kivy.uix.textinput import TextInput
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from filebuttons import FileButtons
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

class MainPage(Screen):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        self.enter = 0
    
    def on_pre_enter(self, *args):
        if self.enter > 0:
            self.model.filebuttons.update()
        self.enter += 1
        return super().on_pre_enter(*args)

class SearchBar(RelativeLayout):
    def __init__(self, **kwargs):
        super(SearchBar, self).__init__(**kwargs)
        self.textinput = TextInput(
            multiline=False,
            text="",
            size_hint=(.7, .7),
            pos_hint={"center_x": .45, "center_y": .5},
            font_size='27sp',
            hint_text="Pesquisar cifra"
        )
        self.textinput.bind(on_text_validate=self.search)
        self.add_widget(self.textinput)
        
        self.searchbutton = SearchButton(
            size_hint=(.125, .69),
            pos_hint={"right": .9, "center_y": .5},
            on_press=self.search 
        )
        self.add_widget(self.searchbutton)

    def search(self, instance):
        self.root.filebuttons.remake_organization(self.textinput.text)

class CreateFileButton(Button):
    def __init__(self, **kwargs):
        super(CreateFileButton, self).__init__(**kwargs)
        self.bind(on_press=self.editpage)
    
    def editpage(self, instance):
        manager = self.root.root.manager
        manager.current = 'editpage'
        manager.ids['editpage'].model.new_file()

class SearchButton(Button):
    pass

class CreditsButton(Button):
    def __init__(self, **kwargs):
        super(CreditsButton, self).__init__(**kwargs)
        self.bind(on_press=self.creditspopup)
        self.popup = Popup(
                title="Créditos", 
                size_hint=(.8, .3), 
                content=Label(
                    text="Design - Felifelps\nProgramação - Felifelps\nGitHub - @Felifelps\nVersão 1.0",
                    color=(1, 1, 1, 1),
                    font_size='25sp',
                    halign="center",
                    valign="top"
                )
        )
        
    def creditspopup(self, instance):
        self.popup.open()
    