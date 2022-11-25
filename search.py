import json
import time
import linecache
import nltk
import math
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

def binary_search(mid_list, start, end, word, indexer_list, allPostings):

    # valid conditioin
    if end >= start:
        mid = (start + end) // 2

        line = linecache.getline("merged_indexer.txt", mid)
        loaded = json.loads(line)

        mid_list.append(mid)

        # compare with mid
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
    else:
        return list()

# calculate the tf-idf for query
def tf_idf_query(raw_query, queries, indexer_list):
    line = linecache.getline("general_output.txt", 2)
    num_indexed_doc = int(line.split(":")[-1])

    # get the tf-idf for query
    tf_query = list()
    idf_query = list()
    found_terms = list()
    found_term_freq = list()

    for posting in indexer_list:
        found_terms.append(posting.get_word())
        found_term_freq.append(posting.get_freq())

    for term in queries:
        if term not in found_terms:
            tf_query.append(0)
            idf_query.append(0)
        else:
            index = found_terms.index(term)
            tf_query.append(1 + math.log(raw_query.count(term), 10))
            idf_query.append(math.log(num_indexed_doc/len(found_term_freq[index]), 10))

    tf_idf_query = list()
    length_query = 0

    # calculate tf_idf without normalization
    for i in range(len(tf_query)):
        tf_idf_query.append(tf_query[i] * idf_query[i])
        length_query += tf_idf_query[i]**2

    length_query = math.sqrt(length_query)

    for i in range(len(tf_query)):
        tf_idf_query[i] = tf_idf_query[i]/length_query

    return tf_idf_query


def ranking(raw_query, queries, indexer_list):
    tf_idf_q = tf_idf_query(raw_query, queries, indexer_list)

    
def search():
    query = input("Enter your query seperated by spaces: ")
    queries = nltk.word_tokenize(query)

    queries = [stemmer.stem(w.lower()) for w in queries]

    # doing ngram
    ngram_iteration = [2, 3]
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

    # list of query words' docID, used for finding intersection
    allPostings = list()

    # dictionary of posting, will be used in tf-idf calculation
    indexer_list = list()

    # sort the query for better performance
    queries = sorted(queries)
    global alphabet
    
    start = time.time()

    # partition word into 26 sublist by starting alphabet
    partition_word = [None]*26
    for word in queries:
        if partition_word[alphabet.index(word[0])] is None:
            partition_word[alphabet.index(word[0])] = [word]
        else:
            partition_word[alphabet.index(word[0])].append(word)

    for sublist in partition_word:
        if sublist is not None:
            #print(sublist)
            counter = 0
            # collect all mid value to help following search in same sublist
            mid_list = list()
            for word in sublist:
                # original start and end position
                start_pos = indicator[alphabet.index(word[0])]
                end_pos = indicator[alphabet.index(word[0]) + 1] - 1
                #print(f"original start is {start_pos}, end is {end_pos}")

                if counter == 0:
                    mid_list = binary_search(mid_list, start_pos, end_pos, word, indexer_list, allPostings)
                    counter += 1
                else:
                    #print(f"now is {word}")
                    for pos in mid_list:
                        line = linecache.getline("merged_indexer.txt", pos)
                        loaded = json.loads(line)

                        if word < loaded["token"]:
                            if pos < end_pos:
                                end_pos = pos
                                #print(f"changing end to {pos}")
                        
                        if word > loaded["token"]:
                            if pos > start_pos:
                                start_pos = pos
                                #print(f"changing start to {pos}")

                    #print(f"new start is {start_pos}, end is {end_pos}")
                    mid_list = binary_search(mid_list, start_pos, end_pos, word, indexer_list, allPostings)
    
    if len(allPostings) != 1:
        intersec = find_intersection(allPostings)
    else:
        intersec = list(allPostings[0])

    result_size = len(intersec)


    ranking(query, queries, indexer_list)

    # get top 5 results
    if result_size > 5:
        intersec = intersec[:5]

    end = time.time()  

    url_result_list = list()

    # look up the url
    for id in intersec:
        line = linecache.getline("url_lookup.txt", id)
        loaded = json.loads(line)
        url_result_list.append(loaded["url"])

    if len(url_result_list) == 0:
        print("No matched result was found.")
    else:
        for i in range(len(url_result_list)):
            print(f"{i + 1}. {url_result_list[i]}")

    print(f"\n{result_size} results ({end-start} seconds)")
    print(f"-----------------------------end of search-----------------------------")

search()
