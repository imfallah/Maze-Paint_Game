from pathlib import Path
import json


class LevelManager:

    def __init__(self):

        self.level_dir = Path("levels")

        self.levels = sorted(
            self.level_dir.glob(
                "level_*.json"
            )
        )

    @property
    def count(self):

        return len(self.levels)

    def get_level(self, index):

        if index < 0:
            index = 0

        if index >= self.count:
            index = self.count - 1

        return str(
            self.levels[index]
        )

    def load(self, index):

        path = self.get_level(index)

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)
