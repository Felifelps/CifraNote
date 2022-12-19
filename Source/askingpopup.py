from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button, Label
from kivy.uix.popup import Popup
from kivy.properties import StringProperty

class AskingPopup(Popup):
    question = StringProperty("")
    def __init__(self, root, question, yes=None, no=None, **kwargs):
        super(AskingPopup, self).__init__(**kwargs)
        self.root = root
        self.size_hint = (0.8, 0.3)
        self.is_open = False
        self.relative = RelativeLayout()
        self.asking = Label(
            text=question, 
            font_size='25sp', 
            size_hint=(.5, .5), 
            pos_hint={"center_x": .5, "center_y": .75}
        )
        self.relative.add_widget(self.asking)
        self.question = question
        self.relative.add_widget(Button(
            text="Sim", 
            font_size='40sp', 
            size_hint=(.5, .5), 
            pos_hint={"center_x": .75, "center_y": .25},
            on_press=self.yes
        ))   
        self.relative.add_widget(Button(
            text="Não", 
            font_size='40sp',
            size_hint=(.5, .5), 
            pos_hint={"center_x": .25, "center_y": .25},
            on_press=self.no
        ))   
        self.content = self.relative
        self.on_no = no
        self.on_yes = yes
    
    def on_question(self, a, b):
        self.asking.text = self.question
        self.title = self.question
        
    def open(self, *_args, **kwargs):
        self.is_open = True
        return super().open(*_args, **kwargs)

    def dismiss(self, *_args, **kwargs):
        self.is_open = False
        return super().dismiss(*_args, **kwargs)
    
    def no(self, instance):
        self.dismiss()
        self.on_no()

    def yes(self, instance):
        self.dismiss()
        self.on_yes()