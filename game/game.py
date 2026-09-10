import pygame

from game.maze import Maze
from game.player import Player


class Game:

    def __init__(self):

        pygame.init()

        self.maze = Maze(
            "levels/level_01.json"
        )

        width = self.maze.cols * self.maze.tile_size
        height = self.maze.rows * self.maze.tile_size

        self.screen = pygame.display.set_mode(
            (width, height)
        )

        pygame.display.set_caption(
            "Maze Paint"
        )

        self.clock = pygame.time.Clock()

        self.player = Player(
            self.maze
        )

        self.running = True
        self.completed = False

        self.font = pygame.font.SysFont(
            "arial",
            42,
            bold=True
        )




    def handle_events(self):

     for event in pygame.event.get():

         if event.type == pygame.QUIT:
             self.running = False

         self.player.handle_keyboard(event)
         self.player.handle_mouse(event)


    def update(self):

        if self.maze.is_complete():
            self.completed = True

    def draw(self):

        self.screen.fill(
            (245, 245, 250)
        )

        self.maze.draw(
            self.screen
        )

        self.player.draw(
            self.screen
        )

        if self.completed:

            overlay = pygame.Surface(
                self.screen.get_size(),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 150)
            )

            self.screen.blit(
                overlay,
                (0, 0)
            )

            text = self.font.render(
                "LEVEL COMPLETE!",
                True,
                (255, 255, 255)
            )

            rect = text.get_rect(
                center=self.screen.get_rect().center
            )

            self.screen.blit(
                text,
                rect
            )

        pygame.display.flip()

    def run(self):

        while self.running:

            self.handle_events()

            self.update()

            self.draw()

            self.clock.tick(60)

        pygame.quit()
