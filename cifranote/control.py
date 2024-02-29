from .models import Note
from .tonechanger import ToneChanger

class ControlObject:
    tabs = None
    new_dialog = None
    rename_dialog = None
    delete_dialog = None
    font_dialog = None
    current_textfield = None

    def set_tabs(self, tabs):
        self.tabs = tabs
        for note in Note.select():
            tabs.add_tab(note.title, note.text)

    def add_new_note(self, text):
        self.tabs.add_tab(text)
        #Cria no banco de dados
        Note.create(
            title=text,
            text=''
        )
    
    def rename_note(self, old_text, new_text):
        self.tabs.rename_tab(old_text, new_text)
        #Cria no banco de dados
        note = Note.get(title=old_text)
        note.title = new_text
        note.save()

    def delete_note(self, text):
        self.tabs.remove_tab(text)
        #Cria no banco de dados
        Note.filter(title=text).get().delete_instance()

    def change_tone(self, sharp=True):
        new_text = ToneChanger.semitone_lyric(
            self.current_textfield.value,
            1 if sharp else -1
        )
        self.current_textfield.value = new_text
        self.current_textfield.update()
        self.current_textfield.load_change()
    
    def save_current_note(self):
        if self.current_textfield == None:
            return 
        note = Note.get(title=self.current_textfield.note_title)
        note.text = self.current_textfield.value
        note.save()


Control = ControlObject()