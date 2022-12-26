import os

class FileManager:
    def __init__(self):
        self.main_path = os.path.abspath("cifras")
        try:
            os.mkdir(self.main_path)
        except:
            pass
        self.update()
        
    def update(self): self.files = list(map(lambda x: x.lower(), os.listdir(self.main_path)))

    def save(self, title, lyric):
        with open(os.path.join(self.main_path, f"{title.lower()}"), "w") as arq: arq.write(lyric)
        self.update()
        
    def load(self, title):
        try: 
            with open(os.path.join(self.main_path, f"{title}"), "r") as arq: return "".join(arq.readlines())
        except: return 'Erro na leitura do arquivo'
    
    def delete(self, title):
        os.remove(os.path.join(self.main_path, f"{title}"))
        self.update()     
           
FILEMANAGER = FileManager()

if "__Tutorial__" in FILEMANAGER.files:
    FILEMANAGER.save(
        "__Tutorial__", 
        '''Seja bem-vindo ao CifraNote!!

Desenvolvi esse aplicativo para servir como bloco de notas para cifras, com a funcionalidade especial de trocar o tom das cifras.

Para criar uma nova cifra, clique no botão de "+" na página inicial. 

Para excluir um arquivo, basta apertar e segurar no botão do seu nome até aparecer a função "Excluir". Clique e confirme.

A caixa de texto com o nome "Tutorial" acima serve para alterar o nome do arquivo. 

Para trocar o tom de uma cifra, use os botões "-Semitom" e "+Semitom" para diminuir ou aumentar, respectivamente, o tom da cifra atual.

Lembre sempre de salvar a cifra antes de sair.

Tente trocar o tom: 
C G Am F

Aproveite o aplicativo!!''')