from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.metrics import dp

class TutorialPage(Screen):
    pass

class TutorialPageModel(RelativeLayout):
    def back_to_mainpage(self, instance):
        self.root.manager.current = "mainpage"
        