import json


class Maze:

    def __init__(self, level_file):

        with open(
            level_file,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        self.tile_size = data["tile_size"]

        self.grid = data["maze"]

        self.start = tuple(
            data["start"]
        )

        self.rows = len(
            self.grid
        )

        self.cols = len(
            self.grid[0]
        )

        # خانه‌هایی که باید رنگ شوند
        self.paintable = set()

        for y in range(self.rows):

            for x in range(self.cols):

                if self.grid[y][x] == ".":

                    self.paintable.add(
                        (x, y)
                    )

        # خانه‌های رنگ‌شده
        self.painted = set()

    # ==========================================
    # WALL
    # ==========================================

    def is_wall(self, x, y):

        if x < 0 or y < 0:
            return True

        if x >= self.cols:
            return True

        if y >= self.rows:
            return True

        return self.grid[y][x] == "#"

    # ==========================================
    # PAINT
    # ==========================================

    def paint(self, x, y):

        if (x, y) in self.paintable:

            self.painted.add(
                (x, y)
            )

    # ==========================================
    # PROGRESS
    # ==========================================

    @property
    def total_paintable(self):

        return len(
            self.paintable
        )

    @property
    def painted_count(self):

        return len(
            self.painted
        )

    @property
    def progress(self):

        if self.total_paintable == 0:
            return 100

        return int(
            (
                self.painted_count
                /
                self.total_paintable
            ) * 100
        )

    # ==========================================
    # COMPLETE
    # ==========================================

    def is_complete(self):

        return (
            self.painted
            ==
            self.paintable
        )
