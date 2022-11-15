import json
query = input("Enter your query seperated by spaces: ")
queries = query.split(" ")
allPostings = []


f = open("indexer3.txt", "r")

for line in f:
    loaded = json.loads(line)
    currToken = loaded["token"]
    postings = eval(loaded["postings"])
    if currToken in queries:
        postingsList = list(postings.keys())
        for posting in postingsList:
            allPostings.append(posting)
    #print(loaded["token"] + "->" + str(postings))

f.close()

print(allPostings)