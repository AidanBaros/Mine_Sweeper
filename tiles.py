import pygame

class Tile:
    def __init__(self,pos:tuple[int,int], grid_dimentions:tuple[int,int], tile_images:str, even_odd:int):
        self.screen:pygame.surface.Surface = pygame.display.get_surface()
        self.screen_size:tuple[int,int] = self.screen.get_size()
        self.grid_dimentions:tuple[int,int] = grid_dimentions
        self.grid_pos:tuple[int,int] = pos
        self.tile_images = pygame.image.load(tile_images)
        self.even_odd:int = even_odd%2
        self.size = self.screen_size[1]//self.grid_dimentions[1]
        self.pos:tuple[int,int] = (self.size*self.grid_pos[0],self.size*self.grid_pos[1])
        self.image_size:tuple[int,int] = (416,32)
        self.near_by_mines:int = 0
        self.is_mine:bool = False
        self.is_clicked:bool = True
        self.flaged:bool = False
        self.cant_be_mine = False
        self.hitbox = pygame.rect.Rect(self.pos[0],self.pos[1],self.size,self.size)
        

    def draw(self):
        offset = 0
        if self.flaged:
            offset = 7
        elif self.is_mine:
            offset = 8
        else:
            offset = self.near_by_mines - 1
        image = pygame.transform.scale(self.tile_images, (self.size*13,self.size))
        if not self.is_clicked:
            if self.even_odd == 0:
                self.screen.blit(image,self.pos,(9*self.size,0,self.size,self.size))
            else:
                self.screen.blit(image,self.pos,(10*self.size,0,self.size,self.size))
        else:
            if self.even_odd == 0:
                self.screen.blit(image,self.pos,(11*self.size,0,self.size,self.size))
            else:
                self.screen.blit(image,self.pos,(12*self.size,0,self.size,self.size))
            self.screen.blit(image,self.pos,(offset*self.size,0,self.size,self.size))

    def collide(self):
        return self.hitbox.collidepoint(pygame.mouse.get_pos())