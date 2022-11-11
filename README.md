# Indexing

The indexer.py will read all given json files to create the inverted index.
The structure of the index is a dictionary whose key is word and value is posting.
```
word: posting
```
\
The structure of postion is defined in `posting.py`
```
class posting:
    def __init__(self, word, freq, pos):
        self.word = word
        self.freq = freq
        self.pos = pos
```
* freq is the dictionary whose key is docID and value is the frequency of the word
* pos is the dictionary whose key is docID and value is the list of position that word appeares

\
The url can be looked up from the url_lookup by docID, url_lookup is a dictionary whose key is docID and value is url
```
docID: url
```
