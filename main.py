import pygame
from grid import Grid


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screenSize = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.Running = True
        self.grid = Grid(9,9,10)
        self.grid.create_grid()
        self.grid.draw()

    def run(self):
        while self.Running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL]:
                self.Running = False

            time = self.clock.tick() / 1000
            
            pygame.display.flip()