from kivy.uix.relativelayout import RelativeLayout
from view.popups import *
import os

from kivy.lang import Builder
Builder.load_file(os.path.join('view', 'mainpage.kv'))
Builder.load_file(os.path.join('view', 'filearea.kv'))
Builder.load_file(os.path.join('view', 'optionsbar.kv'))
Builder.load_file(os.path.join('view', 'actionbuttons.kv'))
Builder.load_file(os.path.join('view', 'popups.kv'))

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