class doc_tfidf:
    def __init__(self, id, wordlist):
        self.id = id
        self.tf = dict()

        for word in wordlist:
            self.tf[word] = 0
            
    def tf_add(self, word, value):
        if word not in self.tf.keys():
            return
        
        self.tf[word] = value

    def get_tf(self):
        return self.tf

    def get_id(self):
        return self.id