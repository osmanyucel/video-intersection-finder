import json
import pprint
import os


def show_all(pairs, limit=20):
    for row in pairs:
        if row["overlap"] > limit:
            if row["overlap"] / row["frames1"] > .95 or row["overlap"] / row["frames2"] > .95:
                print('\033[92m' + str(row) + '\033[0m')
            else:
                print(row)


def show_complete_overlaps(pairs):
    for row in pairs:
        if row["overlap"] > 0 and (row["overlap"] / row["frames1"] > 0.95 or row["overlap"] / row["frames2"] > 0.95):
            print(row)


def show_particular_video(pairs, file_filter, limit=1):
    output = list()
    printed = False
    for row in pairs:
        if row["overlap"] >= limit and (file_filter in row["path1"] or file_filter in row["path2"]):
            if not printed:
                print((row["frames1"] if file_filter in row["path1"] else row["frames2"],
                       row["path1"] if file_filter in row["path1"] else row["path2"]))
                printed = True
            # print(row)
            output.append((row["overlap"],
                           row["frames2"] if file_filter in row["path1"] else row["frames1"],
                           row["path2"] if file_filter in row["path1"] else row["path1"]))
    output = sorted(output, key=lambda row: row[2])
    for o in output:
        if o[1] > 0 and o[0] / o[1] > .95:
            print('\033[92m' + str(o) + '\033[0m')
        else:
            print(o)


def show_sets(pairs, limit=20):
    sets = list()
    for row in pairs:
        if row["overlap"] < limit:
            continue
        newset = set()
        newset.add(row['path1'])
        newset.add(row['path2'])
        for videoset in sets:
            if row['path1'] in videoset or row['path2'] in videoset:
                sets.remove(videoset)
                newset = newset.union(videoset)
        sets.append(newset)
    sets = sorted(sets, key=lambda d: len(d), reverse=True)

    pp = pprint.PrettyPrinter(width=200, compact=False)
    for l in sets:
        pp.pprint(sorted(list(l), reverse=True))


def show_no_overlaps(pairs):
    videos = set()
    for row in pairs:
        videos.add((row['path1'], row['frames1']))
        videos.add((row['path2'], row['frames2']))
    for row in pairs:
        if row["overlap"] > 0:
            if (row['path1'], row['frames1']) in videos:
                videos.remove((row['path1'], row['frames1']))
            if (row['path2'], row['frames2']) in videos:
                videos.remove((row['path2'], row['frames2']))
    for video in videos:
        print(video)
    print(len(videos))


def auto_cleanup(pairs, limit_rate=.0, limit_frame=0):
    for pair in pairs:
        if "MP4 Archive" in pair["path1"] or "MP4 Archive" in pair["path2"]:
            if "MP4 Archive" in pair["path1"] and "wmv" in pair["path2"]:
                path_keep, path_remove, length_remove = pair["path1"], pair["path2"], pair["frames2"]
            elif "MP4 Archive" in pair["path2"] and "wmv" in pair["path1"]:
                path_keep, path_remove, length_remove = pair["path2"], pair["path1"], pair["frames1"]
            else:
                continue
            overlap = pair["overlap"]
            if length_remove == 0:
                continue
            if overlap / length_remove >= limit_rate and overlap >= limit_frame:
                print()
                print(path_keep)
                print(path_remove)
                print(length_remove, overlap)

                name = input("Do you want to delete "+path_remove)
                if name == "y":
                    print("Deleting "+path_remove)
                    os.remove(path_remove)


if __name__ == '__main__':
    with open("pairs.json", "r+") as fp:
        pairs = json.load(fp)
    pairs = sorted(pairs, key=lambda d: d['overlap'], reverse=True)
    print(len(pairs))
    show_sets(pairs, limit=100)
    # show_all(pairs)
    # show_complete_overlaps(pairs)
    # show_no_overlaps(pairs)
    # auto_cleanup(pairs, limit_frame=100)

