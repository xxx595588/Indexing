import json
import time
import linecache
import nltk
from posting import posting
from nltk import ngrams

stemmer = nltk.stem.SnowballStemmer("english")
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

# find the intersection of given list
def find_intersection(allPostings):
    intersec = list()

    for i in range(1, len(allPostings)):
        if len(intersec) == 0:
            intersec = [id for id in allPostings[i] if id in allPostings[i-1]]
        else:
            intersec = [id for id in allPostings[i] if id in intersec]

    return intersec

def binary_search(f, start, end, word, indexer_list, allPostings):

    # valid conditioin
    if end >= start:
        mid = (start + end) // 2

        line = linecache.getline("merged_indexer.txt", mid)
        loaded = json.loads(line)

        # compare with mid
        if word == loaded["token"]:
            postings = posting(word, eval(loaded["postings"]), eval(loaded["positions"]))
            indexer_list.append(postings)
            allPostings.append(postings.get_freq().keys())
        # search start to mid - 1
        elif word < loaded["token"]:
            binary_search(f, start, mid - 1, word, indexer_list, allPostings)
        # search mid + 1 to end
        else:
            binary_search(f, mid + 1, end, word, indexer_list, allPostings)
        
    
def search():
    query = input("Enter your query seperated by spaces: ")
    queries = query.split(" ")

    queries = [stemmer.stem(w.lower()) for w in queries]


    # doing ngram
    ngram_iteration = [2]
    ngram_temp = list()

    for iter in ngram_iteration:
        ngramTokens = list(ngrams(queries, iter))
        for ngram in ngramTokens:
            ngram_temp.append(ngram)

    queries += ngram_temp

    for i in range(len(queries)):
        if(type(queries[i]) == tuple):
            queries[i] = " ".join(list(queries[i]))

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

    for word in queries:
        start_pos = indicator[alphabet.index(word[0])]
        end_pos = indicator[alphabet.index(word[0]) + 1] - 1
        f = open("merged_indexer.txt", "r")
        binary_search(f, start_pos, end_pos, word, indexer_list, allPostings)
        f.close()

    if len(allPostings) != 1:
        intersec = find_intersection(allPostings)
    else:
        intersec = list(allPostings[0])

    end = time.time()

    url_result_list = list()

    print(intersec)

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
