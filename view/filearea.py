from kivy.uix.carousel import Carousel
from kivy.uix.relativelayout import RelativeLayout
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
    pass
