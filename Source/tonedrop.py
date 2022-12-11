from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.properties import StringProperty

class ToneDrop(DropDown):
    selected = StringProperty("")
    def __init__(self, mainbutton, **kwargs):
        super(ToneDrop, self).__init__(**kwargs)
        self.mainbutton = mainbutton
        self.mainbutton.bind(on_release=self.open)
        self.base = ["Auto", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        for option in self.base:
            button = Button(text=option, size_hint=(2.75, None), font_size='18sp', on_release=lambda button: self.on_option_select(button), height=dp(40))
            self.add_widget(button)
    
    def on_option_select(self, button, filename=False):    
        name = (button.text if filename == False else filename)
        self.select(name)
        self.selected = name
        self.mainbutton.text = f"Tom: {self.selected}"
        self.on_selected()