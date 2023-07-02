def read_classification_from_file(fpath):
    spam_dict = dict()
    with open(fpath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            split_line = line.split()
            spam_dict.get(split_line[0])
            spam_dict[split_line[0]] = split_line[1]
    return spam_dict