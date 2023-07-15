from cleanup import cleanup
from video_reader import process
from main import main_process
import os

if __name__ == '__main__':
    cleanup("videos.json", lambda row: os.path.isfile(row["path"]))
    cleanup("pairs.json", lambda row: os.path.isfile(row["path1"]) and os.path.isfile(row["path2"]))
    process()
    main_process()
