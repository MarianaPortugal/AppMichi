import os
import json

PROGRESS_FILE = "data/progress.json"
VIDEOS_PATH = "assets/vídeos"

def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return 0
    with open(PROGRESS_FILE, "r") as f:
        return json.load(f).get("current_video", 0)

def save_progress(index):
    with open(PROGRESS_FILE, "w") as f:
        json.dump({"current_video": index}, f)

def get_next_video():
    videos = sorted(os.listdir(VIDEOS_PATH))
    index = load_progress()
    if index < len(videos):
        return os.path.join(VIDEOS_PATH, videos[index])
    return None
