from kivy.uix.carousel import Carousel
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from control.control import CONTROL
from kivy.properties import BooleanProperty, StringProperty, ObjectProperty
from kivy.metrics import dp
from kivy.clock import Clock

class FileArea(Carousel):
    loaded = BooleanProperty(False)
    def __init__(self, **kwargs):
        super(FileArea, self).__init__(**kwargs)
        self.control = CONTROL.save_instance(self, "filearea")
        self.scroll_distance = dp(75)
        self.scroll_timeout = 200
            
    def on_current_slide(self, instance, value): 
        if self.loaded: self.control.save_files_cache()
    
    def load_slide(self, slide):
        if isinstance(slide, str):
            for i in self.slides:
                if i.title == slide:
                    slide = i
                    break
        return super().load_slide(slide)
        
    def add_page(self, title, content, load=True):
        slide = FilePage(self)
        slide.title, slide.content = title, content
        self.add_widget(slide)
        if load: self.load_slide(slide)
        return slide
        
class FilePage(RelativeLayout):
    title = StringProperty("")
    content = StringProperty("")
    def __init__(self, filearea, **kwargs):
        self.filearea = filearea
        super(FilePage, self).__init__(**kwargs)
    
    def on_content(self, instance, value): self.filearea.control.fm.save(self.title, self.content)
    
class FilePageTextInput(TextInput):
    _bubble = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(FilePageTextInput, self).__init__(**kwargs)
        
    def on_text(self, instance, value): 
        self.filepage.content = self.text
    
    def change_tone(self, lyric):
        self._undo.append({'undo_command': ('delsel', 0, self.text), 'redo_command': (0, len(self.text))})
        self.text = ""
        self.insert_text(lyric)
    
    def select_all(self, erase=False):
        override = super().select_all()
        if erase: Clock.schedule_once(lambda dt: self.do_backspace(), 1)
        return override
    
    def on_cursor(self, instance, value):
        self.height = max((len(self._lines) + 15) * self.line_height, self.filepage.filearea.control.mainpage.height*0.85)
        return super().on_cursor(instance, value)
        
    def on__bubble(self, instance, value):
        self._bubble.but_cut.text = "Recortar"
        self._bubble.but_copy.text = "Copiar"
        self._bubble.but_paste.text = "Colar"
        self._bubble.but_selectall.text = "Selecionar\ntudo"
        self._bubble.but_cut.font_size = "12sp"
        self._bubble.but_copy.font_size = "12sp"
        self._bubble.but_paste.font_size = "12sp"
        self._bubble.but_selectall.font_size = "12sp"
        
   
        
