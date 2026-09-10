import json
from pathlib import Path
from game.leaderboard_api import LeaderboardAPI

class SaveManager:
    NORMAL_LEVELS = 20
    HARD_LEVEL_START = 21
    HARD_LEVEL_END = 30

    def __init__(self):
        self.path = Path.home() / ".mazepaint_save.json"
        self.data = {
            "unlocked": 1,
            "hard_unlocked": False,
            "completed": [],
            "stars": {}
        }
        self.leaderboard = LeaderboardAPI()
        self.load()

    def load(self):
        if not self.path.exists():
            return
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                saved = json.load(file)
            self.data.update(saved)
            self.data.setdefault("hard_unlocked", False)
            self.data.setdefault("completed", [])
            self.data.setdefault("stars", {})
            completed = set(self.data["completed"])
            if 20 in completed or "20" in completed:
                self.data["hard_unlocked"] = True
                self.data["unlocked"] = max(self.data.get("unlocked", 1), 21)
        except Exception:
            pass

    def save(self):
        try:
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(self.data, file, indent=4)
        except Exception:
            pass

    def is_unlocked(self, level):
        level = int(level)
        if 1 <= level <= self.NORMAL_LEVELS:
            return level <= self.data["unlocked"]
        if self.HARD_LEVEL_START <= level <= self.HARD_LEVEL_END:
            return bool(self.data.get("hard_unlocked", False))
        return False



   def complete(self, level, stars, time_seconds=None):
    level = int(level)
    stars = max(0, min(3, int(stars)))

    if level not in self.data["completed"]:
        self.data["completed"].append(level)

    key = str(level)

    self.data["stars"][key] = max(
        stars,
        self.data["stars"].get(key, 0)
    )

    if 1 <= level < self.NORMAL_LEVELS:
        if level >= self.data["unlocked"]:
            self.data["unlocked"] = level + 1

    elif level == self.NORMAL_LEVELS:
        self.data["unlocked"] = self.HARD_LEVEL_START
        self.data["hard_unlocked"] = True

    elif self.HARD_LEVEL_START <= level <= self.HARD_LEVEL_END:
        self.data["hard_unlocked"] = True

    self.save()

    # ارسال رکورد به Leaderboard آنلاین
    if time_seconds is not None:
        self.leaderboard.submit_score(
            level=level,
            time_seconds=time_seconds,
            stars=stars
        )

    def get_stars(self, level):
        return self.data["stars"].get(str(level), 0)

    def is_hard_unlocked(self):
        return bool(self.data.get("hard_unlocked", False))

    def reset(self):
        self.data = {
            "unlocked": 1,
            "hard_unlocked": False,
            "completed": [],
            "stars": {}
        }
        self.save()
