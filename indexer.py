import os
import json
import nltk
import re
import time
from bs4 import BeautifulSoup
from nltk.corpus import words

stop_word = set(['', 'a', 'able', 'about', 'above', 'abst', 'accordance', 'according', 'accordingly', 'across', 'act', 'actually', 'added', 'adj', 'affected', 'affecting', 'affects', 'after', 'afterwards', 'again', 'against', 'ah', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'an', 'and', 'announce', 'another', 'any', 'anybody', 'anyhow', 'anymore', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apparently', 'approximately', 'are', 'aren', 'arent', 'arise', 'around', 'as', 'aside', 'ask', 'asking', 'at', 'auth', 'available', 'away', 'awfully', 'b', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'begin', 'beginning', 'beginnings', 'begins', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'between', 'beyond', 'biol', 'both', 'brief', 'briefly', 'but', 'by', 'c', 'ca', 'came', 'can', 'cannot', "can't", 'cause', 'causes', 'certain', 'certainly', 'co', 'com', 'come', 'comes', 'contain', 'containing', 'contains', 'could', 'couldnt', 'd', 'date', 'did', "didn't", 'different', 'do', 'does', "doesn't", 'doing', 'done', "don't", 'down', 'downwards', 'due', 'during', 'e', 'each', 'ed', 'edu', 'effect', 'eg', 'eight', 'eighty', 'either', 'else', 'elsewhere', 'end', 'ending', 'enough', 'especially', 'et', 'et-al', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'except', 'f', 'far', 'few', 'ff', 'fifth', 'first', 'five', 'fix', 'followed', 'following', 'follows', 'for', 'former', 'formerly', 'forth', 'found', 'four', 'from', 'further', 'furthermore', 'g', 'gave', 'get', 'gets', 'getting', 'give', 'given', 'gives', 'giving', 'go', 'goes', 'gone', 'got', 'gotten', 'h', 'had', 'happens', 'hardly', 'has', "hasn't", 'have', "haven't", 'having', 'he', 'hed', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'heres', 'hereupon', 'hers', 'herself', 'hes', 'hi', 'hid', 'him', 'himself', 'his', 'hither', 'home', 'how', 'howbeit', 'however', 'hundred', 'i', 'id', 'ie', 'if', "i'll", 'im', 'immediate', 'immediately', 'importance', 'important', 'in', 'inc', 'indeed', 'index', 'information', 'instead', 'into', 'invention', 'inward', 'is', "isn't", 'it', 'itd', "it'll", 'its', 'itself', "i've", 'j', 'just', 'k', 'keep\tkeeps', 'kept', 'kg', 'km', 'know', 'known', 'knows', 'l', 'largely', 'last', 'lately', 'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', 'lets', 'like', 'liked', 'likely', 'line', 'little', "'ll", 'look', 'looking', 'looks', 'ltd', 'm', 'made', 'mainly', 'make', 'makes', 'many', 'may', 'maybe', 'me', 'mean', 'means', 'meantime', 'meanwhile', 'merely', 'mg', 'might', 'million', 'miss', 'ml', 'more', 'moreover', 'most', 'mostly', 'mr', 'mrs', 'much', 'mug', 'must', 'my', 'myself', 'n', 'na', 'name', 'namely', 'nay', 'nd', 'near', 'nearly', 'necessarily', 'necessary', 'need', 'needs', 'neither', 'never', 'nevertheless', 'new', 'next', 'nine', 'ninety', 'no', 'nobody', 'non', 'none', 'nonetheless', 'noone', 'nor', 'normally', 'nos', 'not', 'noted', 'nothing', 'now', 'nowhere', 'o', 'obtain', 'obtained', 'obviously', 'of', 'off', 'often', 'oh', 'ok', 'okay', 'old', 'omitted', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'ord', 'other', 'others', 'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'owing', 'own', 'p', 'page', 'pages', 'part', 'particular', 'particularly', 'past', 'per', 'perhaps', 'placed', 'please', 'plus', 'poorly', 'possible', 'possibly', 'potentially', 'pp', 'predominantly', 'present', 'previously', 'primarily', 'probably', 'promptly', 'proud', 'provides', 'put', 'q', 'que', 'quickly', 'quite', 'qv', 'r', 'ran', 'rather', 'rd', 're', 'readily', 'really', 'recent', 'recently', 'ref', 'refs', 'regarding', 'regardless', 'regards', 'related', 'relatively', 'research', 'respectively', 'resulted', 'resulting', 'results', 'right', 'run', 's', 'said', 'same', 'saw', 'say', 'saying', 'says', 'sec', 'section', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'selves', 'sent', 'seven', 'several', 'shall', 'she', 'shed', "she'll", 'shes', 'should', "shouldn't", 'show', 'showed', 'shown', 'showns', 'shows', 'significant', 'significantly', 'similar', 'similarly', 'since', 'six', 'slightly', 'so', 'some', 'somebody', 'somehow', 'someone', 'somethan', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'specifically', 'specified', 'specify', 'specifying', 'still', 'stop', 'strongly', 'sub', 'substantially', 'successfully', 'such', 'sufficiently', 'suggest', 'sup', 'sure\tt', 'take', 'taken', 'taking', 'tell', 'tends', 'th', 'than', 'thank', 'thanks', 'thanx', 'that', "that'll", 'thats', "that've", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'thered', 'therefore', 'therein', "there'll", 'thereof', 'therere', 'theres', 'thereto', 'thereupon', "there've", 'these', 'they', 'theyd', "they'll", 'theyre', "they've", 'think', 'this', 'those', 'thou', 'though', 'thoughh', 'thousand', 'throug', 'through', 'throughout', 'thru', 'thus', 'til', 'tip', 'to', 'together', 'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying', 'ts', 'twice', 'two', 'u', 'un', 'under', 'unfortunately', 'unless', 'unlike', 'unlikely', 'until', 'unto', 'up', 'upon', 'ups', 'us', 'use', 'used', 'useful', 'usefully', 'usefulness', 'uses', 'using', 'usually', 'v', 'value', 'various', "'ve", 'very', 'via', 'viz', 'vol', 'vols', 'vs', 'w', 'want', 'wants', 'was', 'wasnt', 'way', 'we', 'wed', 'welcome', "we'll", 'went', 'were', 'werent', "we've", 'what', 'whatever', "what'll", 'whats', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'wheres', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whim', 'whither', 'who', 'whod', 'whoever', 'whole', "who'll", 'whom', 'whomever', 'whos', 'whose', 'why', 'widely', 'willing', 'wish', 'with', 'within', 'without', 'wont', 'words', 'world', 'would', 'wouldnt', 'www', 'x', 'y', 'yes', 'yet', 'you', 'youd', "you'll", 'your', 'youre', 'yours', 'yourself', 'yourselves', "you've", 'z', 'zero'])
ori_loc = os.getcwd()

# focuse on there tag for indexing
tag = ["title", "p", "h1", "h2", "h3", "h4", "h5", "h6"]

# The structure of the index is {word: [documnt ID]}, key is a string and value is a list
index = dict()

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

    for i in range(len(tokens)):
        if tokens[i] in stop_word or len(tokens[i]) == 1 :
            if tokens[i] not in tbr:
                tbr.add(tokens[i])
        elif re.search("[^a-z]", tokens[i]):
            if tokens[i] not in tbr:
                tbr.add(tokens[i])

    # clean up for the tokens
    tokens = set([w for w in tokens if w not in tbr])

    return tokens

# fetch all json file and tokenize the text from its content
def fetch_data():
    global ori_loc
    path = input("Input the path: ")
    os.chdir(path)

    global index, total_doc, indexed_doc, dup_doc

    for web_folder in os.listdir():
        os.chdir(web_folder)
        for html_file in os.listdir():

            tokens = tokenize(html_file)
            hash_num = hash(frozenset(tokens))
            tokens = list(tokens)

            total_doc += 1

            if hash_num not in dup:
                indexed_doc += 1
                dup.add(hash_num)
                for w in tokens:
                    if index.get(w) is None:
                        index[w] = [html_file]
                    else:
                        index[w].append(html_file)

                print(tokens)
            else:
                dup_doc += 1
           
        # go to parent folder
        os.chdir(os.path.dirname(os.getcwd()))

    os.chdir(ori_loc)

# generate the ouput file
def write_file():
    global index, total_doc, indexed_doc, dup_doc

    index = dict(sorted(index.items(), key=lambda item: item[0]))

    for i in index:
        index[i] = sorted(index[i])

    # ouput the indexer:
    # word: frequency -> ID list(posting)
    f_1 = open("indexer_output.txt", "w")
    for i in index:
        f_1.write(f"{i}: {len(index[i])} -> ID: {index[i]}\n")
    f_1.close()

    # contain some general info for the indexing process
    f_2 = open("general_output.txt", "w")
    file_stat = os.stat("indexer_output.txt")
    file_size = file_stat.st_size / 1000
    elapsed_time = end_time - start_time
    f_2.write(f"Total number of documents: {total_doc}\n"
                + f"Number of indexed documents: {indexed_doc}\n"
                + f"Numbe of duplicated documents: {dup_doc}\n"
                + f"Total runtime: {elapsed_time} seconds\n"
                + f"Number of unique tokens: {len(index)}\n"
                + f"Total size of index: {file_size}KB")


def main():
    global start_time
    start_time = time.time()

    fetch_data()

    global end_time
    end_time = time.time()

    write_file()

if __name__ == "__main__":
   main()