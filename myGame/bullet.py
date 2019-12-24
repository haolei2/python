import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self,ai_stings,screen,ship):
        super().__init__()
        self.screen = screen

        self.rect = pygame.Rect(0,0,ai_stings.bullet_width,ai_stings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y)
        self.color = ai_stings.bullet_color
        self.speed_factor = ai_stings.bullet_speed_factor

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_buttet(self):
        pygame.draw.rect(self.screen,self.color,self.rect)