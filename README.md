# Search-Engine-Group-10

## - Indexing

The indexer.py will read all given json files to create the inverted index.
The structure of the index is a dictionary whose key is word and value is posting.
```
word: posting
```
\
The structure of postion is defined in `posting.py`
```
class posting:
    def __init__(self, word, freq, pos, imp_freq, imp_pos):
        self.word = word
        self.freq = freq
        self.pos = pos
        self.imp_freq = imp_freq
        self.imp_pos = imp_pos
```
* freq is the dictionary whose key is docID and value is the frequency of the word
* pos is the dictionary whose key is docID and value is the list of position that word appeares

\
The url can be looked up from the url_lookup by docID, `url_lookup` is a dictionary whose key is docID and value is url
```
docID: url
```
\
For example, the word `helen` has data structure like:
```
{"token":"helen", "postings":"{10014: 1, 20940: 1}", "positions":"{10014: [4], 20940: [1]}", "imp_postings":"{6312: 2, 10014: 1, 10473: 1, 20940: 1, 21566: 2}", "imp_positions":"{6312: [3, 6], 10014: [4], 10473: [1], 20940: [1], 21566: [3, 5]}"}
```

\
According to the considerable data collection, the program will store the partial indexing files to `index files` folder when it reachs certain size.
Finally, all partial indexing files will be merged into one file called `merged_indexer`, please reference to `merge.py`.


## - Retrieval

Most of the retrieving process are done in `search.py`, the search adopts binary search to retrieve given query in the corpus which is `merged_indexer`.

The search adopts tf.idf score for ranking computation:


### Log-frequency weighting:

$$
w_{t, d} = 
\begin{cases} 
    \text{$1+ log_{10} tf_{(t, d)}$, if $tf_{(t, d)} > 0$}\\ 
    \text{0, Otherwise}\\ 
\end{cases} 
$$

### Inverse document frequency:

$$idf_{t} = log_{10} (N/df_{t})$$

### tf-idf weighting:

$$tf.idf_{(t, d)} = (1+log_{10}tf_{(t, d)}) \times log_{10} (N/df_{t}) $$

### Score of query of a document:

$$Score(q, d) = \sum_{t \in q \cap d} tf.idf_{(t, d)}$$
