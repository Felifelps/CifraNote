import re

class ToneChanger:
    """
    This class changes the tone of a lyric
    
    ToneChanger.semitone_lyric(
        quantity, # Any integer. Use negative numbers to down semitones
        lyric # Str with the lyric
    )
    """

    PATTERN_CHARS = '()+-'

    NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    ALTERNATIVE_NOTES =  ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    NOTES_PATTERN = f"({'|'.join(set(NOTES + ALTERNATIVE_NOTES))})"

    COMMON_CHARS = "[mM123456789°/()+-]"
    CHORD_PATTERN = fr"{NOTES_PATTERN}{{1}}({COMMON_CHARS}*){NOTES_PATTERN}?(\s+|\n)"

    @classmethod
    def format_pattern(cls, pattern):
        # Formats pattern to handle metacharacteres
        for char in cls.PATTERN_CHARS:
            pattern = pattern.replace(char, fr'\{char}')
        return fr'{pattern}'

    @classmethod
    def semitone_chord(cls, quantity, match_list):
        # Gets the match_list and transforms into a list
        match_list = list(match_list)

        # Loops into match_list, skipping 1 and 3 values
        for index, group in enumerate(match_list):
            # If the 2 group is None also skip
            if index in [1, 3] or not group:
                continue

            # Gets the note value
            search = cls.NOTES if group in cls.NOTES else cls.ALTERNATIVE_NOTES
            note_value = search.index(group)

            # Sets new note and adds it into match_list
            new_note = search[(note_value + quantity)%len(search)]
            match_list[index] = new_note

        return "".join(match_list)

    @classmethod
    def semitone_lyric(cls, quantity, data):
        # Gets all the chords in the data
        result = re.findall(cls.CHORD_PATTERN, data)

        # Transformed data is the final lyric
        transformed_data = ''

        # Loops into the chords
        for match_list in result:
            # match_list = ('main_note', 'common_chars', 'bass_note', 'chord_end')
            chord = ''.join(match_list)

            # Gets the chord position
            match = re.search(cls.format_pattern(chord), data)
            pos = match.span()

            # Gets the new chord
            new_chord = cls.semitone_chord(quantity, match_list)

            # Saves the new_chord and updates data
            transformed_data += data[:pos[0]] + new_chord
            data = data[pos[1]:]

        # Set the end of the lyric
        transformed_data += data

        return transformed_data
