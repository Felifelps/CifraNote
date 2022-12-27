from model.filemanager import FileManager
from model.tonechanger import ToneChanger
from view.popups import *

class Control:
    fm = FileManager()
    tn = ToneChanger()
    
    def save_instance(self, instance, iname):
        exec(f"self.{iname} = instance")
        return self

    def create_file_popup(self):
        self.fnp = FileNamePopup()
        self.fnp.cancel.bind(on_press=lambda x: self.dismiss())
        self.fnp.save.bind(on_press=lambda x: self.control.create_new_file_page())

    #FileNamePopup
    def create_new_file_page(self):
        #fired on save click of filenamepopup
        self.mainpage.fnp.save.disabled = True
        if self.mainpage.fnp.textinput.text == "": 
            self.mainpage.fnp.save.disabled = False
            self.mainpage.fastpopup.text = "Nome vazio"
            self.mainpage.fastpopup.open()
        elif self.mainpage.fnp.textinput.text.lower() in self.fm.files: 
            self.mainpage.fnp.save.disabled = False
            self.mainpage.fastpopup.text = "Já existe"
        else:
            self.filearea.add_page(self.mainpage.fnp.textinput.text)
            self.fm.save(self.mainpage.fnp.textinput.text, "")
            self.mainpage.fnp.dismiss()
            self.mainpage.fastpopup.text = "Arquivo criado"
        self.mainpage.fastpopup.open()
        
    def delete_file_page(self):
        #fired on delete click on deletefilepopup
        self.mainpage.dfp.delete.disabled = True
        self.mainpage.fastpopup.text = "Arquivo deletado"
        self.mainpage.fastpopup.open()
        self.filearea.remove_widget(self.filearea.current_slide)
        self.fm.delete(self.mainpage.dfp.current)
        self.mainpage.dfp.dismiss()

CONTROL = Control()
    