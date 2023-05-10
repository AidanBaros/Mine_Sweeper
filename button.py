import pygame
from pygame import Vector2

class Button:
    def __init__(self, title:str, pos:Vector2, size:Vector2, color:tuple[int,int,int]):
        self.title:str = title
        self.pos:Vector2 = pos
        self.size:Vector2 = size
        self.color:tuple[int,int,int] = color
        self.rect = pygame.Rect(int(self.pos.x),int(self.pos.y),int(self.size.x), int(self.size.y))


    def draw(self, screen:pygame.surface.Surface):
        pygame.draw.rect(screen,self.color,self.rect)


    def collide(self,mouse_pos:tuple[int,int]):
        return self.rect.collidepoint(mouse_pos)

