from kivy.uix.carousel import Carousel
from kivy.uix.relativelayout import RelativeLayout

class FileArea(Carousel):
    def __init__(self, **kwargs):
        super(FileArea, self).__init__(**kwargs)
            
    def add_page(self, title):
        x = FilePage()
        x.title, x.content = title, ""
        self.add_widget(x)
        self.load_slide(x)
        
class FilePage(RelativeLayout):
    pass
