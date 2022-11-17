import json
import time
import linecache
import nltk
from posting import posting
from nltk import ngrams

stemmer = nltk.stem.SnowballStemmer("english")
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
ngram_iteration = [2, 3]

# find the intersection of given list
def find_intersection(allPostings):
    intersec = list()

    for i in range(1, len(allPostings)):
        if len(intersec) == 0:
            intersec = [id for id in allPostings[i] if id in allPostings[i-1]]
        else:
            intersec = [id for id in allPostings[i] if id in intersec]

    return intersec

# implement binary search to find the target word in the file
def binary_search(mid_list, start, end, word, indexer_list, allPostings):

    # valid conditioin for binary search
    if end >= start:
        mid = (start + end) // 2

        # get the mid-th word in the file
        line = linecache.getline("merged_indexer.txt", mid)
        loaded = json.loads(line)

        mid_list.append(mid)

        # compare word with mid-th word
        if word == loaded["token"]:
            postings = posting(word, eval(loaded["postings"]), eval(loaded["positions"]))
            indexer_list.append(postings)
            allPostings.append(postings.get_freq().keys())
            return mid_list
        # search start to mid - 1
        elif word < loaded["token"]:
            return binary_search(mid_list, start, mid - 1, word, indexer_list, allPostings)
        # search mid + 1 to end
        else:
            return binary_search(mid_list, mid + 1, end, word, indexer_list, allPostings)
    # word isn't present in the file
    else:
        return list()
        
    
def search():
    query = input("Enter your query seperated by spaces: ")
    queries = nltk.word_tokenize(query)
    queries = [stemmer.stem(w.lower()) for w in queries]

    # doing ngram
    global ngram_iteration
    ngram_temp = list()

    for iter in ngram_iteration:
        ngramTokens = list(ngrams(queries, iter))
        for ngram in ngramTokens:
            ngram_temp.append(ngram)

    queries += ngram_temp

    for i in range(len(queries)):
        if(type(queries[i]) == tuple):
            queries[i] = " ".join(list(queries[i]))

    # open indicator.txt file which can boost the binary search speed
    f = open("indicator.txt", "r")
    indicator = eval(f.readline()[:-1])

    # list of query words' docID, use for finding intersection
    allPostings = list()

    # dictionary of id/freq, will be used in tf-idf calculation
    indexer_list = list()

    # sort the query for better performance
    queries = sorted(queries)
    global alphabet
    
    start = time.time()

    # partition query's word into 26 sublist by their starting alphabet
    partition_word = [None]*26
    for word in queries:
        if partition_word[alphabet.index(word[0])] is None:
            partition_word[alphabet.index(word[0])] = [word]
        else:
            partition_word[alphabet.index(word[0])].append(word)

    for sublist in partition_word:
        if sublist is not None:
            first_time = True
            # collect all mid value to help following search in the same sublist
            mid_list = list()
            for word in sublist:
                # original start and end position for corresponding alphabet
                start_pos = indicator[alphabet.index(word[0])]
                end_pos = indicator[alphabet.index(word[0]) + 1] - 1

                if first_time:
                    mid_list = binary_search(mid_list, start_pos, end_pos, word, indexer_list, allPostings)
                    first_time = False
                else:
                    # check with mid_list to trim the search range
                    for pos in mid_list:
                        line = linecache.getline("merged_indexer.txt", pos)
                        loaded = json.loads(line)

                        if word < loaded["token"]:
                            if pos < end_pos:
                                end_pos = pos
                        
                        if word > loaded["token"]:
                            if pos > start_pos:
                                start_pos = pos

                    mid_list = binary_search(mid_list, start_pos, end_pos, word, indexer_list, allPostings)
    
    if len(allPostings) != 1:
        intersec = find_intersection(allPostings)
    else:
        intersec = list(allPostings[0])

    end = time.time()  

    url_result_list = list()

    for id in intersec:
        line = linecache.getline("url_lookup.txt", id)
        loaded = json.loads(line)
        url_result_list.append(loaded["url"])

    if len(url_result_list) == 0:
        print("No matched result was found.")
    else:
        for i in range(len(url_result_list)):
            print(f"{i + 1}. {url_result_list[i]}")

    print(f"search time is: {end-start} sec")

search()
