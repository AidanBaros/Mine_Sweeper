import pygame
from grid import Grid
from tiles import Tile


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screenSize = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.Running:bool = True
        self.tile_images:str = "tile_images.png"
        self.grid_size:tuple[int,int] = (9,9)
        self.grid:Grid = Grid(self.grid_size,10, self.tile_images)
        self.grid.create_grid()
        self.first_click:bool = False
        self.tiles_around:list[tuple[int,int]] = [
            (-1,-1),(-1,0),(-1,1),
            (0,-1),(0,0),(0,1),
            (1,-1),(1,0),(1,1)
        ]
        self.queue:list = [] 

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
        for y, row in enumerate(self.grid.grid):
            for x, tile in enumerate(row):
                if tile.collide():
                    if not self.first_click:
                        self.first_click = True
                        for i in self.tiles_around:
                            self.grid.grid[y+i[0]][x+i[1]].cant_be_mine = True
                        self.grid.mine_gen()
                    self.queue.append(tile)
                    self.reveal()
                    breakflag = True
                    break
            if breakflag:
                break
                            

    def right_click(self):
        pass

    def reveal(self):
        index = 0
        temp = []
        while index < len(self.queue):
            tile:Tile = self.queue[index]
            for i in self.tiles_around:
                if ((tile.grid_pos[0]+i[0] >= 0 and 
                    tile.grid_pos[0]+i[0] < self.grid_size[0])
                and
                    (tile.grid_pos[1]+i[1] >= 0 and 
                    tile.grid_pos[1]+i[1] < self.grid_size[1])
                ):
                    grid_pos = self.grid.grid[tile.grid_pos[0]+i[0]][tile.grid_pos[1]+i[1]]
                    grid_pos.is_clicked = True
                    if tile.near_by_mines == 0 and (grid_pos not in self.queue):
                        self.queue.append(grid_pos)
                else:
                    continue
            index += 1
            # self.queue.extend(temp)
            # self.queue = list(set(self.queue))

            
        self.queue = []
        index = 0
        #tile.is_clicked = True
        


















"""
while True:
                        current_pos = (y,x)
                        next_pos = None
                        number_checked = 0
                        check = 0
                        for i in self.tiles_around:
                            if ((current_pos[0]+i[0] >= 0 and 
                                current_pos[0]+i[0] <= self.grid_size[0])
                            and
                                (current_pos[1]+i[1] >= 0 and 
                                current_pos[1]+i[1] <= self.grid_size[1])
                            ):
                                grid_pos = self.grid.grid[current_pos[0]+i[0]][current_pos[1]+i[1]]
                                number_checked += 1
                            else:
                                continue
                            if not grid_pos.is_clicked:
                                grid_pos.is_clicked = True
                                if grid_pos.near_by_mines > 0 or i == (0,0):
                                    grid_pos.checked = True
                                if next_pos == None:
                                    next_pos = grid_pos.grid_pos
                        for j in self.tiles_around:
                            if self.grid.grid[current_pos[0]+j[0]][current_pos[1]+j[1]].checked:
                                check += 1
                        if check == number_checked:
                            break
                        current_pos = next_pos

"""