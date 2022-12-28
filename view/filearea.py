from kivy.uix.carousel import Carousel
from kivy.uix.relativelayout import RelativeLayout
from control.control import CONTROL

class FileArea(Carousel):
    def __init__(self, **kwargs):
        super(FileArea, self).__init__(**kwargs)
        self.control = CONTROL.save_instance(self, "filearea")
        self.control.load_files()
        
    def add_page(self, title):
        x = FilePage()
        x.title = title
        self.add_widget(x)
        self.load_slide(x)
        
class FilePage(RelativeLayout):
    pass
