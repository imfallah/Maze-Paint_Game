import json
from pathlib import Path


class SaveManager:

    def __init__(self):

        self.path = (
            Path.home()
            / ".mazepaint_save.json"
        )

        self.data = {
            "unlocked": 1,
            "completed": [],
            "stars": {}
        }

        self.load()

    # ==========================================

    def load(self):

        if not self.path.exists():
            return

        try:

            with open(
                self.path,
                "r",
                encoding="utf-8"
            ) as file:

                saved = json.load(file)

            self.data.update(
                saved
            )

        except Exception:

            pass

    # ==========================================

    def save(self):

        try:

            with open(
                self.path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.data,
                    file,
                    indent=4
                )

        except Exception:

            pass

    # ==========================================

    def is_unlocked(
        self,
        level
    ):

        return level <= self.data[
            "unlocked"
        ]

    # ==========================================

    def complete(
        self,
        level,
        stars
    ):

        if level not in self.data[
            "completed"
        ]:

            self.data[
                "completed"
            ].append(level)

        self.data[
            "stars"
        ][str(level)] = max(
            stars,
            self.data[
                "stars"
            ].get(
                str(level),
                0
            )
        )

        if level >= self.data[
            "unlocked"
        ]:

            self.data[
                "unlocked"
            ] = level + 1

        self.save()

    # ==========================================

    def get_stars(
        self,
        level
    ):

        return self.data[
            "stars"
        ].get(
            str(level),
            0
        )
