import os
import time
import math
import random
import pygame

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, Qt, QRunnable, QThreadPool
from game.maze import Maze
from game.player import Player
from game.save_manager import SaveManager


# Levels are looked up relative to the project root, not the process's
# current working directory — otherwise "levels/level_XX.json" only
# resolves correctly when the app happens to be launched from that
# exact folder, which is a common reason "next level" silently fails.
# This file lives in <project_root>/game/, so the project root is one
# level up from here.
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


def level_file_path(level_number):
    return os.path.join(
        BASE_DIR,
        "levels",
        f"level_{level_number:02d}.json"
    )


# Visual theme per level: painted tile color, accent, and roller style.
LEVEL_THEMES = [
    # name, tile, highlight, accent, roller_outer, roller_inner, roller_mark, ring, style
    ("Mint",       (57,190,102), (120,245,155), (110,240,135), (196,118,18), (255,174,45), (211,130,22), "circle"),
    ("Ocean",      (45,150,210), (105,205,255), (75,190,245),  (25,95,150),  (45,175,235),  (25,115,185),  "ring"),
    ("Violet",     (145,85,220), (205,150,255), (185,120,255), (85,45,145),  (165,95,235),  (105,55,175),  "diamond"),
    ("Coral",      (235,90,100), (255,155,160), (255,125,135), (155,45,55),  (240,95,105),  (185,55,65),  "circle"),
    ("Sun",        (240,175,35), (255,220,105), (255,195,65),  (170,105,10),  (250,175,35),  (200,125,10),  "ring"),
    ("Cyan",       (30,190,185), (100,245,235), (65,225,215),  (10,105,105),  (35,205,195),  (15,140,135),  "hex"),
    ("Rose",       (220,75,145), (255,145,195), (245,110,170), (135,35,85),   (225,75,145),   (165,45,105),   "heart"),
    ("Blue",       (65,105,225), (135,170,255), (105,145,255), (30,55,140),   (70,110,230),   (45,75,170),    "diamond"),
    ("Lime",       (145,205,45), (205,245,105), (175,225,65),  (75,120,15),   (155,210,45),   (105,150,20),    "hex"),
    ("Plum",       (175,75,195), (225,135,240), (205,105,225), (100,35,120),  (180,75,200),   (125,45,145),    "ring"),
    ("Sky",        (60,165,235), (140,220,255), (100,195,250), (25,90,145),   (65,170,235),   (35,120,180),    "circle"),
    ("Tangerine",  (235,115,40), (255,180,100), (255,145,65),  (145,55,10),   (235,115,35),   (180,75,15),     "diamond"),
    ("Aqua",       (35,205,150), (120,250,205), (75,230,175),  (10,115,80),   (40,205,150),   (15,145,105),    "hex"),
    ("Magenta",    (210,55,190), (250,125,235), (235,90,215),  (125,20,105),  (215,60,195),   (155,30,135),    "heart"),
    ("Royal",      (85,75,220), (155,145,255), (120,110,245), (40,35,125),   (90,80,225),    (55,50,165),     "ring"),
    ("Gold",       (220,155,35), (255,215,100), (245,185,55),  (130,80,5),    (225,160,40),   (165,105,10),    "circle"),
    ("Teal",       (25,165,155), (100,225,215), (60,200,190),  (5,85,85),     (30,170,160),   (10,115,110),    "hex"),
    ("Cherry",     (205,50,70), (250,120,135), (230,80,100),  (120,20,35),   (210,55,75),    (150,30,50),     "diamond"),
    ("Electric",   (80,125,235), (150,205,255), (115,170,255), (30,65,145),   (85,135,240),   (45,90,175),    "ring"),
    ("Boss",       (245,70,45), (255,170,105), (255,110,70),  (110,20,10),   (245,75,45),    (165,35,15),     "hex"),
    ("Aurora",     (70,205,125), (155,255,185), (105,235,155), (20,100,60),   (75,210,130),   (35,145,85),     "diamond"),
    ("Ice",        (80,190,230), (170,240,255), (120,220,250), (35,105,145),  (85,195,235),   (50,135,180),    "circle"),
    ("Neon",       (185,70,230), (240,140,255), (215,100,250), (90,25,125),   (190,75,235),   (125,40,165),    "heart"),
    ("Inferno",    (235,75,35), (255,160,90), (255,105,55),  (115,25,5),    (240,80,35),    (165,40,10),     "ring"),
    ("Diamond",    (120,175,245), (200,235,255), (160,210,255), (45,80,145),   (125,180,245),  (75,120,180),    "diamond"),
]

