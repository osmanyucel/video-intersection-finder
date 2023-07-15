import json
import os
from Video import Video
from multiprocessing import Pool, cpu_count


def is_video_file(name):
    return name[-4:].lower() in [".mkv", ".mpg", ".vob", ".wmv", ".mov", ".mp4", ".avi"]


def read_file(path):
    print(path)
    video = Video(path)
    video.load()
    print("DONE " + path)
    return video


def read_all_files(root: str):
    processed_paths = set()
    try:
        with open("videos.json", "r+") as fp:
            cached_videos = json.load(fp)
    except:
        cached_videos = list()
        pass
    for v in cached_videos:
        processed_paths.add(v["path"])
    paths = list()
    for path, subdirs, files in os.walk(root):
        for name in files:
            full_path = os.path.join(path, name)
            if is_video_file(full_path) and not full_path in processed_paths:
                paths.append(full_path)
    with Pool(cpu_count() - 1) as p:
        videos = p.map(read_file, paths)
    videos.extend(cached_videos)
    return videos


def process():
    videos = read_all_files("/media/osman/SAMSUNG1/Video Düzen/")
    with open("videos.json", "w+") as fp:
        json.dump(videos, fp, cls=Video.CustomEncoder)


if __name__ == '__main__':
    process()
