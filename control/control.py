from model.filemanager import FileManager
from model.tonechanger import ToneChanger

class Control:
    def __init__(self, owner):
        self.fm = FileManager()
        self.tn = ToneChanger()
        self.owner = owner
        
    

        
    