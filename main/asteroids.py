import pygame
import random
#enemy ship class
class Astroids(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == "flaming":
            self.meteor = pygame.image.load("assets/asteroids/flaming_meteor.png").convert_alpha()
            self.speed = 7
        else:
            self.meteor = pygame.image.load("assets/asteroids/meteor.png").convert_alpha()
            self.speed = 5
        
        self.image = self.meteor
        self.rect = self.image.get_rect(midtop = (random.randint(0,765),-10))

    def destory(self):
        if self.rect.y > 430:
            self.kill()
    
    def update(self):
        self.rect.y += self.speed
        self.destory()
