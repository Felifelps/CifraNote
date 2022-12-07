from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button, Label
from kivy.uix.bubble import BubbleButton, Bubble
from kivy.uix.textinput import TextInput, TextInputCutCopyPaste
from kivy.metrics import dp
from kivy.uix.popup import Popup
from tonedrop import ToneDrop
from filemanager import FILEMANAGER
from tone_changer import TONE_CHANGER
from kivy.properties import StringProperty
from askingpopup import AskingPopup

class EditPage(Screen):
    def __init__(self, **kwargs):
        super(EditPage, self).__init__(**kwargs)
        self.name = 'editpage'
        self.model = EditPageModel(self)
        self.add_widget(self.model)

class EditPageModel(RelativeLayout):
    title = StringProperty("")
    lyric = StringProperty("")
    def __init__(self, root, **kwargs):
        super(EditPageModel, self).__init__(**kwargs)
        self.root = root
        self.controlbar = ControlBar(
            root=self,
            pos_hint={"x": 0, "top": 1},
            size_hint=(1, 0.2)
        )
        self.add_widget(self.controlbar)
    
    def load_data(self, title, tone, lyric):
        self.controlbar.load(title, tone)
        self.textinput.text = lyric
        self.new = False
    
    def new_file(self):
        self.controlbar.new()
        self.textinput.text = ""
        self.new = True

class ToneChangerTextInput(TextInput):
    def __init__(self, **kwargs):
        super(ToneChangerTextInput, self).__init__(**kwargs)
    
    def change_tone(self, root, old, new):
        if self.selection_text != "": 
            self.text = self.text.replace(self.selection_text, TONE_CHANGER.change_tone(self.selection_text, old, new))
        else:
            self.text = TONE_CHANGER.change_tone(self.text, old, new)
            root.tonevisor.text = f"Tom: {new}"
            root.tone = new
        
    def on_cursor(self, instance, value):
        one_percent = self.scroll.height/100
        relative_cursor_pos = 1 - (((self.line_height*self.cursor_row)/one_percent)/100)
        if self.cursor_pos[1] > self.scroll.height or self.cursor_pos[1] < self.scroll.top - self.scroll.height: self.scroll.scroll_y = relative_cursor_pos
        return super().on_cursor(instance, value)
    
class ControlBar(RelativeLayout):
    tone = StringProperty("Auto")
    def __init__(self, root, **kwargs):
        super(ControlBar, self).__init__(**kwargs)
        self.root = root
        self.textinput = root.textinput

        self.__tone_visors()

        self.__buttons()

        self.__popup_creating()
    
    def __tone_visors(self):
        self.tonevisor = Label(
            text=f"Tom: {self.tone}",
            size_hint=(0.25, 0.25),
            pos_hint={"center_x": 0.25, "center_y": 0.75},
            font_size='18sp'
        )
        self.add_widget(self.tonevisor)

        self.tonebutton = Button(
            text=f"Tom: {self.tone}",
            size_hint=(0.23, 0.25),
            pos_hint={"center_x": 0.26, "center_y": 0.75},
            font_size='18sp'
        )
        self.tone_drop = ToneDrop(self.tonebutton)
        self.tone_drop.on_selected = lambda: self.root.change_tone(self.tone, self.tone_drop.selected)
        self.add_widget(self.tonebutton)

    def __popup_creating(self):
        self.popup = AskingPopup(self, size_hint=(.8, .2))
        self.popup.title = "Salvar alterações?"
        self.popup.on_no = self.exit
        self.popup.on_yes = self.save

    def __buttons(self):
        self.sharpbutton = Button(
            text="+Semitom",
            size_hint=(0.25, 0.25),
            pos_hint={"center_x": 0.75, "center_y": 0.75},
            font_size='18sp',
            on_press=lambda instance: self.textinput.change_tone(self, self.tone, TONE_CHANGER.NOTE_POSITION[1 if TONE_CHANGER.MAJOR_SCALES["C"][self.tone] + 1 == 13 else TONE_CHANGER.MAJOR_SCALES["C"][self.tone] + 1])
        )
        self.add_widget(self.sharpbutton)

        self.flatbutton = Button(
            text="-Semitom",
            size_hint=(0.25, 0.25),
            pos_hint={"center_x": 0.5, "center_y": 0.75},
            font_size='18sp',
            on_press=lambda instance: self.textinput.change_tone(self, self.tone, TONE_CHANGER.NOTE_POSITION[12 if TONE_CHANGER.MAJOR_SCALES["C"][self.tone] - 1 == 0 else TONE_CHANGER.MAJOR_SCALES["C"][self.tone] - 1])
        )
        self.add_widget(self.flatbutton)
    
    def load(self, title, tone):
        self.remove_widget(self.tonebutton)
        if self.tonevisor not in list(self.children): self.add_widget(self.tonevisor)
        self.titleinput.text = title
        self.tonevisor.text = f"Tom: {tone}"
        self.tone = tone
        self.sharpbutton.disabled, self.flatbutton.disabled = False, False
    
    def new(self):
        self.remove_widget(self.tonevisor)
        if self.tonebutton not in list(self.children): self.add_widget(self.tonebutton)
        self.titleinput.text = "Nova cifra"
        self.tonebutton.text = "Tom: Auto" 
        self.tone = "Auto"
        self.sharpbutton.disabled, self.flatbutton.disabled = True, True
        
    def save_actual_tone(self):
        self.tone = self.tone_drop.selected
        
    def exit(self): self.root.root.manager.current = 'mainpage'
    
    def quit(self): self.popup.open()
    
    def save(self):
        FILEMANAGER.save(self.titleinput.text, (TONE_CHANGER.get_tone(self.textinput.text) if self.tone == "Auto" else self.tone), self.textinput.text, self.root.new)
        def close(instance):
            popup.dismiss()
            self.exit()
        popup = Popup(size_hint=(.75, .2), title="Cifra salva", content=Button(text="Ok", on_press=close, font_size='25sp'))
        popup.open()
        