
import json
import os

PROGRESS_FILE = "data/progress.json"
VIDEO_PATH = "assets/vídeos"

def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return {}
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_progress(data):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def get_videos_for_theme(theme):
    progress = load_progress()
    if theme not in progress:
        return []

    theme_data = progress[theme]
    result = []
    for video_key in sorted(theme_data.keys()):
        video_file = f"{video_key}.mp4"
        video_path = os.path.join(VIDEO_PATH, video_file)
        is_unlocked = (
            video_key.endswith("_1") or
            (theme_data.get(video_key.replace("_2", "_1"), {}).get("watched") and
             theme_data.get(video_key.replace("_2", "_1"), {}).get("submitted"))
        )
        result.append({
            "file": video_path,
            "name": video_key,
            "unlocked": is_unlocked,
            "watched": theme_data[video_key]["watched"],
            "submitted": theme_data[video_key]["submitted"]
        })
    return result

def mark_watched(theme, video_name):
    progress = load_progress()
    if theme in progress and video_name in progress[theme]:
        progress[theme][video_name]["watched"] = True
        save_progress(progress)

def mark_submitted(theme, video_name):
    progress = load_progress()
    if theme in progress and video_name in progress[theme]:
        progress[theme][video_name]["submitted"] = True
        save_progress(progress)
