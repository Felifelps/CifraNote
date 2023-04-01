class ToneChanger:
    NOTES_RELATION = {
        "C":  {"C": 1, "C#": 2, "Db": 2, "D": 3, "D#": 4, "Eb": 4, "E": 5, "F": 6, "F#": 7, "Gb": 7, "G": 8, "G#": 9,  "Ab": 9, "A": 10, "A#": 11, "Bb": 11, "B": 12},
        "C#":  {"C": 12, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,  "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11},
        "Db":  {"C": 12, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,  "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11},
        "D":  {"C": 11, "C#": 12, "Db": 12, "D": 1, "D#": 2, "Eb": 2, "E": 3, "F": 4, "F#": 5, "Gb": 5, "G": 6, "G#": 7,  "Ab": 7, "A": 8, "A#": 9, "Bb": 9, "B": 10},
        "D#":  {"C": 10, "C#": 11, "Db": 11, "D": 12, "D#": 1, "Eb": 2, "E": 2, "F": 3, "F#": 4, "Gb": 4, "G": 5, "G#": 6,  "Ab": 6, "A": 7, "A#": 8, "Bb": 8, "B": 9},
        "Eb":  {"C": 10, "C#": 11, "Db": 11, "D": 12, "D#": 1, "Eb": 2, "E": 2, "F": 3, "F#": 4, "Gb": 4, "G": 5, "G#": 6,  "Ab": 6, "A": 7, "A#": 8, "Bb": 8, "B": 9},
        "E":  {"C": 9, "C#": 10, "Db": 10, "D": 11, "D#": 12, "Eb": 12, "E": 1, "F": 2, "F#": 3, "Gb": 3, "G": 4, "G#": 5,  "Ab": 5, "A": 6, "A#": 7, "Bb": 7, "B": 8},
        "F":  {"C": 8, "C#": 9, "Db": 9, "D": 10, "D#": 11, "Eb": 11, "E": 12, "F": 1, "F#": 2, "Gb": 2, "G": 3, "G#": 4,  "Ab": 4, "A": 5, "A#": 6, "Bb": 6, "B": 7},
        "F#":  {"C": 7, "C#": 8, "Db": 8, "D": 9, "D#": 10, "Eb": 10, "E": 11, "F": 12, "F#": 1, "Gb": 1, "G": 2, "G#": 3,  "Ab": 3, "A": 4, "A#": 5, "Bb": 5, "B": 6},
        "Gb":  {"C": 7, "C#": 8, "Db": 8, "D": 9, "D#": 10, "Eb": 10, "E": 11, "F": 12, "F#": 1, "Gb": 1, "G": 2, "G#": 3,  "Ab": 3, "A": 4, "A#": 5, "Bb": 5, "B": 6},
        "G":  {"C": 6, "C#": 7, "Db": 7, "D": 8, "D#": 9, "Eb": 9, "E": 10, "F": 11, "F#": 12, "Gb": 12, "G": 1, "G#": 2,  "Ab": 2, "A": 3, "A#": 4, "Bb": 4, "B": 5},
        "G#":  {"C": 5, "C#": 6, "Db": 7, "D": 7, "D#": 8, "Eb": 8, "E": 9, "F": 10, "F#": 11, "Gb": 11, "G": 12, "G#": 1,  "Ab": 1, "A": 2, "A#": 3, "Bb": 3, "B": 5},
        "Ab":  {"C": 5, "C#": 6, "Db": 7, "D": 7, "D#": 8, "Eb": 8, "E": 9, "F": 10, "F#": 11, "Gb": 11, "G": 12, "G#": 1,  "Ab": 1, "A": 2, "A#": 3, "Bb": 3, "B": 5},
        "A":  {"C": 4, "C#": 5, "Db": 5, "D": 6, "D#": 7, "Eb": 7, "E": 8, "F": 9, "F#": 10, "Gb": 10, "G": 11, "G#": 12,  "Ab": 12, "A": 1, "A#": 2, "Bb": 2, "B": 3},
        "A#":  {"C": 3, "C#": 4, "Db": 4, "D": 5, "D#": 6, "Eb": 6, "E": 7, "F": 8, "F#": 9, "Gb": 9, "G": 10, "G#": 11,  "Ab": 11, "A": 12, "A#": 1, "Bb": 1, "B": 2},
        "Bb":  {"C": 3, "C#": 4, "Db": 4, "D": 5, "D#": 6, "Eb": 6, "E": 7, "F": 8, "F#": 9, "Gb": 9, "G": 10, "G#": 11,  "Ab": 11, "A": 12, "A#": 1, "Bb": 1, "B": 2},
        "B":  {"C": 2, "C#": 3, "Db": 3, "D": 4, "D#": 5, "Eb": 5, "E": 6, "F": 7, "F#": 8, "Gb": 8, "G": 9, "G#": 10,  "Ab": 10, "A": 11, "A#": 12, "Bb": 12, "B": 1},
    }

    NOTE_POSITION = {
        1 : "C", 
        2 : "C#",
        3 : "D", 
        4 : "D#", 
        5 : "E", 
        6 : "F", 
        7 : "F#", 
        8 : "G", 
        9 : "G#", 
        10 : "A", 
        11 : "A#", 
        12 : "B" 
    }

    HARMONIC_FIELDS = {
        'C': ['C', 'Dm', 'Em', 'F', 'G', 'Am', 'B°'], 
        'C#': ['C°', 'C#', 'Db', 'D#m', 'Ebm', 'Fm', 'F#', 'Gb', 'G#', 'Ab', 'A#m', 'Bbm'], 
        'Db': ['C°', 'C#', 'Db', 'D#m', 'Ebm', 'Fm', 'F#', 'Gb', 'G#', 'Ab', 'A#m', 'Bbm'], 
        'D': ['C#°', 'Db°', 'D', 'Em', 'F#m', 'Gbm', 'G', 'A', 'Bm'], 
        'D#': ['Cm', 'D°', 'D#', 'Fm', 'Gm', 'G#', 'Ab', 'A#', 'Bb'], 
        'Eb': ['Cm', 'D°', 'D#', 'Fm', 'Gm', 'G#', 'Ab', 'A#', 'Bb'], 
        'E': ['C#m', 'Dbm', 'D#°', 'Eb°', 'E', 'F#m', 'Gbm', 'G#m', 'Abm', 'A', 'B'], 
        'F': ['C', 'Dm', 'E°', 'F', 'Gm', 'Am', 'A#', 'Bb'], 
        'F#': ['C#', 'Db', 'D#m', 'Ebm', 'F°', 'F#', 'Gb', 'G#m', 'Abm', 'A#m', 'Bbm', 'B'], 
        'Gb': ['C#', 'Db', 'D#m', 'Ebm', 'F°', 'F#', 'Gb', 'G#m', 'Abm', 'A#m', 'Bbm', 'B'], 
        'G': ['C', 'D', 'Em', 'F#°', 'Gb°', 'G', 'Am', 'Bm'], 
        'G#': ['Cm', 'C#', 'D#', 'Eb', 'Fm', 'G°', 'G#', 'Ab', 'A#m', 'Bbm', 'Bm'], 
        'Ab': ['Cm', 'C#', 'D#', 'Eb', 'Fm', 'G°', 'G#', 'Ab', 'A#m', 'Bbm', 'Bm'], 
        'A': ['C#m', 'Dbm', 'D', 'E', 'F#m', 'Gbm', 'G#°', 'Ab°', 'A', 'Bm'], 
        'A#': ['Cm', 'Dm', 'D#', 'Eb', 'F', 'Gm', 'A°', 'A#', 'Bb'], 
        'Bb': ['Cm', 'Dm', 'D#', 'Eb', 'F', 'Gm', 'A°', 'A#', 'Bb'], 
        'B': ['C#m', 'Dbm', 'D#m', 'Ebm', 'E', 'F#', 'Gb', 'G#m', 'Abm', 'A#°', 'Bb°', 'B']
    }
            
    COMMON_CHARS = "CDEFGAB#bmM45679°/()-+"

    def chord_lines(self, lyric):
        chord_lines_index = []
        index = 0
        for line in lyric.split("\n"):
            number_of_chords = 0
            number_of_words = 0
            words = line.split()
            for word in words:
                if self.is_chord(word): 
                    number_of_chords += 1
                else:
                    number_of_words += 1
            if number_of_chords > number_of_words and line != "": chord_lines_index.append(index)
            index += 1
        return chord_lines_index

    def change_chord(self, chord, old_tone, new_tone):
        basic_note = ""
        notes = []
        for i in chord: 
            if i == "/":
                notes.append(basic_note)
                basic_note = ""
            elif i in "CDEFGAB#b": 
                basic_note += i
        notes.append(basic_note)
        if len(notes) > 1:
            final_chord = self.change_chord(chord.split('/')[0], old_tone, new_tone) + "/" + self.change_chord(chord.split('/')[1], old_tone, new_tone)
            return final_chord
        for i in notes:
            index = self.NOTES_RELATION[old_tone][basic_note]
            for note in self.NOTES_RELATION[new_tone]:
                if self.NOTES_RELATION[new_tone][note] == index:
                    return chord.replace(basic_note, note)

    def is_chord(self, string):
        n = 0
        for i in string:
            if i in self.COMMON_CHARS: n += 1
        if n == len(string): 
            return True
        return False
    
    def order_of_chords(self, chords_list, descendent=True):
        final_list = []
        stop = len(chords_list)
        while len(final_list) < stop:
            greater = ""
            for chord in chords_list:
                if len(chord) > len(greater): 
                    greater = chord
            final_list.append(chords_list.pop(chords_list.index(greater)))
            for i in chords_list:
                if len(i) == len(final_list[-1]):
                    final_list.append(chords_list.pop(chords_list.index(i)))
        return (final_list if descendent else final_list[::-1])

    def get_tone(self, lyric):
        chord_lines = self.chord_lines(lyric)
        n = 0
        counter = {"": 0}
        for i in self.HARMONIC_FIELDS: counter[i] = 0
        for line in lyric.split("\n"):
            if n in chord_lines:
                for tone in self.HARMONIC_FIELDS:
                    for base_chord in self.HARMONIC_FIELDS[tone]:
                        for chord in line.split():
                            if base_chord in chord:
                                counter[tone] += 1
        
        major = ""
        for i in counter:
            if counter[i] >= counter[major]: major = i
        if major == "":
            return "C"
        return major

    def semitone_chord(self, chord, semitones):
        #1 : sharp, -1 : flat, 0 : None
        basic_note = ""
        notes = []
        for index, i in enumerate(chord): 
            if i == "/":
                notes.append(basic_note)
                basic_note = ""
            elif i in "CDEFGAB#": 
                basic_note += i
            elif i == "b" and chord[index - 1] in "CDEFGAB":
                basic_note += i
        notes.append(basic_note)
        if len(notes) > 1:
            final_chord = self.semitone_chord(chord.split('/')[0], semitones) + "/" + self.semitone_chord(chord.split('/')[1], semitones)
            return final_chord
        note = notes[0]
        print(chord, note)
        new_note = self.NOTE_POSITION[(self.NOTES_RELATION["C"][note] + semitones)%12 if (self.NOTES_RELATION["C"][note] + semitones)%12 != 0 else 12]
        return chord.replace(note, new_note)
            
    def semitone_lyric(self, lyric, semitones):
        #1 : sharp, -1 : flat, 0 : None
        new_lyric = []
        chord_lines = self.chord_lines(lyric)
        n = 0
        for line in lyric.split("\n"):
            if n in chord_lines:
                cline = line
                chords = self.order_of_chords(line.split())
                for chord in chords:
                    if self.is_chord(chord): 
                        cline = "@@".join(cline.split(chord))
                parts = cline.split("@@")
                new_line = ""
                x = 0
                for chord in line.split():
                    if self.is_chord(chord):
                        new_line += parts[x] + self.semitone_chord(chord, semitones)
                        x += 1
                new_lyric.append(new_line)
            else:
                new_lyric.append(line)
            n += 1
        return "\n".join(new_lyric)
    
    def change_tone(self, lyric, old_tone="", new_tone=""):
        new_lyric = []
        chord_lines = self.chord_lines(lyric)
        n = 0
        for line in lyric.split("\n"):
            if n in chord_lines:
                cline = line
                chords = self.order_of_chords(line.split())
                for chord in chords:
                    if self.is_chord(chord): 
                        cline = "@@".join(cline.split(chord))
                parts = cline.split("@@")
                new_line = ""
                x = 0
                for chord in line.split():
                    if self.is_chord(chord):
                        new_line += parts[x] + self.change_chord(chord, old_tone, new_tone)
                        x += 1
                new_lyric.append(new_line)
            else:
                new_lyric.append(line)
            n += 1
        return "\n".join(new_lyric)
    
TONECHANGER = ToneChanger()
c = """
Tom: Bm
Bm7
Não consigo tirar da minha cabeça
                                 Bm7/A
Esses olhos que eu nunca vi tão perto

A ponto de bater o cílio no meu

A/G
Não sai da mente o sorriso entreaberto

Eu penso se eu tô errado ou se tô certo

Em cultivar esse bem querer

Bm7
O problema é que já tem alguém do seu lado
                       Bm7/A
E eu me sinto tão errado por tentar me 
aproximar
Remover anúncio
    A/G
Por isso eu mantenho a distancia necessária

Pra que não se esqueça minha cara

E que ao meu lado é um bom lugar
 C#m7(b5)                     F#7
Mais que isso eu não vou fazer não

              Bm7
Apesar de querer

E como eu quero, e como eu quero
             Bm7/A
Apesar de querer

E como eu quero, como eu quero
             A/G
Apesar de querer

E como eu quero, como eu quero
F#7
AiAi
"""