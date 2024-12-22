import numpy as np
from frequency_extractor import FrequencyExtractor


class NoteDefiner:
    midi_of_notes = {
        48: "C3",  49: "C3#", 50: "D3",  51: "D3#",
        52: "E3",  53: "F3",  54: "F3#", 55: "G3",
        56: "G3#", 57: "A3",  58: "A3#", 59: "B3",
        60: "C4",  61: "C4#", 62: "D4",  63: "D4#",
        64: "E4",  65: "F4",  66: "F4#", 67: "G4",
        68: "G4#", 69: "A4",  70: "A4#", 71: "B4",
        72: "C5",  73: "C5#", 74: "D5",  75: "D5#",
        76: "E5",  77: "F5",  78: "F5#", 79: "G5",
        80: "G5#", 81: "A5",  82: "A5#", 83: "B5",
        84: "C6",  85: "C6#", 86: "D6",  87: "D6#",
        88: "E6",  89: "F6",  90: "F6#", 91: "G6",
        92: "G6#", 93: "A6",  94: "A6#", 95: "B6"
        }

    duration_of_notes = {
        "0.10-0.15":    0.25,
        "0.16-0.30":    0.5,
        "0.31-0.41":    0.75,
        "0.42-0.57":    1,
        "0.58-0.89":    1.5,
        "0.90-1.25":    2,
        "1.26-1.75":    3,
        "1.76-2.50":    4
    }

    def __init__(self, audio_file):
        self.extractor = FrequencyExtractor(audio_file)
        self.freqs = self.extractor.extract_frequencies()

    def notes_dur_definer(self):
        dur_types = []
        for dur in self.freqs:
            for dur_range, note_type in self.duration_of_notes.items():
                start, end = map(float, dur_range.split('-'))
                if start <= round(dur["duration"], 2) <= end:
                    dur_types.append(note_type)
                    break
        return dur_types

    def pitch_definer(self):
        defined_pitches = []

        for freq in self.freqs:
            midi = round(12 * np.log2(freq['frequency'] / 440.0) + 69)
            if midi in self.midi_of_notes:
                defined_pitches.append(self.midi_of_notes[midi])
        return defined_pitches
