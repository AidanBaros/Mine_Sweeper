import pygame
from pygame.math import Vector2
import random
from tiles import Tile
from button import Button
import time


class Game:
    def __init__(self):
        self.playing = True
        pygame.init()
        self.screen:pygame.surface.Surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_size:Vector2 = Vector2(self.screen.get_size())
        self.clock:pygame.time.Clock = pygame.time.Clock()
        self.tile_images:str = "tile_images.png"
        self.flag:pygame.image = pygame.image.load(self.tile_images)
        self.grid_size:Vector2
        self.num_mines:int
        self.center_on_x:bool
        self.x_offset:int = int(self.screen_size.x * 0.05)
        self.y_offset:int = int(self.screen_size.y * 0.05)
        self.tiles_around:list[Vector2] = [
            Vector2(-1,-1),Vector2(0,-1),Vector2(1,-1),
            Vector2(-1,0),Vector2(0,0),Vector2(1,0),
            Vector2(-1,1),Vector2(0,1),Vector2(1,1)
        ]
        self.font = pygame.font.SysFont("Roboto", int(self.screen_size.y/27))
        self.flag = pygame.transform.scale(self.flag,(int(self.screen_size.y * 0.04)*13,int(self.screen_size.y * 0.04)))

        self.grid:list[list[Tile]] = []
        self.start_tick:int = 0
        self.mouse_check:bool = False
        self.Running:bool = True
        self.first_click:bool = False
        self.queue:list[Tile] = []
        self.num_flags:int = 0
        self.in_UI:bool = True
        self.button_list:list[Button] = []
        self.seconds:int = 0
        self.last_time:str =  "---"


    def run(self):
        while self.playing:
            if self.in_UI:
                self.UI()
            self.game()
            self.grid:list[list[Tile]] = []
            self.start_tick:int = 0
            self.mouse_check:bool = False
            self.Running:bool = True
            self.first_click:bool = False
            self.queue:list[Tile] = []
            self.num_flags:int = 0
            self.in_UI:bool = True
            self.button_list:list[Button] = []
            self.seconds:int = 0


    def left_click(self):
        breakflag = False
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if tile.hitbox.collidepoint(self.mouse_pos):
                    if not tile.flaged:
                        if not self.first_click:
                            self.first_click = True
                            self.start_tick = pygame.time.get_ticks()
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
                self.grid[y].append(Tile(Vector2(x,y), self.tile_images, even_or_odd, self.tile_size, self.x_offset, self.y_offset))
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


    def win_check(self, seconds):
        not_mine = (self.grid_size.x * self.grid_size.y) - self.num_mines
        check = 0
        for row in self.grid:
            for tile in row:
                if not tile.is_mine and tile.clicked:
                    check += 1
        if not_mine == check:
            self.last_time = str(seconds)
            self.Running = False
            self.in_UI = True


    def loose_check(self):
        for row in self.grid:
            for tile in row:
                if tile.is_mine and tile.clicked:
                    print("YOU LOOSE")
                    self.Running = False
                    self.in_UI = True


    def edge_display(self):
        self.screen.blit(
            self.flag,
            (self.x_offset + (self.tile_size*self.grid_size.x) - self.screen_size.y * 0.04,(self.screen_size.y*0.01)),
            (int((self.screen_size.y * 0.04)*7),0,int(self.screen_size.y * 0.04),int(self.screen_size.y * 0.04))
            )
        text = self.font.render(str(self.num_mines - self.num_flags), True, "white")
        self.screen.blit(
            text,
            (self.x_offset + (self.tile_size*self.grid_size.x) - ((text.get_width()) + (self.screen_size.y * 0.04)),(self.screen_size.y*0.01))
            )
        self.screen.blit(
            self.font.render(f"Time: {self.seconds}", True, "white"), 
            (self.x_offset,(self.screen_size.y*0.01))
            )


    def update(self):
        self.mouse_pos:tuple[int,int] = pygame.mouse.get_pos()
        self.num_flags = 0
        for row in self.grid:
            for tile in row:
                if tile.flaged:
                    self.num_flags += 1
        self.seconds = round((pygame.time.get_ticks() - self.start_tick) / 1000)
        if not self.first_click:
            self.seconds = 0
        self.win_check(self.seconds)
        self.loose_check()

        self.reveal()

        self.screen.fill((0,100,0))
        for row in self.grid:
            for tile in row:
                tile.draw(self.screen)
        
        self.edge_display()


    def start_up(self):
        self.max_num_mines:int = int(self.grid_size.x * self.grid_size.y * 0.5)
        if self.screen_size.x/self.grid_size.x < self.screen_size.y/self.grid_size.y:
            self.tile_size = int((self.screen_size.x*0.9)/self.grid_size.x)
            self.center_on_x = False
            self.y_offset = int((self.screen_size.y - (self.grid_size.y * self.tile_size))/2)
        else:
            self.tile_size = int((self.screen_size.y*0.9)/self.grid_size.y)
            self.center_on_x = True
            self.x_offset = int((self.screen_size.x - (self.grid_size.x * self.tile_size))/2)
        self.create_grid()


    def game(self):
        while self.Running:
            self.clock.tick(60)
            for event in pygame.event.get():
                mouse_press = pygame.mouse.get_pressed()
                if event.type == pygame.QUIT:
                    self.quit()
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
            if keys[pygame.K_LCTRL] or keys[pygame.K_ESCAPE]:
                self.quit()
            
            self.update()

            pygame.display.flip()


    def UI(self):
        easy = Button("Easy",Vector2(self.screen_size.x/2 - (self.screen_size.x * 0.25),self.screen_size.y/1.25),Vector2(self.screen_size.x * 0.2,self.screen_size.y * 0.1),(0,190,0),(0,0,0))
        self.button_list.append(easy)
        medium = Button("Medium",Vector2(self.screen_size.x/2,self.screen_size.y/1.25),Vector2(self.screen_size.x * 0.2,self.screen_size.y * 0.1),(0,190,0),(0,0,0))
        self.button_list.append(medium)
        hard = Button("Hard",Vector2(self.screen_size.x/2 + (self.screen_size.x * 0.25),self.screen_size.y/1.25),Vector2(self.screen_size.x * 0.2,self.screen_size.y * 0.1),(0,190,0),(0,0,0))
        self.button_list.append(hard)

        while self.in_UI:
            self.mouse_pos:tuple[int,int] = pygame.mouse.get_pos()
            self.clock.tick(60)
            for event in pygame.event.get():
                mouse_press = pygame.mouse.get_pressed()
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEBUTTONDOWN and not self.mouse_check:
                    self.mouse_check = True
                    if mouse_press[0] == 1:
                        for button in self.button_list:
                            if button.collide(self.mouse_pos):
                                if button == easy:
                                    self.grid_size = Vector2(10,8)
                                    self.num_mines = 10
                                if button == medium:
                                    self.grid_size = Vector2(18,14)
                                    self.num_mines = 40
                                if button == hard:
                                    self.grid_size = Vector2(24,20)
                                    self.num_mines = 100
                                self.start_up()
                                self.in_UI = False
                                self.Running = True
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_check = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL] or keys[pygame.K_ESCAPE]:
                self.quit()

            self.screen.fill((0,100,0))
            for button in self.button_list:
                button.draw(self.screen)

            pygame.display.flip()


    def quit(self):
        self.Running = False
        self.in_UI = False
        self.playing = False