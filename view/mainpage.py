from kivy.uix.relativelayout import RelativeLayout
from view.popups import *

from kivy.lang import Builder
Builder.load_file('view\\mainpage.kv')

class MainPage(RelativeLayout):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        self.control = CONTROL.save_instance(self, "mainpage")
        self.control.load_files()
        OpenFilePopup()
        FileNamePopup()
        DeleteFilePopup()
        RenameFilePopup()
        self.add_widget(FastPopup())