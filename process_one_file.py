import json
import os

from tqdm import tqdm

from Video import Video


def is_video_file(name):
    return name[-4:].lower() in [".mkv", ".mpg", ".vob", ".wmv"]


def read_all_files(root: str, limit=999999, seen=set()):
    videos = list()
    i = 0
    for path, subdirs, files in os.walk(root):
        for name in files:
            if is_video_file(name):
                if i >= limit:
                    return videos
                video = Video(os.path.join(path, name))
                if video.path in seen:
                    continue
                print(video.path)
                video.load()
                videos.append(video)
                i += 1
    return videos


def find_all_overlaps(videos):
    for i in range(len(videos)):
        for j in range(i + 1, len(videos)):
            print("{}\t{}\t{}\t{}\t{}".format(videos[i].path,
                                              len(videos[i].frames),
                                              videos[j].path,
                                              len(videos[j].frames),
                                              len(videos[i].find_overlap(videos[j]))))


prepared = set()
videos = list()
try:
    with open("videos.json", "r+") as fp:
        data = json.load(fp)
        for file in data:
            prepared.add(file["path"])
            videos.append(Video(file["path"], file["frames"]))
    videos.sort()
except:
    raise


def findoverlap(tuple1):
    v1 = tuple1[0]
    v2 = tuple1[1]
    d = {"path1": v1.path, "frames1": len(v1.frames),
         "path2": v2.path, "frames2": len(v2.frames),
         "overlap": v1.find_overlap(v2)}
    return d


# print(len(videos))
# print(len(videos[0].frames))
# videos += read_all_files("/media/osman/SAMSUNG/Video Düzen/", limit=1000, seen=prepared)
# print(len(videos))
# with open("videos_old.json", "w+") as fp:
#     json.dump(videos, fp, cls=Video.CustomEncoder)


if __name__ == '__main__':
    mainvideo = Video("/media/osman/SAMSUNG1/Video Düzen/MP4 Archive/Working/Done/Fatma Gülen Çeyiz.mp4")
    mainvideo.load()

    for j in tqdm(range(0, len(videos))):
        outputs = findoverlap((mainvideo, videos[j]))
        if outputs["overlap"] > 0:
            print(outputs)
