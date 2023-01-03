from control.control import CONTROL
from kivy.uix.button import Button, Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.animation import Animation
from kivy.properties import BooleanProperty
from kivy.clock import Clock

class FileButton(Button):
    pass
    
class OpenFilePopup(Popup):
    def __init__(self, **kwargs):
        super(OpenFilePopup, self).__init__(**kwargs) 
        self.control = CONTROL.save_instance(self, "ofp")
        self.content = OpenFilePopupContent(self)
    
    def open(self, *_args, **kwargs):
        self.content.clear_buttons()
        self.control.create_list_files()
        self.content.scroll.scroll_y = 1
        return super().open(*_args, **kwargs)

class OpenFilePopupContent(RelativeLayout):
    kivy_file_done = BooleanProperty(False)
    def __init__(self, root, **kwargs):
        self.root = root
        super(OpenFilePopupContent, self).__init__(**kwargs)
    
    def add_button(self, name, selected=False):
        b = FileButton(text=name, on_press=lambda a: [self.root.control.filearea.load_slide(name), self.root.dismiss()])
        if selected: b.line_color = (1, .3, .3, 1)
        self.stack.add_widget(b)
        self.stack.height = b.height * len(self.stack.children)
    
    def clear_buttons(self): self.stack.clear_widgets()
    
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
    
class RenameFilePopup(Popup):
    def __init__(self, **kwargs):
        super(RenameFilePopup, self).__init__(**kwargs) 
        self.control = CONTROL.save_instance(self, "rfp")
        self.content = RenameFilePopupContent(self)
    
    def open(self, *_args, **kwargs):
        self.content.textinput.text = ""
        self.content.rename.disabled = False
        self.content.question.text = f"Renomear '{self.control.filearea.current_slide.title}' para: "
        self.size_hint_x = max(len(self.content.question.text) * 0.035, self.size_hint_x)
        return super().open(*_args, **kwargs)

class RenameFilePopupContent(RelativeLayout):
    kivy_file_done = BooleanProperty(False)
    def __init__(self, root, **kwargs):
        self.root = root
        super(RenameFilePopupContent, self).__init__(**kwargs)
    
    def on_kivy_file_done(self, instance, value):
        if self.kivy_file_done:
            self.cancel.bind(on_press=self.root.dismiss)
            self.rename.bind(on_press=lambda a: self.root.control.rename_file())
    
class DeleteFilePopup(Popup):
    def __init__(self, **kwargs):
        super(DeleteFilePopup, self).__init__(**kwargs) 
        self.control = CONTROL.save_instance(self, "dfp")
        self.content = DeleteFilePopupContent(self)
    
    def open(self, *_args, **kwargs):
        self.content.question.text = f"Quer mesmo apagar '{self.control.filearea.current_slide.title}' ?"
        self.size_hint_x = len(self.content.question.text) * 0.035
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
    def __init__(self, **kwargs):
        super(FastPopup, self).__init__(**kwargs) 
        self.control = CONTROL.save_instance(self, "fp")
        self.opacity = 0
    
    def open(self, text):
        self.size_hint_x = len(text) * 0.03
        self.text = text
        Animation(opacity=1, duration=0.25).start(self)
        Clock.schedule_once(self.kill, 2)
    
    def kill(self, dt): Animation(opacity=0, duration=0.25).start(self)
        
    

        