import pygame
from pygame.math import Vector2
import random
from tiles import Tile


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screenSize:tuple[int,int] = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.tile_images:str = "tile_images.png"
        self.grid_size:Vector2 = Vector2(9,9)
        self.num_mines:int = 10
        self.tile_size:Vector2 = Vector2(self.screenSize[0]/self.grid_size.x,self.screenSize[1]/self.grid_size.y)
        self.tiles_around:list[Vector2] = [
            Vector2(-1,-1),Vector2(0,-1),Vector2(1,-1),
            Vector2(-1,0),Vector2(0,0),Vector2(1,0),
            Vector2(-1,1),Vector2(0,1),Vector2(1,1)
        ]
        self.grid:list[list[Tile]] = []
        self.create_grid()

        self.Running:bool = True
        self.first_click:bool = False
        self.queue:list[Tile] = [] 
        


    def run(self):
        while self.Running:
            #self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL]:
                self.Running = False
            mouse_press = pygame.mouse.get_pressed()
            if mouse_press[0] == 1:
                self.left_click()
            elif mouse_press[1] == 1:
                pass
            elif mouse_press[2] == 1:
                self.right_click()

            self.reveal()


            time = self.clock.tick() / 1000
            self.screen.fill((255,255,255))
            for row in self.grid:
                for tile in row:
                    tile.draw(self.screen)
            
            pygame.display.flip()


    def left_click(self):
        breakflag = False
        mouse = pygame.mouse.get_pos()
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if tile.hitbox.collidepoint(mouse):
                    if not self.first_click:
                        self.first_click = True
                        for i in self.tiles_around:
                            self.grid[int(y+i.y)][int(x+i.x)].cant_be_mine = True
                        self.mine_gen()
                    if tile.is_mine and tile.flaged == False:
                        print("YOU LOOSE")
                    elif tile.nearby_mines > 0:
                        tile.is_clicked = True
                    else:
                        self.queue.append(tile)
                    breakflag = True
                    break
            if breakflag:
                break


    def right_click(self):
        breakflag = False
        mouse = pygame.mouse.get_pos()
        for row in self.grid:
            for tile in row:
                if tile.hitbox.collidepoint(mouse):
                    tile.flaged = True
                    breakflag = True
                    break
            if breakflag:
                break


    def reveal(self):
        index = 0
        while index < len(self.queue):
            tile:Tile = self.queue[index]
            for i in self.tiles_around:
                if ((tile.grid_pos.x+i.x >= 0 and 
                    tile.grid_pos.x+i.x < self.grid_size.x)
                and
                    (tile.grid_pos.y+i.y >= 0 and 
                    tile.grid_pos.y+i.y < self.grid_size.y)
                ):
                    current_tile:Tile = self.grid[int(tile.grid_pos.y+i.y)][int(tile.grid_pos.x+i.x)]
                    
                    if tile.nearby_mines == 0 and tile.is_mine == False:
                        current_tile.is_clicked = True
                        if current_tile not in self.queue:
                            self.queue.append(current_tile)
            index += 1
        # for i in self.queue:
        #     print(i.grid_pos)
        self.queue = []
        index = 0

    def create_grid(self):
        even_or_odd = 0
        for y in range(int(self.grid_size.y)):
            self.grid.append([])
            for x in range(int(self.grid_size.x)):
                even_or_odd += 1
                self.grid[y].append(Tile(Vector2(x,y),self.tile_images, even_or_odd,int(self.tile_size.y)))
            if self.grid_size.x%2 == 0:
                even_or_odd += 1

    def mine_gen(self):
        count = 0
        while True:
            ranx = random.randint(0,int(self.grid_size.x)-1)
            rany = random.randint(0,int(self.grid_size.y)-1)
            
            if self.grid[rany][ranx].is_mine == False and self.grid[rany][ranx].cant_be_mine == False:
                self.grid[rany][ranx].is_mine = True
                count += 1
            if count == self.num_mines:
                break
        
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if tile.is_mine:
                    if x+1 < self.grid_size.x:
                        self.grid[y][x+1].nearby_mines += 1
                    if x-1 >= 0:
                        self.grid[y][x-1].nearby_mines += 1
                    if y+1 < self.grid_size.y:
                        self.grid[y+1][x].nearby_mines += 1
                    if y-1 >= 0:
                        self.grid[y-1][x].nearby_mines += 1
                    if x+1 < self.grid_size.x and y+1 < self.grid_size.y:
                        self.grid[y+1][x+1].nearby_mines += 1
                    if x-1 >= 0 and y-1 >= 0:
                        self.grid[y-1][x-1].nearby_mines += 1
                    if x+1 < self.grid_size.x and y-1 >= 0:
                        self.grid[y-1][x+1].nearby_mines += 1
                    if x-1 >= 0 and y+1 < self.grid_size.y:
                        self.grid[y+1][x-1].nearby_mines += 1 
        
        


















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