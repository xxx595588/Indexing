def read_indexer():
    indexer_dict = {}

    file = "indexer_output.txt"

    with open(file) as f:
        for line in f:
            i = line.split(":")
            indexer_dict[i[0]] = i[2][:-1]

    return indexer_dict