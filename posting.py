class posting:
    def __init__(self, word, freq, pos, imp_freq, imp_pos):
        self.word = word
        self.freq = freq
        self.pos = pos
        self.imp_freq = imp_freq
        self.imp_pos = imp_pos
    
    def freq_add(self, freq_dict):
        self.freq = freq_dict

    def pos_add(self, pos_list):
        self.pos = pos_list

    def imp_freq_add(self, imp_freq_dict):
        self.imp_freq = imp_freq_dict

    def imp_pos_add(self, imp_pos_list):
        self.imp_pos = imp_pos_list

    def get_word(self):
        return self.word

    def get_freq(self):
        return self.freq

    def get_pos(self):
        return self.pos

    def get_imp_freq(self):
        return self.imp_freq

    def get_imp_pos(self):
        return self.imp_pos
