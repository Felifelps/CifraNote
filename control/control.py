from model.filemanager import FileManager
from model.tonechanger import ToneChanger

class Control:
    fm = FileManager()
    tn = ToneChanger()
    
    def save_instance(self, instance, iname):
        exec(f"self.{iname} = instance")
        return self
    
    def load_files(self):
        for i in self.fm.files: 
            self.filearea.add_page(i)
        self.filearea.load_slide(self.filearea.slides[0])
        
    def create_new_file_page(self):
        #fired on save click of filenamepopup
        self.fnp.content.save.disabled = True
        if self.fnp.content.textinput.text == "": 
            self.fnp.content.save.disabled = False
            self.mainpage.fastpopup.text = "Nome vazio"
            self.mainpage.fastpopup.open()
        elif self.fnp.content.textinput.text.lower() in self.fm.files: 
            self.fnp.content.save.disabled = False
            self.mainpage.fastpopup.text = "Já existe"
        else:
            self.filearea.add_page(self.fnp.content.textinput.text)
            self.fm.save(self.fnp.content.textinput.text, "")
            self.fnp.dismiss()
            self.mainpage.fastpopup.text = "Arquivo criado"
        self.mainpage.fastpopup.open()
        
    def delete_file_page(self):
        #fired on delete click on deletefilepopup
        self.dfp.content.delete.disabled = True
        self.mainpage.fastpopup.text = "Arquivo deletado"
        self.mainpage.fastpopup.open()
        self.fm.delete(self.filearea.current_slide.title)
        self.filearea.remove_widget(self.filearea.current_slide)
        self.dfp.dismiss()

CONTROL = Control()
    