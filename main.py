import kivy
kivy.require("1.9.0")
from kivy.app import App

from view.mainpage import MainPage

import sys
if "win" in sys.platform:
    from kivy.core. window import Window
    from kivy.metrics import dp
    Window.size = (dp(400), dp(700))
    
class CifraNoteApp(App):
    def build(self):
        return MainPage()
    
if __name__ == "__main__":
    CifraNoteApp().run()

    