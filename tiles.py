import pygame

class Tile:
    def __init__(self,pos:tuple[int,int], grid_dimentions:tuple[int,int]):
        self.screen:pygame.surface.Surface = pygame.display.get_surface()
        self.screen_size:tuple[int,int] = self.screen.get_size()
        self.grid_dimentions:tuple[int,int] = grid_dimentions
        self.grid_pos:tuple[int,int] = pos
        self.size = 120#self.screen_size[0]//self.grid_dimentions[0]
        self.pos:tuple[int,int] = (self.size*self.grid_pos[0],self.size*self.grid_pos[1])
        self.near_by_mines:int = 0
        self.is_mine:bool = False
        self.is_clicked:bool = False
        self.flaged:bool = False
        self.image = None

    def draw(self):
        color = (255,255,255)
        if self.is_mine:
            color = (0,0,0)
        elif self.near_by_mines > 0:
            color = (255-(50*self.near_by_mines),255-(50*self.near_by_mines),255-(50*self.near_by_mines))
        pygame.draw.rect(self.screen,color,(self.pos[0],self.pos[1],self.size,self.size))