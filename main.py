import pygame
from pygame.math import Vector2
import random
from tiles import Tile


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_size:Vector2 = Vector2(self.screen.get_size())
        self.clock = pygame.time.Clock()
        self.tile_images:str = "tile_images.png"
        self.grid_size:Vector2 = Vector2(10,8)
        self.max_num_mines = int(self.grid_size.x * self.grid_size.y * 0.5)
        self.num_mines:int = 10
        self.tiles_around:list[Vector2] = [
            Vector2(-1,-1),Vector2(0,-1),Vector2(1,-1),
            Vector2(-1,0),Vector2(0,0),Vector2(1,0),
            Vector2(-1,1),Vector2(0,1),Vector2(1,1)
        ]
        if self.screen_size.x/self.grid_size.x < self.screen_size.y/self.grid_size.y:
            self.tile_size = int(self.screen_size.x/self.grid_size.x)
        else:
            self.tile_size = int(self.screen_size.y/self.grid_size.y)
        self.grid:list[list[Tile]] = []
        self.create_grid()

        self.mouse_check = False
        self.Running:bool = True
        self.first_click:bool = False
        self.queue:list[Tile] = []
        

    def run(self):
        while self.Running:
            #self.clock.tick(60)
            for event in pygame.event.get():
                mouse_press = pygame.mouse.get_pressed()
                if event.type == pygame.QUIT:
                    self.Running = False
                if event.type == pygame.MOUSEBUTTONDOWN and not self.mouse_check:
                    self.mouse_check = True
                    if mouse_press[0] == 1:
                        self.left_click()
                    elif mouse_press[1] == 1:
                        self.middle_click()
                    elif mouse_press[2] == 1 and self.first_click:
                        self.right_click()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_check = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL]:
                self.Running = False
            
            self.win_check()
            self.loose_check()

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
                    if not tile.flaged:
                        if not self.first_click:
                            self.first_click = True
                            for i in self.tiles_around:
                                if self.offscreen(tile.grid_pos,i):
                                    self.grid[int(y+i.y)][int(x+i.x)].cant_be_mine = True
                            self.mine_gen()
                        if tile.is_mine:
                            tile.clicked = True
                        elif tile.nearby_mines > 0:
                            tile.clicked = True
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
                if tile.hitbox.collidepoint(mouse) and not tile.clicked:
                    if not tile.flaged:
                        tile.flaged = True
                    elif tile.flaged:
                        tile.flaged = False
                    breakflag = True
                    break
            if breakflag:
                break


    def middle_click(self):
        breakflag = False
        mouse = pygame.mouse.get_pos()
        for row in self.grid:
            for tile in row:
                if tile.hitbox.collidepoint(mouse) and tile.clicked:
                    around_check = 0
                    for i in self.tiles_around:
                        if self.offscreen(tile.grid_pos,i):
                            if self.grid[int(tile.grid_pos.y + i.y)][int(tile.grid_pos.x + i.x)].flaged:
                                around_check += 1
                    grid = self.grid[int(tile.grid_pos.y)][int(tile.grid_pos.x)]
                    if grid.nearby_mines <= around_check:
                        for i in self.tiles_around:
                            if self.offscreen(tile.grid_pos,i):
                                grid  = self.grid[int(tile.grid_pos.y + i.y)][int(tile.grid_pos.x + i.x)]
                                if self.offscreen(tile.grid_pos,i) and not grid.flaged:
                                    self.queue.append(grid)
                                    grid.clicked = True
                    breakflag = True
                    break
            if breakflag:
                break

        
    def offscreen(self, current_pos:Vector2, offset:Vector2):
        if ((current_pos.x + offset.x >= 0 and 
            current_pos.x + offset.x < self.grid_size.x)
        and
            (current_pos.y + offset.y >= 0 and 
            current_pos.y + offset.y < self.grid_size.y)
        ):
            return True
        return False


    def reveal(self):
        index = 0
        while index < len(self.queue):
            tile:Tile = self.queue[index]
            for i in self.tiles_around:
                if self.offscreen(tile.grid_pos,i):
                    current_tile:Tile = self.grid[int(tile.grid_pos.y+i.y)][int(tile.grid_pos.x+i.x)]
                    if tile.nearby_mines == 0 and not tile.is_mine and not tile.flaged:
                        current_tile.clicked = True
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
                self.grid[y].append(Tile(Vector2(x,y), self.tile_images, even_or_odd, self.tile_size))
            if self.grid_size.x%2 == 0:
                even_or_odd += 1


    def mine_gen(self):
        count = 0
        while True:
            ranx = random.randint(0,int(self.grid_size.x)-1)
            rany = random.randint(0,int(self.grid_size.y)-1)
            grid = self.grid[rany][ranx]
            self.count()
            continueflag = False
            for i in self.tiles_around:
                if self.offscreen(grid.grid_pos,i):
                    if self.grid[int(rany+i.y)][int(ranx+i.x)].nearby_mines >= 7:
                        continueflag = True
                        break
            if continueflag:
                continue
            if grid.is_mine == False and grid.cant_be_mine == False:
                grid.is_mine = True
                count += 1
            if count == self.num_mines:
                self.count()
                break


    def count(self):
        for row in self.grid:
            for tile in row:
                tile.nearby_mines = 0

        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if tile.is_mine:
                    for i in self.tiles_around:
                        if self.offscreen(tile.grid_pos,i):
                            self.grid[int(y+i.y)][int(x+i.x)].nearby_mines += 1 


    def win_check(self):
        not_mine = (self.grid_size.x * self.grid_size.y) - self.num_mines
        check = 0
        for row in self.grid:
            for tile in row:
                if not tile.is_mine and tile.clicked:
                    check += 1
        if not_mine == check:
            print("YOU WIN")


    def loose_check(self):
        for row in self.grid:
            for tile in row:
                if tile.is_mine and tile.clicked:
                    print("YOU LOOSE")
