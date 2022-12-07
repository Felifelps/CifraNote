import os
from tone_changer import CipherHandler

class CifraFile(CipherHandler):
    def __init__(self, title, tone):
        self.title = title
        self.tone = tone
        self.lyric = ""
        self.capo = "sem capo"
    
    def save_and_change_tone(self, new_tone):
        self.lyric = self.change_tone(self.lyric, self.tone, new_tone)
        self.tone = new_tone
    
class CifraFiles:
    def __init__(self):
        self.files = []
        self.main_path = os.path.abspath("cifras")
        try:
            os.mkdir(self.main_path)
        except:
            pass
    
    def add_file(self, cifrafile):
        cifrafile.id = len(self.files) + 1
        n = 0
        for file in self.files:
            if file.title == cifrafile.title: n += 1
        cifrafile.title += ("" if n == 0 else f" ({n})")
        self.files.append(cifrafile)
        with open(os.path.join(self.main_path, f"{cifrafile.title}"), "w") as arq:
            arq.write(f"_TONE_:{cifrafile.tone}\n_CAPO_:{cifrafile.capo}\n{cifrafile.lyric}")
        
    def remove_file(self, title):
        pass
        