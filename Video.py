import cv2
from LCS import lcs
import json


class Video:
    def __init__(self, path, frames=None):
        self.path = path
        self.frames = frames

    class CustomEncoder(json.JSONEncoder):
        def default(self, o):
            return {"path": o.path, "frames": o.frames}

    def load(self):
        frames = []
        cap = cv2.VideoCapture(self.path)
        while cap.isOpened():
            ret, frame = cap.read()
            if frame is None:
                break
            phash = self.pHash(frame)
            frames.append(phash)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        cap.release()
        self.frames = frames

    def pHash(self, cv_image):
        h = cv2.img_hash.pHash(cv_image)  # 8-byte hash
        pH = int.from_bytes(h.tobytes(), byteorder='big', signed=False)
        return pH

    def find_overlap(self, other_video):
        return lcs(self.frames, other_video.frames)

    def __eq__(self, other):
        return len(self.frames) == len(other.frames)

    def __lt__(self, other):
        return len(self.frames) < len(other.frames)

    def __le__(self, other):
        return len(self.frames) <= len(other.frames)