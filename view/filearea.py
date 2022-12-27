from kivy.uix.carousel import Carousel
from kivy.uix.relativelayout import RelativeLayout

class FileArea(Carousel):
    def __init__(self, **kwargs):
        super(FileArea, self).__init__(**kwargs)
            
    def add_page(self, title):
        x = FilePage()
        x.title = title
        self.add_widget(x)
        self.load_slide(x)
    
    def load_slide(self, slide):
        return super().load_slide(slide)
        
class FilePage(RelativeLayout):
    pass
