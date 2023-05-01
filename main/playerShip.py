import pygame
# player ship class

class PlayerShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        width = 50
        height = 50
        img_1 = pygame.image.load("assets/ship/ship-1.png").convert_alpha()
        ship_1 = pygame.transform.scale(img_1,(width,height))

        img_2 = pygame.image.load("assets/ship/ship-2.png").convert_alpha()
        ship_2 = pygame.transform.scale(img_2,(width,height))

        img_3 = pygame.image.load("assets/ship/ship-3.png").convert_alpha()
        ship_3 = pygame.transform.scale(img_3,(width,height))

        img_4 = pygame.image.load("assets/ship/ship-4.png").convert_alpha()
        ship_4 = pygame.transform.scale(img_4,(width,height))

        img_5 = pygame.image.load("assets/ship/ship-5.png").convert_alpha()
        ship_5 = pygame.transform.scale(img_5,(width,height))

        self.ship_move = [ship_1,ship_2,ship_3,ship_4,ship_5]
        self.ship_index = 0
        self.image = self.ship_move[self.ship_index]
        self.rect = self.image.get_rect(midbottom = (400,330))

    def playerInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5

        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        if self.rect.x <= 0:
            self.rect.x = 0

        if self.rect.x >= 764:
            self.rect.x = 764

    def animation(self):
        self.ship_index += 0.1
        if self.ship_index >= len(self.ship_move):
            self.ship_index = 0
        self.image = self.ship_move[int(self.ship_index)]
    #def create_bullet(self):
     #   self.xpos = self.rect.x
      #  self.ypos = self.rect.y
       # return Bullet(self.xpos,self.ypos)
    
    def update(self):
        self.playerInput()
        self.animation()

class Bullet(pygame.sprite.Sprite):
    def __init__(self,xpos,ypos):
        super().__init__()
        width = 30
        height = 30
        img_1 = pygame.image.load("assets/laser/laser-1.png")
        laser_1 = pygame.transform.scale(img_1,(width,height))

        img_2 = pygame.image.load("assets/laser/laser-2.png")
        laser_2 = pygame.transform.scale(img_2,(width,height))

        self.laser_move = [laser_1,laser_2]
        self.laser_index = 0
        self.image = self.laser_move[self.laser_index]
        self.rect = self.image.get_rect(midbottom = ((xpos + 20),ypos))
    
    def animation(self):
        self.laser_index += 0.1
        if self.laser_index >= len(self.laser_move):
            self.laser_index = 0
        self.image = self.laser_move[int(self.laser_index)]
    
    def update(self):
        self.rect.y -= 5
        self.animation()