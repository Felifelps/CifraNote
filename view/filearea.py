from kivy.uix.carousel import Carousel
from kivy.uix.relativelayout import RelativeLayout
from control.control import CONTROL

class FileArea(Carousel):
    def __init__(self, **kwargs):
        super(FileArea, self).__init__(**kwargs)
        self.control = CONTROL.save_instance(self, "filearea")
    
    def on_slides(self, *args):
        self.load_slide(self.slides[0])
        return super().on_slides(*args)

    def on_current_slide(self, instance, value):
        self.control.save_files_cache()
    
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
