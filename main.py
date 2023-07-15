import json
import shutil
from tqdm import tqdm

from Video import Video


def find_all_overlaps(videos):
    for i in range(len(videos)):
        for j in range(i + 1, len(videos)):
            print("{}\t{}\t{}\t{}\t{}".format(videos[i].path,
                                              len(videos[i].frames),
                                              videos[j].path,
                                              len(videos[j].frames),
                                              videos[i].find_overlap(videos[j])))

def findoverlap(tuple1):
    v1 = tuple1[0]
    v2 = tuple1[1]
    d = {"path1": v1.path, "frames1": len(v1.frames),
         "path2": v2.path, "frames2": len(v2.frames),
         "overlap": v1.find_overlap(v2)}
    return d

def main_process():
    videos = list()
    prepared = list()

    try:
        with open("videos.json", "r+") as fp:
            data = json.load(fp)
            for file in data:
                prepared.append(file["path"])
                videos.append(Video(file["path"], file["frames"]))
        videos.sort()
    except:
        raise
    processed_pairs = set()
    pairs = list()
    try:
        with open("pairs.json", "r+") as fp:
            pairs = json.load(fp)
            for pair in pairs:
                processed_pairs.add((pair["path1"], pair["path2"]))
    except:
        # print("PAIRS.JSON IS BROKEN FALLING BACK TO BACKUP")
        # with open("pairs.bak.json", "r+") as fp:
        #     pairs = json.load(fp)
        #     for pair in pairs:
        #         processed_pairs.add((pair["path1"], pair["path2"]))
        pass
    for i in range(len(videos)):
        is_new = False
        for j in tqdm(range(i + 1, len(videos)), desc=videos[i].path):
            if (videos[i].path, videos[j].path) in processed_pairs:
                continue
            is_new = True
            outputs = findoverlap((videos[i], videos[j]))
            pairs.append(outputs)
        # if is_new:
        #     shutil.copyfile("pairs.json", "pairs.bak.json")
        #     with open("pairs.json", "w+") as fp:
        #         json.dump(pairs, fp)
    # shutil.copyfile("pairs.json", "pairs.bak.json")
    with open("pairs.json", "w+") as fp:
        json.dump(pairs, fp)


if __name__ == '__main__':
    main_process()