from model.filemanager import FileManager
from model.tonechanger import ToneChanger

class Control:
    fm = FileManager()
    tn = ToneChanger()
    instances = {}
    popups = {}
    
    def save_instance(self, instance, iclass):
        self.instances[iclass] = instance
        return self

    def save_popup_instance(self, popup, pclass):
        self.popups[pclass] = popup
        return self

    #FileNamePopup
    def create_new_file_page(self):
        #fired on save click of filenamepopup
        popup = self.popups['filenamepopup']
        popup.save.disabled = True
        mainpage = self.instances['mainpage']
        filearea = self.instances['filearea']
        if popup.textinput.text == "": 
            popup.save.disabled = False
            mainpage.fastpopup.text = "Nome vazio"
            mainpage.fastpopup.open()
        elif popup.textinput.text.lower() in self.fm.files: 
            popup.save.disabled = False
            mainpage.fastpopup.text = "Já existe"
            mainpage.fastpopup.open()
        else:
            filearea.add_page(popup.textinput.text)
            self.fm.save(popup.textinput.text, "")
            popup.dismiss()

CONTROL = Control()
    

    

        
    