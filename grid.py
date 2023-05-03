import pygame
from tiles import Tile
import random

class Grid:
    def __init__(self,x_size:int,y_size:int,num_mines:int,tile_images:str):
        self.x_size:int = x_size
        self.y_size:int = y_size
        self.num_mines:int = num_mines
        self.tile_images:str = tile_images
        self.grid:list[list[Tile]] = []

    def create_grid(self):
        even_or_odd = 0
        for y in range(self.y_size):
            self.grid.append([])
            for x in range(self.x_size):
                even_or_odd += 1
                self.grid[y].append(Tile((x,y),(self.x_size,self.y_size),self.tile_images, even_or_odd))
            if self.x_size%2 == 0:
                even_or_odd += 1

    def mine_gen(self):
        count = 0
        while True:
            ranx = random.randint(0,self.x_size-1)
            rany = random.randint(0,self.y_size-1)
            
            if self.grid[rany][ranx].is_mine == False and self.grid[rany][ranx].cant_be_mine == False:
                self.grid[rany][ranx].is_mine = True
                count += 1
            if count == self.num_mines:
                break
        
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if tile.is_mine:
                    if x+1 < self.x_size:
                        self.grid[y][x+1].near_by_mines += 1
                    if x-1 >= 0:
                        self.grid[y][x-1].near_by_mines += 1
                    if y+1 < self.y_size:
                        self.grid[y+1][x].near_by_mines += 1
                    if y-1 >= 0:
                        self.grid[y-1][x].near_by_mines += 1
                    if x+1 < self.x_size and y+1 < self.y_size:
                        self.grid[y+1][x+1].near_by_mines += 1
                    if x-1 >= 0 and y-1 >= 0:
                        self.grid[y-1][x-1].near_by_mines += 1
                    if x+1 < self.x_size and y-1 >= 0:
                        self.grid[y-1][x+1].near_by_mines += 1
                    if x-1 >= 0 and y+1 < self.y_size:
                        self.grid[y+1][x-1].near_by_mines += 1 
    
    def draw(self):
        for row in self.grid:
            for tile in row:
                tile.draw()