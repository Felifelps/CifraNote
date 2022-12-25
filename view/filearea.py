from kivy.uix.carousel import Carousel
from kivy.uix.relativelayout import RelativeLayout

class FileArea(Carousel):
    def __init__(self, **kwargs):
        super(FileArea, self).__init__(**kwargs)
    
    def add_page(self, title, content=""):
        x = FilePage()
        x.title, x.content = title, content
        self.add_widget(x)
        
class FilePage(RelativeLayout):
    pass
