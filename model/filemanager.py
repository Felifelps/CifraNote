import os

class FileManager:
    def __init__(self):
        self.main_path = os.path.abspath("files")
        try:
            os.mkdir(self.main_path)
        except:
            pass
        self.update()
        
    def update(self): self.files = os.listdir(self.main_path)

    def save(self, title, lyric):
        with open(os.path.join(self.main_path, f"{title}"), "w") as arq: arq.write(lyric)
        self.update()
        
    def load(self, title):
        try: 
            with open(os.path.join(self.main_path, f"{title}"), "r") as arq: return "".join(arq.readlines())
        except: return 'Erro na leitura do arquivo'
    
    def delete(self, title):
        os.remove(os.path.join(self.main_path, f"{title}"))
        self.update()   
    
    def rename(self, old_title, new_title):
        old_file = self.load(old_title)
        self.delete(old_title)
        self.save(new_title, old_file) 
           
FILEMANAGER = FileManager()
