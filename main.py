import kivy
kivy.require("1.9.0")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

Builder.load_file('mainpage.kv')
Builder.load_file('editpage.kv')

import sys
if "win" in sys.platform:
    from kivy.core.window import Window
    Window.size = (400, 800)

class CifraNoteScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(CifraNoteScreenManager, self).__init__(**kwargs)
        
class CifraNoteApp(App):
    def build(self):
        return CifraNoteScreenManager()
    
if __name__ == "__main__":
    CifraNoteApp().run()

    