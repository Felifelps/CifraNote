from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from filemanager import FILEMANAGER
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from askingpopup import AskingPopup
from kivy.lang import Builder
from kivy.properties import ObjectProperty

class FileButtons(ScrollView):
    def __init__(self, **kwargs):
        super(FileButtons, self).__init__(**kwargs)
        self.do_scroll_y = True
        self.do_scroll_x = False
        self.box = BoxLayout(orientation="vertical",size_hint_y=None)
        self.box.bind(minimum_height=self.box.setter('height'))
        self.update()
        self.add_widget(self.box)
    
    def update(self):
        self.box.clear_widgets()
        n = 1
        for cipher in FILEMANAGER.files:
            button = FileButton(
                self,
                text=cipher, 
                size_hint=(0.99, None), 
                height='80sp',
                color=(1, 1, 1, 1), 
                pos_hint={"center_x": 0.5}
                )
            self.box.add_widget(button)
            n += 1
        if FILEMANAGER.files == []: self.box.add_widget(Label(text="Não temos cifras no momento", size_hint=(1, None), height=80, font_size="25sp"))
        self.size = self.box.size

    def remake_organization(self, base_string):
        self.box.clear_widgets()
        files = FILEMANAGER.files
        order = []
        for string in files:
            if base_string.lower() in string.lower() or string.lower() in base_string.lower(): order.append(string)

        for string in files:
            if string not in order: order.append(string)
                
        for title in order:
            self.box.add_widget(FileButton(
                self,
                text=title, 
                size_hint=(0.99, None), 
                height='80sp',
                color=(1, 1, 1, 1), 
                pos_hint={"center_x": 0.5}
            ))
        
        if self.box.children == []:
            self.box.add_widget(Label(text="Não encontramos cifras parecidas", size_hint=(1, None), height=80, font_size=20))

class FileButton(Button):
    def __init__(self, root, **kwargs):
        super(FileButton, self).__init__(**kwargs)
        self.root = root
        self.data = FILEMANAGER.load(self.text)
        self.use = True
        self.popup = AskingPopup(self, self.text, size_hint=(.8, .2), title=self.text)
        b = BoxPopup()
        b.root = self.popup
        self.popup.content = b
    
    def delete(self): 
        new_popup = AskingPopup(self, "Excluir este arquivo?", size_hint=(.8, .2))
        def dismiss():
            new_popup.dismiss()
            self.popup.dismiss()
        def yes():
            FILEMANAGER.delete(self.text)
            self.root.update()
            dismiss()
        new_popup.no = lambda a: dismiss()
        new_popup.yes = lambda a: yes() 
        new_popup.open()
    
    def on_press(self):
        self.use = True
        Clock.schedule_once(self.on_hold, 0.25)
        return super().on_press()

    def on_hold(self, dt):
        if self.use == True:
            self.popup.open()
    
    def on_release(self):
        self._cancel()
        if not self.popup.is_open:
            manager = self.root.root.root.manager
            manager.current = 'editpage'
            manager.ids['editpage'].model.load_data(self.text, self.data["tone"], self.data["lyric"])
        return super().on_release()
    
    def _cancel(self): self.use = False

class BoxPopup(BoxLayout):
    def __init__(self, **kwargs):
        super(BoxPopup, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        delete = Button(text='Excluir', font_size='27sp')
        delete.bind(on_press=self.delete)
        self.add_widget(delete)
        
    def rename(self, a):
        self.root.root.rename()
    
    def delete(self, a):
        self.root.root.delete()

        