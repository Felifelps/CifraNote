import os

class FileManager:
    def __init__(self):
        self.main_path = os.path.abspath("cifras")
        try:
            os.mkdir(self.main_path)
        except:
            pass
        self.update()
        
    def update(self): self.files = os.listdir(self.main_path)

    def save(self, title, tone, lyric, new):
        if new:
            n = 0
            while 1:
                if n == len(self.files): break
                elif self.files[n] == title:
                    title += " (1)"
                    n = 0
                n += 1
        with open(os.path.join(self.main_path, f"{title}"), "w") as arq:
            arq.write(f"__TONE__:{tone}\n" + lyric)
        self.update()
        
    def load(self, title):
        try:
            with open(os.path.join(self.main_path, f"{title}"), "r") as arq:
                all = arq.readlines()
        except:
            return 'Erro na leitura do arquivo'
        return {"tone": all[0].replace("__TONE__:", "").replace("\n", ""), "lyric": "".join(all[1:])}
    
    def delete(self, title):
        os.remove(os.path.join(self.main_path, f"{title}"))
        self.update()        
        
FILEMANAGER = FileManager()

import create_tutorial
with open("create_tutorial.py", "w") as arq: arq.write("")