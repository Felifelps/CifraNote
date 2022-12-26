from control.control import CONTROL
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.animation import Animation
from kivy.properties import ObjectProperty
from kivy.clock import Clock

Builder.load_file("view\\popups.kv")
    
class FileNamePopup(RelativeLayout):
    root = ObjectProperty(None)
    is_open = False
    open_anim = Animation(opacity=1, duration=0.25)
    close_anim = Animation(opacity=0, duration=0.25)
    def __init__(self, root, **kwargs):
        self.root = root
        super(FileNamePopup, self).__init__(**kwargs) 
        self.control = CONTROL.save_popup_instance(self, "filenamepopup")
        self.opacity = 0
        self.__finished = False
    
    def __final_configurations(self):
        self.cancel.bind(on_press=lambda x: self.dismiss())
        self.save.bind(on_press=lambda x: self.control.create_new_file_page())
    
    def initial_configurations(self):
        self.textinput.text = ""
        self.save.disabled = False
        
    def open(self):
        if not self.__finished: self.__final_configurations()
        self.initial_configurations()
        self.open_anim.start(self)
        self.is_open = True
    
    def dismiss(self):
        self.close_anim.start(self)
        self.is_open = False
    
    def on_touch_down(self, touch):
        if not self.collide_point(touch.x, touch.y) or self.cancel.collide_point(touch.x, touch.y): self.dismiss()
        return super().on_touch_down(touch)
    
class FastPopup(Label):
    def __init__(self, root, **kwargs):
        super(FastPopup, self).__init__(**kwargs) 
        self.opacity = 0
    
    def open(self):
        Animation(opacity=1, duration=0.25).start(self)
        Clock.schedule_once(self.kill, 2)
    
    def kill(self, dt):
        Animation(opacity=0, duration=0.25).start(self)
        del self
        
    
        
        