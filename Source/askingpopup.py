from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import StringProperty

class AskingPopup(Popup):
    question = StringProperty("")
    def __init__(self, root, **kwargs):
        super(AskingPopup, self).__init__(**kwargs)
        self.root = root
        self.is_open = False
        self.title = "Salvar cifra?"
        self.relative = RelativeLayout()
        self.relative.add_widget(Button(
            text="Sim", 
            font_size='40sp', 
            size_hint=(.5, 1), 
            pos_hint={"center_x": .75, "center_y": .5},
            on_press=self.yes
        ))   
        self.relative.add_widget(Button(
            text="Não", 
            font_size='40sp',
            size_hint=(.5, 1), 
            pos_hint={"center_x": .25, "center_y": .5},
            on_press=self.no
        ))   
        self.content = self.relative
        self.on_no = None
        self.on_yes = None
    
    def open(self, *_args, **kwargs):
        self.is_open = True
        return super().open(*_args, **kwargs)

    def dismiss(self, *_args, **kwargs):
        self.is_open = False
        return super().dismiss(*_args, **kwargs)
    
    def no(self, instance):
        self.dismiss()
        self.on_no()
        self.on_no = True

    def yes(self, instance):
        self.dismiss()
        self.on_yes()
        self.on_yes = True