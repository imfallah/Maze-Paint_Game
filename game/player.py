from collections import deque
import math


class Player:

    def __init__(self, maze):

        self.maze = maze

        self.x, self.y = maze.start

        size = maze.tile_size

        self.pixel_x = (
            self.x * size + size / 2
        )

        self.pixel_y = (
            self.y * size + size / 2
        )

        self.speed = 700

        self.moving = False

        self.current_target = None

        self.path = []

        self.input_queue = deque(
            maxlen=3
        )

        self.direction = (0, 0)

        self.maze.paint(
            self.x,
            self.y
        )

    # ==========================================
    # INPUT
    # ==========================================

    def slide(self, dx, dy):

        direction = (
            dx,
            dy
        )

        # اگر در حال حرکت است
        if self.moving:

            if direction not in self.input_queue:

                self.input_queue.append(
                    direction
                )

            return

        self.start_move(
            dx,
            dy
        )

    # ==========================================
    # START MOVE
    # ==========================================

    def start_move(self, dx, dy):

        path = self.get_slide_path(
            dx,
            dy
        )

        if not path:

            return

        self.direction = (
            dx,
            dy
        )

        self.path = path

        self.next_target()

    # ==========================================
    # FIND PATH
    # ==========================================

    def get_slide_path(
        self,
        dx,
        dy
    ):

        path = []

        x = self.x
        y = self.y

        while True:

            nx = x + dx
            ny = y + dy

            if self.maze.is_wall(
                nx,
                ny
            ):
                break

            x = nx
            y = ny

            path.append(
                (x, y)
            )

        return path

    # ==========================================
    # NEXT TARGET
    # ==========================================

    def next_target(self):

        if not self.path:

            self.moving = False

            self.direction = (
                0,
                0
            )

            self.process_queue()

            return

        self.current_target = (
            self.path.pop(0)
        )

        self.moving = True

    # ==========================================
    # QUEUE
    # ==========================================

    def process_queue(self):

        if not self.input_queue:

            return

        dx, dy = (
            self.input_queue.popleft()
        )

        self.start_move(
            dx,
            dy
        )

    # ==========================================
    # UPDATE
    # ==========================================

    def update(self, dt):

        if not self.moving:

            return

        tx, ty = (
            self.current_target
        )

        size = self.maze.tile_size

        target_x = (
            tx * size
            + size / 2
        )

        target_y = (
            ty * size
            + size / 2
        )

        dx = (
            target_x
            - self.pixel_x
        )

        dy = (
            target_y
            - self.pixel_y
        )

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        step = (
            self.speed * dt
        )

        if distance <= step:

            self.pixel_x = target_x
            self.pixel_y = target_y

            self.x = tx
            self.y = ty

            self.maze.paint(
                self.x,
                self.y
            )

            self.next_target()

        else:

            self.pixel_x += (
                dx / distance
            ) * step

            self.pixel_y += (
                dy / distance
            ) * step
