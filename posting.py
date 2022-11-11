class posting:
    def __init__(self, word, freq, pos):
        self.word = word
        self.freq = freq
        self.pos = pos
    
    def freq_add(self, freq_dict):
        self.freq = freq_dict

    def pos_add(self, pos_list):
        self.pos = pos_list
        
    def get_word(self):
        return self.word

    def get_freq(self):
        return self.freq

    def get_pos(self):
        return self.pos
