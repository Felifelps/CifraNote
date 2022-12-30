from model.filemanager import FileManager
from model.tonechanger import ToneChanger

class Control:
    fm = FileManager()
    tn = ToneChanger()
    
    def save_instance(self, instance, iname):
        exec(f"self.{iname} = instance")
        return self
    
    def load_files(self, load=""):
        if load == "": load = self.load_files_cache()
        self.filearea.loaded = False
        for file in self.fm.files: self.filearea.add_page(file, self.fm.load(file), False)
        if self.fm.files == []: load = self.filearea.add_page("Nota Geral", "", False)
        self.filearea.ordenate_slides()
        self.filearea.loaded = True
        self.filearea.load_slide(load)
    
    def save_files_cache(self):
        with open("cache", "w") as arq: arq.write(self.filearea.current_slide.title) 
    
    def load_files_cache(self):
        with open("cache", "r") as arq: return arq.read()

    def create_list_files(self):
        for i in self.filearea.slides: self.ofp.content.add_button(i.title, (True if i == self.filearea.current_slide else False))
        
    def create_new_file_page(self):
        #fired on save click of filenamepopup
        self.fnp.content.save.disabled = True
        if self.fnp.content.textinput.text == "": 
            self.fnp.content.save.disabled = False
            self.fp.open("Nome vazio")
        elif self.fnp.content.textinput.text.lower() in self.fm.files: 
            self.fnp.content.save.disabled = False
            self.fp.open("Já existe")
        else:
            self.fm.save(self.fnp.content.textinput.text, "")
            self.load_files(self.fnp.content.textinput.text)
            self.fnp.dismiss()
            self.fp.open("Arquivo criado")
    
    def rename_file(self):
        #fired on rename click of renamefilepopup
        self.rfp.content.rename.disabled = True
        if self.rfp.content.textinput.text == "": 
            self.rfp.content.rename.disabled = False
            self.fp.open("Nome vazio")
        elif self.rfp.content.textinput.text.lower() in self.fm.files: 
            self.rfp.content.rename.disabled = False
            self.fp.open("Já existe")
        else:
            self.fm.delete(self.filearea.current_slide.title)
            self.fm.save(self.rfp.content.textinput.text, "")
            self.filearea.remove_widget(self.filearea.current_slide)
            self.load_files(self.rfp.content.textinput.text)
            self.rfp.dismiss()
            self.fp.open("Arquivo renomeado")
        
    def delete_file_page(self):
        #fired on delete click on deletefilepopup
        self.dfp.content.delete.disabled = True
        if len(self.fm.files) == 1: return [self.dfp.dismiss(), self.fp.open("Deve haver no mínimo um arquivo")]
        self.fm.delete(self.filearea.current_slide.title)
        self.filearea.remove_widget(self.filearea.current_slide)
        self.fp.open("Arquivo deletado")
        self.dfp.dismiss()

CONTROL = Control()
    