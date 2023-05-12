import pygame
import math
import random
import sys
import playerShip
import asteroids

# game set-up
pygame.init()
clock = pygame.time.Clock()
WIDTH = 800
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("space shooter")

# main game background
image = pygame.image.load("assets/background/space-bg.png").convert()
space = pygame.transform.scale(image,(800,300))
bg_height = space.get_height()
scroll = 0
panel = math.ceil(HEIGHT / bg_height ) + 3

# intro background
intro_bg = pygame.image.load("assets/background/intro-bg.png").convert()
intro_sound = pygame.mixer.Sound("audio/bg-music.mp3")

#game over background
gameover_bg = pygame.image.load("assets/background/gameover-bg.png").convert()

# score 
score_font = pygame.font.Font("assets/font2.ttf",20)
def score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    txt_surf = score_font.render("score: ",False,"White")
    txt_rect = txt_surf.get_rect(center = (50,10))
    score_surf = score_font.render(f"{current_time}",False,'White')
    score_rect = score_surf.get_rect(center = (97,10))
    screen.blit(score_surf,score_rect)
    screen.blit(txt_surf,txt_rect)

# collision function
def collision():
    if pygame.sprite.spritecollide(playerShip_group.sprite,asteroid_group,False):
            asteroid_group.empty()
            return True
    else:
        return False
    
start_time = 0
#player ship
ship = playerShip.PlayerShip()
playerShip_group = pygame.sprite.GroupSingle()
playerShip_group.add(ship)

# asteroids
asteroid_group = pygame.sprite.Group()
meteros = ['meteor','flaming','meteor','meteor','flaming','meteor','meteor']
timer = pygame.USEREVENT + 1
pygame.time.set_timer(timer,1500)

# game loop
GAME_ACTIVE = False
INTRO_ACTIVE = True
GAME_OVER = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                pygame.mixer.Sound.stop(intro_sound)
                INTRO_ACTIVE = False
                GAME_ACTIVE = True

        if GAME_ACTIVE:
            if event.type == timer:
                for i in range(3):
                    asteroid_group.add(asteroids.Astroids(random.choice(meteros)))
                #laser_audio.play()
        if GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    GAME_ACTIVE = True
                    GAME_OVER = False
                    start_time =  int(pygame.time.get_ticks()/1000) - start_time

    if INTRO_ACTIVE:
        #intro_sound.play()
        screen.blit(intro_bg,(0,0))

    #scrolling feature
    if GAME_ACTIVE:
        for i in range(panel):
            screen.blit(space,(0, i * bg_height + scroll - bg_height))
        scroll += 5
        if abs(scroll) > bg_height:
            scroll = 0

        playerShip_group.draw(screen)
        playerShip_group.update()

        asteroid_group.draw(screen)
        asteroid_group.update()

        #score
        score()

        #collision
        collision_checker = collision()
        if collision_checker:
            GAME_ACTIVE = False
            GAME_OVER = True

    if GAME_OVER:
        screen.blit(gameover_bg,(0,0))

    clock.tick(60)
    pygame.display.update()

# create game over interface
# create levels
# track score
# display score on game over interface 