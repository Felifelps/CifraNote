from model.filemanager import FileManager
from model.tonechanger import ToneChanger

class Control:
    fm = FileManager()
    tn = ToneChanger()
    
    def save_instance(self, instance, iname):
        exec(f"self.{iname} = instance")
        return self
    
    def load_files(self):
        cache = self.load_files_cache()
        for file in cache["order"]: self.filearea.add_page(file, self.fm.load(file), False)
        if cache["order"] == []: cache["last"] = self.filearea.add_page("Nota Geral", "", False)
        self.filearea.load_slide(cache["last"])
    
    def save_files_cache(self): 
        string = ""
        for slide in self.filearea.slides: string += slide.title + "\n"
        string += self.filearea.current_slide.title
        with open("cache", "w") as arq: arq.write(string) 
    
    def load_files_cache(self):
        cache = {"order": None, "last": None}
        with open("cache", "r") as arq: alist = arq.read().split("\n")
        cache["last"] = alist.pop(-1)
        print( cache["last"])
        cache["order"] = alist
        print(cache)
        return cache
        
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
    