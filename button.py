import pygame
from pygame.math import Vector2

class Button:
    def __init__(self, title:str, pos:Vector2, size:Vector2, button_color:tuple[int,int,int], text_color:tuple[int,int,int]):
        self.title:str = title
        self.pos:Vector2 = pos
        self.size:Vector2 = size
        self.button_color:tuple[int,int,int] = button_color
        self.text_color:tuple[int,int,int] = text_color
        self.rect:pygame.Rect = pygame.Rect(0,0,int(self.size.x), int(self.size.y))
        self.rect.center = (int(self.pos.x),int(self.pos.y))
        self.font = pygame.font.SysFont("Roboto", int(self.size.y))
        self.text = self.font.render(self.title, True, text_color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center


    def draw(self, screen:pygame.surface.Surface):
        pygame.draw.rect(screen,self.button_color,self.rect)
        screen.blit(self.text, self.text_rect)


    def collide(self,mouse_pos:tuple[int,int]):
        return self.rect.collidepoint(mouse_pos)

