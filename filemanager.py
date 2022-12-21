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

from times import times
if times == 0:
    with open(os.path.abspath("cifras\Tutorial"), "w") as arq:
        arq.write('''__TONE__:C
    Seja bem-vindo ao CifraNote!!

    Desenvolvi esse aplicativo para servir como bloco de notas para cifras, com a funcionalidade especial de trocar o tom das cifras.

    Para criar uma nova cifra, clique no botão de "+" na página inicial. 

    Para excluir um arquivo, basta apertar e segurar no botão do seu nome até aparecer a função "Excluir". Clique e confirme.

    A caixa de texto com o nome "Tutorial" acima serve para alterar o nome do arquivo. 

    Para trocar o tom de uma cifra, use os botões "-Semitom" e "+Semitom" para diminuir ou aumentar, respectivamente, o tom da cifra atual.

    Lembre sempre de salvar a cifra antes de sair.

    Tente trocar o tom: 
    C G Am F

    Aproveite o aplicativo!!
    ''')
    times += 1
if times > 0:
    with open("times.py", "w") as arq:
        arq.write(f"times = {times + 1}")
        
FILEMANAGER = FileManager()