# World/environment theme per level.
# name, background_top, background_bottom, grid, ambient, wall, floor, style
WORLD_THEMES = [
    ("Forest",   (7, 22, 16),  (13, 45, 28),  (18, 55, 35),  (35, 105, 65),  (27, 52, 38),  (220, 232, 220), "leaves"),
    ("Ocean",    (5, 20, 38),  (8, 55, 82),  (15, 65, 90),  (35, 135, 175),  (28, 58, 78),  (218, 238, 242), "bubbles"),
    ("Violet",   (18, 8, 35),  (48, 16, 72),  (60, 22, 82),  (125, 65, 180),  (52, 35, 70),  (232, 222, 240), "stars"),
    ("Volcano",  (35, 7, 5),   (82, 18, 7),  (105, 28, 10),  (220, 65, 25),  (70, 32, 25),  (245, 225, 210), "embers"),
    ("Desert",   (42, 24, 8),  (88, 52, 14),  (110, 67, 20),  (220, 145, 45),  (75, 55, 32),  (245, 232, 205), "sand"),
    ("Ice",      (8, 28, 45),  (20, 78, 105),  (28, 95, 125),  (110, 215, 245), (42, 76, 92),  (225, 244, 250), "snow"),
    ("Rose",     (38, 8, 28),  (82, 18, 55),  (105, 28, 68),  (225, 90, 160),  (72, 38, 62),  (245, 225, 238), "petals"),
    ("Cyber",    (5, 8, 24),   (12, 20, 55),  (20, 30, 75),  (65, 160, 255),  (32, 42, 72),  (220, 232, 250), "scan"),
    ("Toxic",    (8, 25, 8),   (22, 62, 15),  (30, 82, 18),  (130, 235, 55),  (42, 70, 32),  (225, 242, 210), "bubbles"),
    ("Royal",    (10, 8, 28),  (28, 20, 70),  (38, 28, 90),  (125, 110, 245), (48, 42, 82),  (230, 225, 245), "stars"),
    ("Sunset",   (38, 12, 8),  (85, 28, 18),  (110, 42, 25),  (245, 125, 55),  (76, 45, 38),  (248, 228, 210), "horizon"),
    ("Aqua",     (4, 30, 30),  (8, 78, 72),  (12, 95, 90),  (55, 220, 205),  (30, 70, 68),  (220, 244, 240), "bubbles"),
    ("Candy",    (35, 8, 35),  (82, 20, 72),  (105, 28, 90),  (245, 105, 220), (72, 38, 70),  (248, 230, 245), "sparkles"),
    ("Midnight", (3, 5, 15),   (10, 15, 35),  (16, 25, 48),  (70, 100, 180),  (28, 38, 60),  (215, 225, 240), "stars"),
    ("Gold",     (30, 20, 4),  (72, 48, 8),   (92, 62, 12),  (235, 185, 55),  (72, 56, 25),  (246, 236, 205), "sparkles"),
    ("Emerald",  (4, 25, 20),  (8, 65, 45),   (12, 82, 55),  (50, 210, 135),  (30, 68, 52),  (220, 242, 230), "leaves"),
    ("Cherry",   (32, 5, 12),  (78, 10, 28),  (98, 18, 35),  (235, 70, 95),  (70, 32, 40),  (245, 225, 230), "embers"),
    ("Storm",    (10, 12, 18), (28, 35, 48),  (40, 48, 62),  (100, 150, 190), (48, 55, 65), (225, 232, 238), "rain"),
    ("Neon",     (12, 3, 20),  (38, 8, 55),   (55, 12, 75),  (220, 70, 245),  (58, 32, 72),  (235, 220, 245), "scan"),
    ("Inferno",  (25, 4, 2),   (72, 12, 3),   (95, 20, 5),   (255, 95, 25),  (68, 28, 20), (245, 220, 205), "embers"),
    ("Galaxy",   (4, 3, 20),   (15, 8, 48),   (22, 15, 65),  (105, 95, 240), (35, 35, 72), (225, 225, 245), "stars"),
    ("Jungle",   (3, 28, 12),  (8, 72, 25),   (12, 92, 35),  (70, 205, 85),  (28, 70, 38), (220, 240, 218), "leaves"),
    ("Arctic",   (5, 20, 35),  (18, 58, 88),  (25, 78, 110), (130, 220, 255), (40, 68, 85), (225, 245, 252), "snow"),
    ("Lava",     (35, 3, 2),   (100, 12, 2),  (125, 20, 4),  (255, 125, 35), (75, 28, 18), (248, 220, 195), "embers"),
    ("Boss",     (18, 2, 2),   (65, 5, 5),   (95, 10, 8),   (255, 55, 35),  (60, 22, 20), (242, 218, 205), "pulse"),
    ("Aurora",   (3, 15, 25),  (10, 55, 55),  (18, 75, 78),  (75, 235, 185), (32, 62, 68), (225, 244, 240), "aurora"),
]

class SaveScoreWorker(QRunnable):

    def __init__(self, save_manager, level, stars, elapsed):
        super().__init__()

        self.save_manager = save_manager
        self.level = level
        self.stars = stars
        self.elapsed = elapsed

    def run(self):
        try:
            self.save_manager.complete(
                self.level,
                self.stars,
                self.elapsed
            )

            print(
                f"[Leaderboard] Level {self.level} saved in background."
            )

        except Exception as e:
            print(
                f"[Leaderboard] Background save error: {e}"
            )





