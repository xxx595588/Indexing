import os
import json
import nltk
import re
import time
from bs4 import BeautifulSoup

ori_loc = os.getcwd()

# focuse on these tags for indexing
tag = ["title", "p", "h1", "h2", "h3", "h4", "h5", "h6"]

# map an id to url, the structure is {url: ID}
url_map = dict()

# reversed version of url_map (for better lookup)
url_lookup = dict()

# The structure of the index_freq is {word: {ID: freq}}, key is a string and value is a dictionary
index_freq = dict()

# The structure of the index_pos is {word: [(ID, pos)]}, key is a string and value is a list of tuple
index_pos = dict()

# Set contain indexed document to avoid same content
dup = set()

# Number of total document
total_doc = 0

# Number of indexed document
indexed_doc = 0

# Number of duplicated document which didn't be indexed
dup_doc = 0

# Time calculator
start_time = None
end_time = None

# tokenize the content fetch from the json file
def tokenize(html_file):
    global tag

    raw_data = json.load(open(html_file))
    # get the content
    soup = BeautifulSoup(raw_data["content"], features = "html.parser")
    tag_list = soup.find_all(tag, text=True)

    temp_ter = ""

    for s in tag_list:
        temp_ter += s.text
        temp_ter += "."

    tokens = nltk.word_tokenize(temp_ter)
    tokens = [t.lower() for t in tokens]

    # to be removed word set (number or special character)
    tbr = set()

    for w in tokens:
        if len(w) == 1 or re.search("[^a-z]", w):
            tbr.add(w)

    tokens_list = [w for w in tokens if w not in tbr]

    # dictionary of word/freq
    tokens_freq = dict()
    # dictionary of word/pos
    tokens_pos = dict()

    for i in range(len(tokens_list)):
        # count for the word's frequency
        if tokens_list[i] in tokens_freq:
            tokens_freq[tokens_list[i]] += 1
        else:
            tokens_freq[tokens_list[i]] = 1

        # indicate the word's position
        if tokens_list[i] in tokens_pos:
            tokens_pos[tokens_list[i]].append(i+1)
        else:
            tokens_pos[tokens_list[i]] = [i+1]

    return tokens_freq, tokens_pos, raw_data["url"]

# fetch all json file and tokenize the text from its content
def fetch_data():
    global ori_loc, url_map
    path = input("Input the path: ")
    os.chdir(path)

    global index_freq, total_doc, indexed_doc, dup_doc

    for web_folder in os.listdir():
        os.chdir(web_folder)
        for html_file in os.listdir():
            # words with frequency in dict -> words: freq
            tokens_freq, tokens_pos, url = tokenize(html_file)

            print(f"Processing {url}")

            # set of tokens without repeating
            tokens = tokens_freq.keys()
            hash_num = hash(frozenset(set(tokens)))

            total_doc += 1

            if hash_num not in dup:
                indexed_doc += 1
                dup.add(hash_num)
                url_map[url] = len(url_map) + 1

                for w in tokens:
                    # section for index frequency
                    if index_freq.get(w) is None:
                        new_dict = dict()
                        new_dict[url_map[url]] = tokens_freq[w]
                        index_freq[w] = new_dict
                    else:
                        index_freq[w][url_map[url]] = tokens_freq[w]

                    # section for index position
                    if index_pos.get(w) is None:
                        index_pos[w] = list()
                    
                    pos_list = tokens_pos[w]
                    for i in pos_list:
                        index_pos[w].append((url_map[url], i))
            else:
                dup_doc += 1

        # go to parent folder
        os.chdir(os.path.dirname(os.getcwd()))

    os.chdir(ori_loc)

# generate the ouput file
def write_file():
    global index_freq, index_pos, url_map, url_lookup, total_doc, indexed_doc, dup_doc

    # sort the words
    index_freq = dict(sorted(index_freq.items(), key=lambda item: item[0]))
    index_pos = dict(sorted(index_pos.items(), key=lambda item: item[0]))

    # sort the frequency by ID in index_freq
    for i in index_freq:
        index_freq[i] = dict(sorted(index_freq[i].items(), key=lambda item: item[0]))


    # construct the url lookup table
    url_lookup = {id: url for url, id in url_map.items()}

    # ouput the index with frequency:
    # {word: {ID: freq}}
    f = open("indexer_freq.txt", "w")
    for i in index_freq:
        f.write(f"{i}: {len(index_freq[i])} -> ID/freq: {index_freq[i]}\n")
    f.close()

    f = open("indexer_pos.txt", "w")
    for i in index_pos:
        f.write(f"{i} -> ID/pos: {index_pos[i]}\n")
    f.close()

    # output the url map
    f = open("url_map.txt", "w")
    for i in url_map:
        f.write(f"{i}: {url_map[i]}\n")
    f.close()

    # output the url lookup table
    f = open("url_lookup.txt", "w")
    for i in url_lookup:
        f.write(f"{i}: {url_lookup[i]}\n")
    f.close()

    # contain some general info for the indexing process
    f = open("general_output.txt", "w")
    file_size = (os.stat("indexer_freq.txt").st_size + os.stat("indexer_pos.txt").st_size)/ 1000
    elapsed_time = end_time - start_time
    f.write(f"Total number of documents: {total_doc}\n"
                + f"Number of indexed documents: {indexed_doc}\n"
                + f"Number of duplicated documents: {dup_doc}\n"
                + f"Total runtime: {elapsed_time} seconds\n"
                + f"Number of unique tokens: {len(index_freq)}\n"
                + f"Total size of index: {file_size}KB")
    f.close()

def main():
    global start_time
    start_time = time.time()

    fetch_data()

    global end_time
    end_time = time.time()

    write_file()

if __name__ == "__main__":
    main()