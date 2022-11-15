import json

# find the intersection of given list
def find_intersection(allPostings):
    intersec = list()

    for i in range(1, len(allPostings)):
        if len(intersec) == 0:
            intersec = [id for id in allPostings[i] if id in allPostings[i-1]]
        else:
            intersec = [id for id in allPostings[i] if id in intersec]

    return intersec

def search():
    query = input("Enter your query seperated by spaces: ")
    queries = query.split(" ")

    # list of query words' docID, use for finding intersection
    allPostings = list()

    # dictionary of id/freq, will be used in tf-idf calculation
    id_freq_list = list()

    # sort the query for better performance
    queries = sorted(queries)

    f = open("indexer2.txt", "r")

    # only search for the word in query
    for word in queries:
        line = f.readline()
        loaded = json.loads(line)
        
        # find the first matched word with queries
        while loaded["token"] != word:
            line = f.readline()

            if line == "":
                break

            loaded = json.loads(line)

        if line == "":
            break
        
        # store the info
        postings = eval(loaded["postings"])
        id_freq_list.append(postings)
        allPostings.append(postings.keys())

    f.close()

    intersec = find_intersection(allPostings)

    # calculate the score...