class PygameWidget(QWidget):

    def __init__(self, level=1, parent=None):
        super().__init__(parent)

        self.level = level
        self.parent_window = parent

        self.setAttribute(Qt.WA_NativeWindow)
        self.setFocusPolicy(Qt.StrongFocus)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_loop)

        self.pygame_initialized = False

        self.maze = None
        self.player = None

        self.completed = False
        self.completion_started = False
        self.paused = False

        self.start_time = 0
        self.elapsed = 0

        self.drag_start = None

        self.particles = []
        self.move_particles = []
        self.splash_particles = []

        self.stars = 0

        self.trail_surface = None
        self.trail = []

        # Visual movement state
        self.visual_x = 0.0
        self.visual_y = 0.0
        self.player_prev_x = 0.0
        self.player_prev_y = 0.0

        self.player_speed = 0.0
        self.player_angle = 0.0

        self.player_dir_x = 1.0
        self.player_dir_y = 0.0

        self.bounce = 0.0
        self.squash = 0.0
        self.move_flash = 0.0
        self.screen_shake = 0.0

        self.last_move_particle = 0.0

        # Weather / atmosphere state
        self.weather_type = None
        self.weather_particles = []
        self.weather_timer = 0.0
        self.lightning_flash = 0.0

        self.save = SaveManager()
        self.thread_pool = QThreadPool.globalInstance()

        self.theme = LEVEL_THEMES[(self.level - 1) % len(LEVEL_THEMES)]
        self.theme_name = self.theme[0]
        self.tile_color = self.theme[1]
        self.tile_highlight = self.theme[2]
        self.accent_color = self.theme[3]
        self.roller_outer = self.theme[4]
        self.roller_inner = self.theme[5]
        self.roller_mark = self.theme[6]
        self.roller_style = self.theme[7]

        self.world = WORLD_THEMES[(self.level - 1) % len(WORLD_THEMES)]
        self.world_name = self.world[0]
        self.bg_top = self.world[1]
        self.bg_bottom = self.world[2]
        self.world_grid = self.world[3]
        self.world_ambient = self.world[4]
        self.world_wall = self.world[5]
        self.world_floor = self.world[6]
        self.world_style = self.world[7]

    # ========================================================
    # START
    # ========================================================

    def start(self):

        if self.pygame_initialized:
            self.setFocus()
            return

        os.environ["SDL_WINDOWID"] = str(int(self.winId()))

        pygame.init()

        width = max(1, self.width())
        height = max(1, self.height())

        self.screen = pygame.display.set_mode(
            (width, height)
        )

        self.trail_surface = pygame.Surface(
            (width, height),
            pygame.SRCALPHA
        )

        # یک Surface موقت با اندازه‌ی صفحه که برای همه‌ی
        # افکت‌های شفاف (glow، هاله‌ی شن، پرتوهای نور، برق آسمان،
        # اورلی پاز/کامل) دوباره‌استفاده میشه، به‌جای اینکه هر
        # فریم یک Surface تازه ساخته بشه. ساختن Surface جدید در
        # هر فریم (به‌خصوص با SRCALPHA) دلیل اصلی لگ/میکروفریزها
        # بود؛ fill کردن یک Surface آماده خیلی ارزون‌تره.
        self.fx_surface = pygame.Surface(
            (width, height),
            pygame.SRCALPHA
        )

        self.clock = pygame.time.Clock()

        # فونت‌ها فقط یک‌بار ساخته میشن. ساختن pygame.font.SysFont
        # عملیات سنگینیه (جستجوی فونت سیستم) و صداکردنش در هر
        # فریم (که قبلاً توی draw_hud/draw_pause/draw_complete
        # اتفاق می‌افتاد) دلیل اصلی گیرکردن و لگ بازی بود.
        self.font_hud = pygame.font.SysFont(
            "arial", 18, bold=True
        )
        self.font_hud_small = pygame.font.SysFont(
            "arial", 15
        )
        self.font_pause = pygame.font.SysFont(
            "arial", 48, bold=True
        )
        self.font_complete_title = pygame.font.SysFont(
            "arial", 44, bold=True
        )
        self.font_complete_small = pygame.font.SysFont(
            "arial", 20
        )

        self.load_level()

        self.pygame_initialized = True

        self.timer.start(16)

        self.setFocus()

    # ========================================================
    # LOAD LEVEL
    # ========================================================

    def load_level(self):

        level_path = level_file_path(self.level)

        self.maze = Maze(level_path)
        self.player = Player(self.maze)

        self.theme = LEVEL_THEMES[(self.level - 1) % len(LEVEL_THEMES)]
        self.theme_name = self.theme[0]
        self.tile_color = self.theme[1]
        self.tile_highlight = self.theme[2]
        self.accent_color = self.theme[3]
        self.roller_outer = self.theme[4]
        self.roller_inner = self.theme[5]
        self.roller_mark = self.theme[6]
        self.roller_style = self.theme[7]

        self.world = WORLD_THEMES[(self.level - 1) % len(WORLD_THEMES)]
        self.world_name = self.world[0]
        self.bg_top = self.world[1]
        self.bg_bottom = self.world[2]
        self.world_grid = self.world[3]
        self.world_ambient = self.world[4]
        self.world_wall = self.world[5]
        self.world_floor = self.world[6]
        self.world_style = self.world[7]

        self.completed = False
        self.completion_started = False
        self.paused = False

        self.start_time = time.time()
        self.elapsed = 0

        self.drag_start = None

        self.particles.clear()
        self.move_particles.clear()
        self.splash_particles.clear()

        self.trail.clear()

        self.player_prev_x = self.player.pixel_x
        self.player_prev_y = self.player.pixel_y

        self.visual_x = self.player.pixel_x
        self.visual_y = self.player.pixel_y

        self.player_speed = 0.0
        self.player_angle = 0.0

        self.player_dir_x = 1.0
        self.player_dir_y = 0.0

        self.bounce = 0.0
        self.squash = 0.0
        self.move_flash = 0.0
        self.screen_shake = 0.0

        self.init_weather()

    # ========================================================
    # WEATHER
    # ========================================================

    def init_weather(self):
        """Set up a per-level weather layer driven by the world's style.

        This is what actually shifts the "mood" of each level: rain and
        lightning for storms, drifting snow for ice worlds, wind-blown
        sand for the desert, rising sparks for lava/fire worlds, and soft
        sun rays for warm/golden worlds.
        """

        width = max(1, self.width())
        height = max(1, self.height())

        style = self.world_style

        self.weather_particles = []
        self.weather_timer = 0.0
        self.lightning_flash = 0.0

        if style == "rain":
            self.weather_type = "rain"
            for _ in range(110):
                self.weather_particles.append({
                    "x": random.uniform(0, width),
                    "y": random.uniform(0, height),
                    "speed": random.uniform(11, 19),
                    "len": random.uniform(10, 22),
                    "drift": random.uniform(-4, -1.5),
                })

        elif style in ("snow",):
            self.weather_type = "snow"
            for _ in range(65):
                self.weather_particles.append({
                    "x": random.uniform(0, width),
                    "y": random.uniform(0, height),
                    "speed": random.uniform(0.6, 1.9),
                    "sway": random.uniform(0, math.pi * 2),
                    "sway_speed": random.uniform(0.01, 0.03),
                    "size": random.uniform(1.5, 3.5),
                })

        elif style == "sand":
            self.weather_type = "sand"
            for _ in range(55):
                self.weather_particles.append({
                    "x": random.uniform(-width, width),
                    "y": random.uniform(0, height),
                    "speed": random.uniform(3.5, 8),
                    "len": random.uniform(18, 45),
                })

        elif style in ("embers", "pulse"):
            self.weather_type = "embers_fg"
            for _ in range(40):
                self.weather_particles.append({
                    "x": random.uniform(0, width),
                    "y": random.uniform(0, height),
                    "speed": random.uniform(0.5, 1.7),
                    "sway": random.uniform(0, math.pi * 2),
                    "sway_speed": random.uniform(0.02, 0.05),
                    "size": random.uniform(1.5, 3.5),
                })

        elif style in ("horizon", "sparkles"):
            self.weather_type = "sun"

        else:
            self.weather_type = None

    def update_weather(self):

        if self.weather_type is None:
            return

        width = max(1, self.width())
        height = max(1, self.height())

        if self.weather_type == "rain":

            for drop in self.weather_particles:

                drop["y"] += drop["speed"]
                drop["x"] += drop["drift"]

                if drop["y"] > height:
                    drop["y"] = random.uniform(-40, -5)
                    drop["x"] = random.uniform(0, width)

                if drop["x"] < -20:
                    drop["x"] = width + 20

            self.weather_timer -= 1

            if self.weather_timer <= 0 and random.random() < 0.006:
                self.lightning_flash = 1.0
                self.weather_timer = 120

            self.lightning_flash *= 0.86

        elif self.weather_type == "snow":

            for flake in self.weather_particles:

                flake["y"] += flake["speed"]
                flake["sway"] += flake["sway_speed"]

                if flake["y"] > height:
                    flake["y"] = random.uniform(-20, -5)
                    flake["x"] = random.uniform(0, width)

        elif self.weather_type == "sand":

            for grain in self.weather_particles:

                grain["x"] += grain["speed"]

                if grain["x"] > width + 50:
                    grain["x"] = -50
                    grain["y"] = random.uniform(0, height)

        elif self.weather_type == "embers_fg":

            for ember in self.weather_particles:

                ember["y"] -= ember["speed"]
                ember["sway"] += ember["sway_speed"]

                if ember["y"] < -10:
                    ember["y"] = height + 10
                    ember["x"] = random.uniform(0, width)

    def draw_weather(self):

        if self.weather_type is None:
            return

        width = max(1, self.width())
        height = max(1, self.height())
        t = time.time()

        if self.weather_type == "rain":

            for drop in self.weather_particles:

                x, y = drop["x"], drop["y"]

                pygame.draw.line(
                    self.screen,
                    (170, 195, 225),
                    (x, y),
                    (x + drop["drift"] * 2.2, y + drop["len"]),
                    1
                )

            if self.lightning_flash > 0.05:

                alpha = int(self.lightning_flash * 85)

                self.fx_surface.fill(
                    (255, 255, 255, alpha)
                )

                self.screen.blit(
                    self.fx_surface,
                    (0, 0)
                )

        elif self.weather_type == "snow":

            for flake in self.weather_particles:

                x = flake["x"] + math.sin(flake["sway"]) * 14
                y = flake["y"]

                pygame.draw.circle(
                    self.screen,
                    (255, 255, 255),
                    (int(x), int(y)),
                    max(1, int(flake["size"]))
                )

        elif self.weather_type == "sand":

            self.fx_surface.fill(
                (*self.world_ambient, 10)
            )

            self.screen.blit(
                self.fx_surface,
                (0, 0)
            )

            for grain in self.weather_particles:

                x, y = grain["x"], grain["y"]

                pygame.draw.line(
                    self.screen,
                    self.world_ambient,
                    (x, y),
                    (x - grain["len"], y + grain["len"] * 0.12),
                    1
                )

        elif self.weather_type == "embers_fg":

            for ember in self.weather_particles:

                x = ember["x"] + math.sin(ember["sway"]) * 9
                y = ember["y"]

                glow = (
                    math.sin(t * 3 + ember["sway"]) + 1
                ) * 0.5

                color = tuple(
                    min(255, int(c + glow * 45))
                    for c in self.world_ambient
                )

                pygame.draw.circle(
                    self.screen,
                    color,
                    (int(x), int(y)),
                    max(1, int(ember["size"]))
                )

        elif self.weather_type == "sun":

            self.fx_surface.fill((0, 0, 0, 0))

            cx = width * 0.5
            cy = -height * 0.15

            for i in range(6):

                angle = (
                    (i / 6) * math.pi * 2
                    + t * 0.05
                )

                length = width * 1.4

                end_x = cx + math.cos(angle) * length
                end_y = cy + math.sin(angle) * length + height * 0.6

                pygame.draw.polygon(
                    self.fx_surface,
                    (*self.world_ambient, 16),
                    [
                        (cx, cy),
                        (end_x - 45, end_y),
                        (end_x + 45, end_y),
                    ]
                )

            self.screen.blit(
                self.fx_surface,
                (0, 0)
            )

    # ========================================================
    # KEYBOARD
    # ========================================================

    def keyPressEvent(self, event):

        if not self.player:
            return

        key = event.key()

        if self.completed:

            if key in (
                Qt.Key_Return,
                Qt.Key_Enter
            ):
                self.next_level()

            return

        if key == Qt.Key_Space:

            self.paused = not self.paused
            return

        if key == Qt.Key_R:

            self.restart()
            return

        if self.paused:
            return

        if key in (
            Qt.Key_W,
            Qt.Key_Up
        ):
            self.player.slide(0, -1)

        elif key in (
            Qt.Key_S,
            Qt.Key_Down
        ):
            self.player.slide(0, 1)

        elif key in (
            Qt.Key_A,
            Qt.Key_Left
        ):
            self.player.slide(-1, 0)

        elif key in (
            Qt.Key_D,
            Qt.Key_Right
        ):
            self.player.slide(1, 0)

    # ========================================================
    # MOUSE / SWIPE
    # ========================================================

    def mousePressEvent(self, event):

        if event.button() != Qt.LeftButton:
            return

        if self.completed:
            return

        self.drag_start = event.pos()

    def mouseReleaseEvent(self, event):

        if event.button() != Qt.LeftButton:
            return

        if not self.drag_start:
            return

        if self.paused:

            self.drag_start = None
            return

        start = self.drag_start
        end = event.pos()

        self.drag_start = None

        dx = end.x() - start.x()
        dy = end.y() - start.y()

        if abs(dx) < 15 and abs(dy) < 15:
            return

        if abs(dx) > abs(dy):

            if dx > 0:
                self.player.slide(1, 0)
            else:
                self.player.slide(-1, 0)

        else:

            if dy > 0:
                self.player.slide(0, 1)
            else:
                self.player.slide(0, -1)

    # ========================================================
    # GAME LOOP
    # ========================================================

    def game_loop(self):

        if not self.pygame_initialized:
            return

        for pg_event in pygame.event.get():

            if pg_event.type == pygame.KEYDOWN:

                if self.completed and pg_event.key in (
                    pygame.K_RETURN,
                    pygame.K_KP_ENTER
                ):
                    self.next_level()
                    return

        now = time.time()

        if not self.paused and not self.completed:

            self.elapsed = now - self.start_time

            self.player.update(1 / 60)

            if self.maze.is_complete():
                self.complete_level()

        self.update_player_visual()
        self.update_particles()
        self.update_weather()

        self.draw()

    # ========================================================
    # PLAYER ANIMATION
    # ========================================================

    def update_player_visual(self):

        if not self.player:
            return

        # Smooth interpolation.
        # Even if Player jumps instantly between tiles,
        # the visual roller smoothly travels to the target.
        target_x = self.player.pixel_x
        target_y = self.player.pixel_y

        dx_to_target = target_x - self.visual_x
        dy_to_target = target_y - self.visual_y

        distance_to_target = math.hypot(
            dx_to_target,
            dy_to_target
        )

        old_x = self.visual_x
        old_y = self.visual_y

        # Stronger easing while moving, softer near target.
        smoothing = 0.24

        if distance_to_target > 35:
            smoothing = 0.30

        self.visual_x += dx_to_target * smoothing
        self.visual_y += dy_to_target * smoothing

        dx = self.visual_x - old_x
        dy = self.visual_y - old_y

        distance = math.hypot(dx, dy)

        self.player_speed += (
            distance - self.player_speed
        ) * 0.30

        # Direction
        if distance > 0.03:

            self.player_dir_x = dx / distance
            self.player_dir_y = dy / distance

            # Wheel rotation
            self.player_angle += distance / 13.0
            self.player_angle %= (
                2 * math.pi
            )

            # Bounce / squash animation
            self.bounce += distance * 0.12
            self.squash = min(
                1.0,
                self.squash + distance * 0.08
            )

            # Flash when movement starts
            self.move_flash = min(
                1.0,
                self.move_flash + 0.12
            )

            # Green motion trail
            self.trail.append({
                "x": self.visual_x,
                "y": self.visual_y,
                "life": 1.0
            })

            # Small paint particles
            now = time.time()

            if now - self.last_move_particle > 0.025:

                self.spawn_move_particle()

                self.last_move_particle = now

        # Idle breathing
        self.squash *= 0.90
        self.move_flash *= 0.88

        # Trail fade
        for point in self.trail:
            point["life"] -= 0.075

        self.trail = [
            point
            for point in self.trail
            if point["life"] > 0
        ]

        if len(self.trail) > 22:
            self.trail = self.trail[-22:]

        self.player_prev_x = self.visual_x
        self.player_prev_y = self.visual_y

    # ========================================================
    # MOVEMENT PARTICLES
    # ========================================================

    def spawn_move_particle(self):

        if not self.player:
            return

        angle = random.uniform(
            0,
            math.pi * 2
        )

        speed = random.uniform(
            0.4,
            1.8
        )

        self.move_particles.append({
            "x": self.visual_x,
            "y": self.visual_y,
            "vx": math.cos(angle) * speed,
            "vy": math.sin(angle) * speed,
            "life": 1.0,
            "size": random.uniform(2, 5)
        })

        if len(self.move_particles) > 55:
            self.move_particles.pop(0)

    # ========================================================
    # COMPLETE
    # ========================================================

    def complete_level(self):

        if self.completion_started:
            return

        self.completion_started = True
        self.completed = True

        self.calculate_stars()
        self.create_particles()

        worker = SaveScoreWorker(
           self.save,
           self.level,
           self.stars,
           self.elapsed
         )

        self.thread_pool.start(worker)





    def calculate_stars(self):

        if self.elapsed <= 30:
            self.stars = 3

        elif self.elapsed <= 60:
            self.stars = 2

        else:
            self.stars = 1

    # ========================================================
    # NEXT LEVEL
    # ========================================================

    def next_level(self):

        if not self.pygame_initialized:
            return

        next_level = self.level + 1

        level_path = level_file_path(next_level)

        if os.path.exists(level_path):

            if self.parent_window:
                self.parent_window.show_game(
                    next_level
                )

        else:

            print(
                f"[PygameWidget] no level file at {level_path} — "
                f"returning to level select"
            )

            if self.parent_window:
                self.parent_window.show_levels()

    # ========================================================
    # DRAW
    # ========================================================

    def draw(self):

        self.screen.fill(
            (12, 14, 20)
        )

        self.draw_background()
        self.draw_maze()
        self.draw_trail()
        self.draw_move_particles()
        self.draw_player()
        self.draw_particles()
        self.draw_weather()
        self.draw_hud()

        if self.paused:
            self.draw_pause()

        if self.completed:
            self.draw_complete()

        pygame.display.flip()

    # ========================================================
    # BACKGROUND
    # ========================================================

    def draw_background(self):

        width = self.width()
        height = self.height()
        t = time.time()

        # Vertical gradient: every level gets its own atmosphere.
        top = self.bg_top
        bottom = self.bg_bottom
        for y in range(0, height, 4):
            k = y / max(height - 1, 1)
            color = tuple(
                int(top[i] * (1 - k) + bottom[i] * k)
                for i in range(3)
            )
            pygame.draw.rect(self.screen, color, (0, y, width, 4))

        # Different world styles.
        style = self.world_style

        if style == "scan":
            for y in range(0, height, 26):
                pygame.draw.line(
                    self.screen, self.world_grid,
                    (0, y), (width, y), 1
                )
            for x in range(0, width, 70):
                pygame.draw.line(
                    self.screen, self.world_grid,
                    (x, 0), (x, height), 1
                )

        elif style == "rain":
            for i in range(45):
                x = (i * 83 + int(t * 35 + i * 17)) % max(width, 1)
                y = (i * 47 + int(t * 120 + i * 29)) % max(height, 1)
                pygame.draw.line(
                    self.screen, self.world_ambient,
                    (x, y), (x - 3, y + 14), 1
                )

        elif style == "horizon":
            hy = int(height * 0.58)
            pygame.draw.line(
                self.screen, self.world_ambient,
                (0, hy), (width, hy), 2
            )
            for x in range(0, width, 80):
                pygame.draw.line(
                    self.screen, self.world_grid,
                    (x, hy), (width // 2, height), 1
                )

        elif style == "aurora":
            for i in range(7):
                y = int(height * (0.18 + i * 0.11))
                wave = int(math.sin(t * 0.7 + i) * 25)
                pygame.draw.arc(
                    self.screen,
                    self.world_ambient,
                    (-100 + wave, y - 50, width + 200, 130),
                    0.15, 3.0, 2
                )

        # Ambient particles / stars / bubbles / leaves.
        for i in range(32):
            x = (i * 137 + self.level * 31) % max(width, 1)
            base_y = (i * 83 + self.level * 19) % max(height, 1)
            drift = math.sin(t * (0.45 + (i % 4) * 0.12) + i) * 10

            if style == "stars":
                pulse = (math.sin(t * 2.0 + i) + 1) * 0.5
                r = 1 + int(pulse * 2)
                pygame.draw.circle(
                    self.screen, self.world_ambient,
                    (int(x + drift), int(base_y)), r
                )

            elif style in ("bubbles", "snow", "petals", "leaves"):
                y = (base_y + int(t * (8 + i % 5))) % max(height, 1)
                r = 2 + (i % 4)
                pygame.draw.circle(
                    self.screen, self.world_ambient,
                    (int(x + drift), y), r, 1
                )

            elif style in ("embers", "sparkles"):
                y = (base_y - int(t * (10 + i % 7))) % max(height, 1)
                r = 1 + (i % 3)
                pygame.draw.circle(
                    self.screen, self.world_ambient,
                    (int(x + drift), y), r
                )

            elif style == "pulse":
                pulse = (math.sin(t * 1.7 + i * 0.4) + 1) * 0.5
                r = 2 + int(pulse * 5)
                pygame.draw.circle(
                    self.screen, self.world_ambient,
                    (int(x + drift), int(base_y)), r, 1
                )

        # Subtle 40px grid remains, but uses the world's palette.
        for x in range(0, width, 40):
            pygame.draw.line(
                self.screen, self.world_grid,
                (x, 0), (x, height), 1
            )
        for y in range(0, height, 40):
            pygame.draw.line(
                self.screen, self.world_grid,
                (0, y), (width, y), 1
            )

    # ========================================================
    # MAZE
    # ========================================================

    def draw_maze(self):

        size = self.maze.tile_size

        maze_width = (
            self.maze.cols * size
        )

        maze_height = (
            self.maze.rows * size
        )

        offset_x = (
            self.width() - maze_width
        ) // 2

        offset_y = (
            self.height() - maze_height
        ) // 2

        shadow = pygame.Rect(
            offset_x - 10,
            offset_y - 10,
            maze_width + 20,
            maze_height + 20
        )

        pygame.draw.rect(
            self.screen,
            (5, 6, 9),
            shadow,
            border_radius=20
        )

        for y in range(self.maze.rows):

            for x in range(self.maze.cols):

                rect = pygame.Rect(
                    offset_x + x * size,
                    offset_y + y * size,
                    size,
                    size
                )

                if self.maze.grid[y][x] == "#":

                    pygame.draw.rect(
                        self.screen,
                        self.world_wall,
                        rect,
                        border_radius=8
                    )

                    pygame.draw.rect(
                        self.screen,
                        self.world_grid,
                        rect,
                        2,
                        border_radius=8
                    )

                else:

                    if (
                        x,
                        y
                    ) in self.maze.painted:

                        pygame.draw.rect(
                            self.screen,
                            self.tile_color,
                            rect,
                            border_radius=7
                        )

                        # Paint highlight
                        pygame.draw.rect(
                            self.screen,
                            self.tile_highlight,
                            (
                                rect.x + 5,
                                rect.y + 5,
                                rect.width - 10,
                                4
                            ),
                            border_radius=2
                        )

                        # Animated shine
                        shine = (
                            math.sin(
                                time.time() * 2.2
                                + x * 0.7
                                + y * 0.5
                            )
                            + 1
                        ) * 0.5

                        if shine > 0.72:

                            pygame.draw.circle(
                                self.screen,
                                self.tile_highlight,
                                rect.center,
                                2
                            )

                    else:

                        pygame.draw.rect(
                            self.screen,
                            self.world_floor,
                            rect,
                            border_radius=7
                        )

                        pygame.draw.rect(
                            self.screen,
                            self.world_grid,
                            rect,
                            1,
                            border_radius=7
                        )

    # ========================================================
    # TRAIL
    # ========================================================

    def draw_trail(self):

        if self.trail_surface is None:
            return

        self.trail_surface.fill(
            (0, 0, 0, 0)
        )

        size = self.maze.tile_size

        maze_width = (
            self.maze.cols * size
        )

        maze_height = (
            self.maze.rows * size
        )

        offset_x = (
            self.width() - maze_width
        ) // 2

        offset_y = (
            self.height() - maze_height
        ) // 2

        for point in self.trail:

            life = point["life"]

            alpha = max(
                0,
                min(
                    160,
                    int(life * 160)
                )
            )

            radius = max(
                2,
                int(
                    size * (
                        0.10
                        + 0.22 * life
                    )
                )
            )

            px = int(
                offset_x + point["x"]
            )

            py = int(
                offset_y + point["y"]
            )

            pygame.draw.circle(
                self.trail_surface,
                (75, 235, 125, alpha),
                (px, py),
                radius
            )

        self.screen.blit(
            self.trail_surface,
            (0, 0)
        )

    # ========================================================
    # MOVE PARTICLES
    # ========================================================

    def draw_move_particles(self):

        size = self.maze.tile_size

        maze_width = (
            self.maze.cols * size
        )

        maze_height = (
            self.maze.rows * size
        )

        offset_x = (
            self.width() - maze_width
        ) // 2

        offset_y = (
            self.height() - maze_height
        ) // 2

        for particle in self.move_particles:

            life = particle["life"]

            x = int(
                offset_x
                + particle["x"]
            )

            y = int(
                offset_y
                + particle["y"]
            )

            radius = max(
                1,
                int(
                    particle["size"]
                    * life
                )
            )

            pygame.draw.circle(
                self.screen,
                self.accent_color,
                (x, y),
                radius
            )

    # ========================================================
    # PLAYER
    # ========================================================

    def draw_player(self):

        size = self.maze.tile_size

        maze_width = (
            self.maze.cols * size
        )

        maze_height = (
            self.maze.rows * size
        )

        offset_x = (
            self.width() - maze_width
        ) // 2

        offset_y = (
            self.height() - maze_height
        ) // 2

        speed_ratio = min(
            self.player_speed / 5.5,
            1.0
        )

        # Nice idle breathing
        idle_time = time.time()

        idle_bob = (
            math.sin(idle_time * 4.5)
            * 1.5
        )

        # Movement bounce
        move_bob = (
            math.sin(
                self.bounce * 1.8
            )
            * 2.5
            * speed_ratio
        )

        bob = (
            idle_bob * (1 - speed_ratio)
            + move_bob
        )

        x = (
            offset_x
            + self.visual_x
        )

        y = (
            offset_y
            + self.visual_y
            + bob
        )

        radius = size // 3

        # Squash / stretch
        squash = min(
            self.squash,
            1.0
        )

        if abs(
            self.player_dir_x
        ) >= abs(
            self.player_dir_y
        ):

            width_scale = (
                1.0
                + 0.34 * speed_ratio
                + 0.08 * squash
            )

            height_scale = (
                1.0
                - 0.20 * speed_ratio
                - 0.06 * squash
            )

        else:

            width_scale = (
                1.0
                - 0.20 * speed_ratio
                - 0.06 * squash
            )

            height_scale = (
                1.0
                + 0.34 * speed_ratio
                + 0.08 * squash
            )

        ball_w = (
            radius * 2 * width_scale
        )

        ball_h = (
            radius * 2 * height_scale
        )

        # Shadow
        shadow_rect = pygame.Rect(
            0,
            0,
            ball_w * 0.95,
            ball_h * 0.38
        )

        shadow_rect.center = (
            int(x + 4),
            int(
                offset_y
                + self.visual_y
                + radius * 0.78
            )
        )

        pygame.draw.ellipse(
            self.screen,
            (5, 6, 8),
            shadow_rect
        )

        # Glow behind roller while moving
        if speed_ratio > 0.05:

            self.fx_surface.fill((0, 0, 0, 0))

            glow_radius = int(
                radius
                * (
                    1.25
                    + 0.5 * speed_ratio
                )
            )

            alpha = int(
                25 + 45 * speed_ratio
            )

            pygame.draw.circle(
                self.fx_surface,
                (*self.accent_color, alpha),
                (int(x), int(y)),
                glow_radius
            )

            self.screen.blit(
                self.fx_surface,
                (0, 0)
            )

        # Main roller
        ball_rect = pygame.Rect(
            0,
            0,
            ball_w,
            ball_h
        )

        ball_rect.center = (
            int(x),
            int(y)
        )

        pygame.draw.ellipse(
            self.screen,
            self.roller_outer,
            ball_rect
        )

        core_rect = ball_rect.inflate(
            -6,
            -6
        )

        pygame.draw.ellipse(
            self.screen,
            self.roller_inner,
            core_rect
        )

        # Rotating wheel marks
        rolling_radius = (
            min(ball_w, ball_h)
            * 0.30
        )

        for spot_offset in (
            0.0,
            math.pi
        ):

            angle = (
                self.player_angle
                + spot_offset
            )

            spot_x = (
                x
                + math.cos(angle)
                * rolling_radius
            )

            spot_y = (
                y
                + math.sin(angle)
                * rolling_radius
                * (
                    ball_h
                    / max(ball_w, 1)
                )
            )

            mark_x, mark_y = int(spot_x), int(spot_y)
            mark_r = max(2, int(radius * 0.16))

            if self.roller_style == "diamond":
                pygame.draw.polygon(
                    self.screen, self.roller_mark,
                    [(mark_x, mark_y - mark_r),
                     (mark_x + mark_r, mark_y),
                     (mark_x, mark_y + mark_r),
                     (mark_x - mark_r, mark_y)]
                )
            elif self.roller_style == "hex":
                pygame.draw.circle(self.screen, self.roller_mark, (mark_x, mark_y), mark_r)
                pygame.draw.circle(self.screen, self.roller_inner, (mark_x, mark_y), max(1, mark_r // 2))
            elif self.roller_style == "heart":
                pygame.draw.circle(self.screen, self.roller_mark, (mark_x - mark_r // 2, mark_y), mark_r // 2)
                pygame.draw.circle(self.screen, self.roller_mark, (mark_x + mark_r // 2, mark_y), mark_r // 2)
                pygame.draw.polygon(self.screen, self.roller_mark,
                                    [(mark_x - mark_r, mark_y),
                                     (mark_x + mark_r, mark_y),
                                     (mark_x, mark_y + mark_r + 2)])
            elif self.roller_style == "ring":
                pygame.draw.circle(self.screen, self.roller_mark, (mark_x, mark_y), mark_r, max(1, mark_r // 2))
            else:
                pygame.draw.circle(self.screen, self.roller_mark, (mark_x, mark_y), mark_r)

        # Highlight
        highlight_rect = pygame.Rect(
            0,
            0,
            ball_w * 0.50,
            ball_h * 0.40
        )

        highlight_rect.center = (
            int(
                x - ball_w * 0.18
            ),
            int(
                y - ball_h * 0.22
            )
        )

        pygame.draw.ellipse(
            self.screen,
            self.tile_highlight,
            highlight_rect
        )

        pygame.draw.ellipse(
            self.screen,
            self.roller_outer,
            ball_rect,
            2
        )

        # Small motion ring
        if speed_ratio > 0.25:

            ring_radius = int(
                radius
                * (
                    1.1
                    + speed_ratio * 0.25
                )
            )

            pygame.draw.circle(
                self.screen,
                self.accent_color,
                (int(x), int(y)),
                ring_radius,
                1
            )

    # ========================================================
    # HUD
    # ========================================================

    def draw_hud(self):

        font = self.font_hud
        small = self.font_hud_small

        painted = len(
            self.maze.painted
        )

        total = (
            self.maze.total_paintable
        )

        percent = (
            int(
                painted / total * 100
            )
            if total
            else 100
        )

        text = font.render(
            f"PAINTED   {percent}%",
            True,
            (235, 238, 245)
        )

        self.screen.blit(
            text,
            (25, 20)
        )

        bar_x = 25
        bar_y = 48
        bar_width = 230
        bar_height = 8

        pygame.draw.rect(
            self.screen,
            (42, 45, 54),
            (
                bar_x,
                bar_y,
                bar_width,
                bar_height
            ),
            border_radius=4
        )

        pygame.draw.rect(
            self.screen,
            self.accent_color,
            (
                bar_x,
                bar_y,
                int(
                    bar_width
                    * percent
                    / 100
                ),
                bar_height
            ),
            border_radius=4
        )

        minutes = int(
            self.elapsed // 60
        )

        seconds = int(
            self.elapsed % 60
        )

        timer_text = font.render(
            f"{minutes:02d}:{seconds:02d}",
            True,
            (235, 238, 245)
        )

        timer_rect = timer_text.get_rect(
            top=20,
            right=self.width() - 25
        )

        self.screen.blit(
            timer_text,
            timer_rect
        )

        controls = small.render(
            "WASD / ARROWS  •  SWIPE / DRAG  •  SPACE: PAUSE",
            True,
            (115, 120, 132)
        )

        controls_rect = controls.get_rect(
            bottom=18,
            centerx=self.width() // 2
        )

        self.screen.blit(
            controls,
            controls_rect
        )

    # ========================================================
    # PAUSE
    # ========================================================

    def draw_pause(self):

        self.fx_surface.fill(
            (5, 6, 10, 180)
        )

        self.screen.blit(
            self.fx_surface,
            (0, 0)
        )

        text = self.font_pause.render(
            "PAUSED",
            True,
            (255, 255, 255)
        )

        rect = text.get_rect(
            center=(
                self.width() // 2,
                self.height() // 2
            )
        )

        self.screen.blit(
            text,
            rect
        )

    # ========================================================
    # COMPLETE
    # ========================================================

    def draw_complete(self):

        self.fx_surface.fill(
            (5, 7, 10, 170)
        )

        self.screen.blit(
            self.fx_surface,
            (0, 0)
        )

        font = self.font_complete_title
        small = self.font_complete_small

        title = font.render(
            "LEVEL COMPLETE!",
            True,
            (95, 230, 125)
        )

        title_rect = title.get_rect(
            center=(
                self.width() // 2,
                self.height() // 2 - 30
            )
        )

        self.screen.blit(
            title,
            title_rect
        )
        print("STARS =", self.stars)
        stars = (
            "★" * self.stars
            + "☆" * (3 - self.stars)
        )

        info = small.render(
            f"Level {self.level} complete  •  {stars}",
            True,
            (255, 211, 90)
        )

        info_rect = info.get_rect(
            center=(
                self.width() // 2,
                self.height() // 2 + 25
            )
        )

        self.screen.blit(
            info,
            info_rect
        )

        hint = small.render(
            "Press ENTER to continue",
            True,
            (150, 155, 165)
        )

        hint_rect = hint.get_rect(
            center=(
                self.width() // 2,
                self.height() // 2 + 60
            )
        )

        self.screen.blit(
            hint,
            hint_rect
        )

    # ========================================================
    # COMPLETE PARTICLES
    # ========================================================

    def create_particles(self):

        cx = self.width() // 2
        cy = self.height() // 2

        for _ in range(100):

            self.particles.append({
                "x": cx,
                "y": cy,
                "vx": random.uniform(-5, 5),
                "vy": random.uniform(-5, 5),
                "life": random.uniform(
                    0.5,
                    1.5
                ),
                "size": random.uniform(
                    2,
                    6
                )
            })

    def update_particles(self):

        for particle in self.particles:

            particle["x"] += (
                particle["vx"]
            )

            particle["y"] += (
                particle["vy"]
            )

            particle["vy"] += 0.15

            particle["life"] -= 0.016

        self.particles = [
            p
            for p in self.particles
            if p["life"] > 0
        ]

        for particle in self.move_particles:

            particle["x"] += (
                particle["vx"]
            )

            particle["y"] += (
                particle["vy"]
            )

            particle["vx"] *= 0.96
            particle["vy"] *= 0.96

            particle["life"] -= 0.045

        self.move_particles = [
            p
            for p in self.move_particles
            if p["life"] > 0
        ]

    def draw_particles(self):

        for particle in self.particles:

            radius = max(
                1,
                int(
                    particle["size"]
                    * min(
                        particle["life"],
                        1
                    )
                )
            )

            pygame.draw.circle(
                self.screen,
                (95, 230, 125),
                (
                    int(particle["x"]),
                    int(particle["y"])
                ),
                radius
            )

    # ========================================================
    # RESTART
    # ========================================================

    def restart(self):

        if not self.pygame_initialized:
            return

        self.load_level()

        self.setFocus()

    # ========================================================
    # RESIZE
    # ========================================================

    def resizeEvent(self, event):

        if self.pygame_initialized:

            width = max(
                1,
                self.width()
            )

            height = max(
                1,
                self.height()
            )

            self.screen = pygame.display.set_mode(
                (width, height)
            )

            self.trail_surface = pygame.Surface(
                (width, height),
                pygame.SRCALPHA
            )

            self.fx_surface = pygame.Surface(
                (width, height),
                pygame.SRCALPHA
            )

        super().resizeEvent(event)

    # ========================================================
    # STOP
    # ========================================================

    def stop(self):

        self.timer.stop()

        if self.pygame_initialized:

            pygame.quit()

            self.pygame_initialized = False
