import os
import posting

def index_converter(raw_data):
    # convert raw_data into word: posting
    word = raw_data.split("-> ")[0].split(":")[0]
    raw_posting = raw_data.split("-> ")[1][:-1]

    id_freq = eval(raw_posting.split(", ID/pos: ")[0][9:])
    id_pos = eval(raw_posting.split(", ID/pos: ")[1])

    return posting.posting(word, id_freq, id_pos)

def merge():
    path = "index files"
    os.chdir(path)

    # list of index file to be merged
    files_to_read = os.listdir()
    file_reader = []

    # remove for mac only, windows can ignore
    files_to_read = sorted(files_to_read)

    # store the current posting of each file
    cur_posting = []
    
    # create reader, one per file
    for index_file in files_to_read:
        file_reader.append(open(index_file, "r"))

    for i in range(len(file_reader)):
        data = file_reader[i].readline()
        if data == "":
            cur_posting.append("eof")
        else:
            cur_posting.append(index_converter(data))
            
    # do some merge algo here...
