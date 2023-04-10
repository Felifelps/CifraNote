import os
TUTORIAL = """###TUTORIAL###
Seja bem-vindo ao CifraNote!!

Esse é um app para músicos, então se você se sentir um pouco perdido já sabe para quem perguntar. 

A principal função desse app é facilitar a troca de tom de cifras. Você pode fazer isso apenas colando uma cifra aqui, ou a escrevendo por si só, e usando os botões "b" e "#" acima para diminuir ou aumentar, respectivamente, meio-tom da cifra.

Faça um teste (clique em "b" ou "#" acima):
C G Am F

Ademais, mantenha as cifras salvas aqui (enquanto mantiver o app instalado) e tenha controle sobre o tamanho do texto (menu no canto superior direito).

Divirta-se!!

"""

class FileManager:
    def __init__(self):
        self.main_path = os.path.abspath("files")
        try:
            os.mkdir(self.main_path)
        except:
            pass
        self.__conf_setup()
        if self.get_conf('tutorial') == 'True': 
            self.save('Tutorial', TUTORIAL)
            self.save_conf('tutorial', 'False')
        self.update()
    
    def __conf_setup(self):
        try:
            self.conf()
        except:
            with open("conf", "w") as conf_file:
                conf_file.write("""font_size: 15sp
last_opened: Tutorial
order: Tutorial
tutorial: True      
""")
    def conf(self):
        with open("conf", "r") as conf_file:
            return conf_file.read()
        
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
        text = self.conf()
        for line in text.split("\n"):
            if conf in line:
                with open("conf", "w") as conf_file:
                    return conf_file.write(text.replace(line, conf + ": " + value))
    
    def get_conf(self, conf):
        for line in self.conf().split("\n"):
            if conf in line:
                return line.replace(conf + ": ", "")
        
FILEMANAGER = FileManager()