from kivy.uix.relativelayout import RelativeLayout
from view.popups import *

from kivy.lang import Builder
Builder.load_file('view\\mainpage.kv')

class MainPage(RelativeLayout):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        self.fastpopup = FastPopup(self)
        self.add_widget(self.fastpopup)