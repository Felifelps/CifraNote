from .models import Note
from .tonechanger import ToneChanger

class ControlObject:
    tabs = None
    new_dialog = None
    rename_dialog = None
    delete_dialog = None
    font_dialog = None
    current_textfield = None
    notes_dialog = None
    notes_list = None

    def undo(self):
        if self.current_textfield:
            return Control.current_textfield.undo()

    def redo(self):
        if self.current_textfield:
            return Control.current_textfield.redo()

    def set_tabs(self, tabs):
        self.tabs = tabs
        for note in Note.select():
            tabs.add_tab(note.title, note.text)

    def set_notes_list(self, lv):
        self.notes_list = lv
        for note in Note.select():
            lv.add_note(note.title)

    def add_new_note(self, text):
        self.tabs.add_tab(text)
        self.notes_list.add_note(text)
        Note.create(
            title=text,
            text=''
        )

    def rename_note(self, old_text, new_text):
        self.tabs.rename_tab(old_text, new_text)
        self.notes_list.rename_note(old_text, new_text)
        note = Note.get(title=old_text)
        note.title = new_text
        note.save()

    def delete_note(self, text):
        self.tabs.remove_tab(text)
        self.notes_list.remove_note(text)
        Note.filter(title=text).get().delete_instance()

    def change_tone(self, sharp=True):
        new_text = ToneChanger.semitone_lyric(
            1 if sharp else -1,
            self.current_textfield.value
        )
        self.current_textfield.value = new_text
        self.current_textfield.update()
        self.current_textfield.load_change()

    def save_current_note(self):
        if not self.current_textfield:
            return False
        note = Note.get(title=self.current_textfield.note_title)
        note.text = self.current_textfield.value
        note.save()

Control = ControlObject()
