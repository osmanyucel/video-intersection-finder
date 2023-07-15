import json
import os
from tqdm import tqdm


def cleanup(filename: str, rule):
    if not os.path.isfile(filename):
        print("Missing File: " + filename)
        return
    clean_data = list()
    with open(filename, "r+") as fp:
        data = json.load(fp)
    for row in tqdm(data, desc=filename):
        if rule(row):
            clean_data.append(row)
    with open(filename, "w+") as fp:
        json.dump(clean_data, fp)


if __name__ == '__main__':
    cleanup("videos.json", lambda row: os.path.isfile(row["path"]))
    cleanup("pairs.json", lambda row: os.path.isfile(row["path1"]) and os.path.isfile(row["path2"]))
