from control.control import CONTROL
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.animation import Animation
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.clock import Clock

Builder.load_file("view\\popups.kv")
    
class FileNamePopup(Popup):
    def __init__(self, **kwargs):
        super(FileNamePopup, self).__init__(**kwargs) 
        self.control = CONTROL.save_instance(self, "fnp")
        self.content = FileNamePopupContent(self)
    
    def open(self, *_args, **kwargs):
        self.content.textinput.text = ""
        self.content.save.disabled = False
        return super().open(*_args, **kwargs)

class FileNamePopupContent(RelativeLayout):
    kivy_file_done = BooleanProperty(False)
    def __init__(self, root, **kwargs):
        self.root = root
        super(FileNamePopupContent, self).__init__(**kwargs)
    
    def on_kivy_file_done(self, instance, value):
        if self.kivy_file_done:
            self.cancel.bind(on_press=self.root.dismiss)
            self.save.bind(on_press=lambda a: self.root.control.create_new_file_page())
 
class DeleteFilePopup(Popup):
    def __init__(self, **kwargs):
        super(DeleteFilePopup, self).__init__(**kwargs) 
        self.control = CONTROL.save_instance(self, "dfp")
        self.content = DeleteFilePopupContent(self)
    
    def open(self, *_args, **kwargs):
        self.content.question.text = f"Quer mesmo apagar '{self.control.filearea.current_slide.title}' ?"
        self.content.delete.disabled = False
        return super().open(*_args, **kwargs)
    
class DeleteFilePopupContent(RelativeLayout):
    kivy_file_done = BooleanProperty(False)
    def __init__(self, root, **kwargs): 
        self.root = root
        super(DeleteFilePopupContent, self).__init__(**kwargs)
    
    def on_kivy_file_done(self, instance, value):
        if self.kivy_file_done:
            self.cancel.bind(on_press=self.root.dismiss)
            self.delete.bind(on_press=lambda a: self.root.control.delete_file_page())       

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
        
    

        