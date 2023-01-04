from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.properties import BooleanProperty, ListProperty
from kivy.metrics import dp

class OptionButton(Button):
    pass
    
class OptionsButton(Button):
    values = ListProperty(["No values"])
    is_open = BooleanProperty(False)
    def __init__(self, **kwargs):
        super(OptionsButton, self).__init__(**kwargs)
        self.dropdown = DropDown()
        self.dropdown.on_dismiss = lambda: self.false_is_open() 
        self.values = ["Abrir nota", "Renomear nota", "Excluir nota"]
    
    def false_is_open(self): self.is_open = False 
    
    def on_values(self, instance, value):
        for i in self.values: 
            self.dropdown.add_widget(OptionButton(text=i, font_size="15sp", size_hint=(3, None), height=dp(50), on_press=lambda a: self.on_select(a.text)))
        
    def on_press(self):
        self.is_open = True
        self.dropdown.open(self)
        return super().on_press()

    def on_select(self, value):
        self.dropdown.select(value)
        self.is_open = False
        if value == "Abrir nota": self.control.ofp.open()
        elif value == "Renomear nota": self.control.rfp.open()
        elif value == "Excluir nota": self.control.dfp.open()
    
    def on_is_open(self, instance, value):
        if self.is_open:
            self.size_hint = (.3, 1)
            self.pos_hint = {"right": 1, "center_y": 1.5}
        else:
            self.size_hint = (.1, .9)
            self.pos_hint = {"right": 1, "center_y": 0.5}
