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
    files_to_read.remove(".DS_Store")
    files_to_read = sorted(files_to_read)

    # store the current posting of each file
    cur_posting = []
    
    # create reader, one per file
    for index_file in files_to_read:
        file_reader.append(open(index_file, "r"))
    
    # import postings into cur_posting
    for i in range(len(file_reader)):
        data = file_reader[i].readline()
        if data == "":
            cur_posting.append("eof")
        else:
            cur_posting.append(index_converter(data))
            
    # word list which is corresopnding to cur_posting
    word_list = list()
    
    for post in cur_posting:
        if post == "eof":
            word_list.append("~")
        else:
            word_list.append(post.get_word())
    
    while True:
        # obtain the nmuber of posting needs to be mergerd
        num_to_merge = word_list.count(min(word_list))
        
        # only one minimum posting was found, no need to merge
        if num_to_merge == 1:
            index = word_list.index(min(word_list))
            to_be_merged = cur_posting[index]
            
            # read the next word for file_reader[index]
            data = file_reader[index].readline()
            
            # check if reach end of file
            if data == "":
                cur_posting[index] = "eof"
                word_list[index] = "~"
            else:
                cur_posting[index] = index_converter(data)
                word_list[index] = cur_posting[index].get_word()
                
            # write the signle posting to the disk...
            # (write code here)
            
        else:
            # indicate which cur_posting are about to be merged as a list of indexs
            indexs = [i for i in range(len(word_list)) if word_list[i] == min(word_list)]
            to_be_merged = list()
            
            for i in indexs:
                # gather all postings
                to_be_merged.append(cur_posting[i])
                data = file_reader[i].readline()
                
                # check if reach end of file
                if data == "":
                    cur_posting[i] = "eof"
                    word_list[i] = "~"
                else:
                    cur_posting[i] = index_converter(data)
                    word_list[i] = cur_posting[i].get_word()
                    
            # merge the to_be_merged here...
            # (write code here)
        
        # check if reach end of file for all files
        if cur_posting.count("eof") == len(files_to_read):
            break
