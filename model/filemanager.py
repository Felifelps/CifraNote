import os

class FileManager:
    def __init__(self):
        self.conf = """font_size: 15sp"""
        self.main_path = os.path.abspath("files")
        try:
            os.mkdir(self.main_path)
        except:
            pass
        self.__conf_setup()
        self.update()
    
    def __conf_setup(self):
        try:
            with open(".conf", "r") as conf_file:
                self.conf = conf_file.read()
        except:
            with open(".conf", "w") as conf_file:
                conf_file.write(self.conf)
        
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
    
    def save_conf(self, conf, value):
        for line in self.conf.split("\n"):
            if conf in line:
                with open(".conf", "w") as conf_file:
                    conf_file.write(self.conf.replace(line, conf + ": " + value))
                    return self.__conf_setup()
    
    def get_conf(self, conf):
        for line in self.conf.split("\n"):
            if conf in line:
                return line.replace(conf + ": ", "")
        
FILEMANAGER = FileManager()

