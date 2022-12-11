import os
class FileManager:
    def __init__(self):
        self.main_path = os.path.abspath("cifras")
        try:
            os.mkdir(self.main_path)
        except:
            pass
        self.update()
        
    def update(self):
        self.files = os.listdir(self.main_path)

    def save(self, title, tone, lyric=""):
        n = 0
        with open(os.path.join(self.main_path, f"{title}"), "w") as arq:
            arq.write(f"__TONE__:{tone}\n" + lyric)
        self.update()
        
    def load(self, title):
        try:
            with open(os.path.join(self.main_path, f"{title}"), "r") as arq:
                all = arq.readlines()
        except:
            return 'Erro'
        return {"tone": all[0].replace("__TONE__:", "").replace("\n", ""), "lyric": "".join(all[1:])}
    
    def delete(self, title):
        os.remove(os.path.join(self.main_path, f"{title}"))
        self.update()        

FILEMANAGER = FileManager()
FILEMANAGER.save("Tutorial", "C", '''Seja bem-vindo ao CifraNote!!

Desenvolvi esse aplicativo para
servir como bloco de notas para
cifras, com a funcionalidade
especial de trocar o tom das
cifras.

Para criar uma nova cifra, clique
no botão de "+" na página inicial. 

Para excluir um arquivo, basta apertar e segurar no botão do seu
nome até aparecer a função
"Excluir". Clique e confirme.

A caixa de texto com o nome 
"Tutorial" acima serve para alterar
o nome do arquivo. 

Para trocar o tom de uma cifra,
basta clicar no botão "Tom" acima
e selecionar o tom que quer trocar.

Há algumas falhas no mecanismo
de troca de tom que serão
corrigidas em futuras
atualizações.

Tente trocar o tom: 
C G Am F

Aproveite o aplicativo!!
''')