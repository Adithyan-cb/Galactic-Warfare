import pygame
import random
#---ASTEROID CLASS----
class Astroids(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == "flaming":
            self.meteor = pygame.image.load("assets/asteroids/flaming_meteor.png").convert_alpha()
            self.speed = 7.5
        elif type == "bigAsteroid":
            image = pygame.image.load("assets/asteroids/meteor.png").convert_alpha()
            self.meteor = pygame.transform.scale(image,(200,200))
            self.speed = 6.5
        else:
            self.meteor = pygame.image.load("assets/asteroids/meteor.png").convert_alpha()
            self.speed = 6.5
        
        self.image = self.meteor
        self.rect = self.image.get_rect(midtop = (random.randint(0,765),-20))

    def destory(self):
        if self.rect.y > 430:
            self.kill()
    
    def update(self):
        self.rect.y += self.speed
        self.destory()
