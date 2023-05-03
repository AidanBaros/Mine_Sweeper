import pygame
from grid import Grid


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screenSize = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.Running = True
        self.tile_images:str = "tile_images.png"
        self.grid = Grid(9,9,10, self.tile_images)
        self.grid.create_grid()
        self.first_click = False

    def run(self):
        while self.Running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL]:
                self.Running = False
            mouse = pygame.mouse.get_pressed()
            if mouse[0] == 1:
                self.left_click()
            elif mouse[1] == 1:
                self.right_click()
            elif mouse[2] == 1:
                pass

            time = self.clock.tick() / 1000
            self.screen.fill((255,255,255))
            self.grid.draw()
            
            pygame.display.flip()

    def left_click(self):
        breakflag = False
        mouse_pos = pygame.mouse.get_pos()
        for y, row in enumerate(self.grid.grid):
            for x, tile in enumerate(row):
                if tile.collide():
                    if not self.first_click:
                        self.grid.mine_gen()
                        self.first_click = True
                        tile.cant_be_mine = True
                        self.grid.grid[y+1][x+1].cant_be_mine = True
                        self.grid.grid[y+1][x].cant_be_mine = True
                        self.grid.grid[y+1][x-1].cant_be_mine = True
                        self.grid.grid[y][x+1].cant_be_mine = True
                        self.grid.grid[y][x-1].cant_be_mine = True
                        self.grid.grid[y-1][x+1].cant_be_mine = True
                        self.grid.grid[y-1][x].cant_be_mine = True
                        self.grid.grid[y-1][x-1].cant_be_mine = True
                    tile.is_clicked = True
                    breakflag = True
                    break
            if breakflag:
                break
                            

    def right_click(self):
        pass