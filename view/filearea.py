from kivy.uix.carousel import Carousel
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from control.control import CONTROL
from kivy.properties import BooleanProperty

class FileArea(Carousel):
    loaded = BooleanProperty(False)
    def __init__(self, **kwargs):
        super(FileArea, self).__init__(**kwargs)
        self.control = CONTROL.save_instance(self, "filearea")

    def ordenate_slides(self):
        titles = sorted([i.title for i in self.slides])
        new_list = []
        for j in titles:
            for i in self.slides:
                if i.title == j: 
                    new_list.append(i)
                    break
        self.clear_widgets()
        for i in new_list: self.add_widget(i)
            
    def on_current_slide(self, instance, value): 
        if self.loaded: self.control.save_files_cache()
    
    def load_slide(self, slide):
        if isinstance(slide, str):
            for i in self.slides:
                if i.title == slide:
                    slide = i
                    break
        return super().load_slide(slide)
        
    def add_page(self, title, content, load=True):
        slide = FilePage()
        slide.title, slide.content = title, content
        self.add_widget(slide)
        if load: self.load_slide(slide)
        return slide
        
class FilePage(RelativeLayout):
    kivy_file_done = BooleanProperty(False)
    def __init__(self, **kwargs):
        super(FilePage, self).__init__(**kwargs)
        self.control = CONTROL
    
    def on_content(self, instance, value):
        print("content")
        self.control.fm.save(self.title, self.content)
    
    def save_content(self): 
        print("save")
        self.content = self.textinput 
    
    def on_kivy_file_done(self, instance, value):
        if self.kivy_file_done: 
            print("bind")
            self.textinput.bind(on_text=lambda a, b: self.save_content())
    
class MyTextInput(TextInput):
    def on_text(self, instance, value):
        
