import pygame
import math
import random
import sys
import playerShip
import asteroids
import json
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

#
intro_bg = pygame.image.load("assets/background/intro-bg.png").convert()
intro_sound = pygame.mixer.Sound("audio/bg-music.mp3")

#----GAME OVER BACKGROUND----
gameover_bg = pygame.image.load("assets/background/gameover-bg.png").convert()
gameover_sound = pygame.mixer.Sound("audio/gameover-sound.mp3")

# ------SCORE----------
score_data = {"score":0}
with open("score.txt") as score_file:
    high = json.load(score_file)

high_score = high["score"]
score_font = pygame.font.Font("assets/background/font2.ttf",20)
current_score = 0
def score(time):
    score_data["score"] = time
    txt_surf = score_font.render("score: ",False,"White")
    txt_rect = txt_surf.get_rect(center = (50,10))
    score_surf = score_font.render(f"{time}",False,'White')
    score_rect = score_surf.get_rect(center = (97,10))
    screen.blit(score_surf,score_rect)
    screen.blit(txt_surf,txt_rect)

def score_render(score):
    highscore_surf = score_font.render(f'High score: {score} ',False,"White")
    highscore_rect = highscore_surf.get_rect(center = (400,55))
    screen.blit(highscore_surf,highscore_rect)


score_timer = pygame.USEREVENT + 2
pygame.time.set_timer(score_timer,1500)

# -------COLLISION FUNCTION-----
def collision():
    if pygame.sprite.spritecollide(playerShip_group.sprite,asteroid_group,False):
            asteroid_group.empty()
            return True
    else:
        return False

#----PLAYERSHIP----
ship = playerShip.PlayerShip()
playerShip_group = pygame.sprite.GroupSingle()
playerShip_group.add(ship)

#----ASTEROIDS----
asteroid_group = pygame.sprite.Group()
meteros = ['meteor','flaming','meteor','meteor','flaming','meteor','meteor']
timer = pygame.USEREVENT + 1
pygame.time.set_timer(timer,1500)

#---STATE ACIVATORS---
GAME_ACTIVE = False
INTRO_ACTIVE = True
GAME_OVER = False

#----GAME LOOP----
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if current_score >=  high_score:
                with open("score.txt","w") as score_file:
                    json.dump(score_data,score_file)
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

            if event.type == score_timer:
                current_score += 1

        if GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    if current_score > high_score:
                        with open("score.txt","w") as score_file:
                            json.dump(score_data,score_file)
                    GAME_ACTIVE = True
                    GAME_OVER = False
                    current_score = 0

    #----GAME INTRO-----
    if INTRO_ACTIVE:
        intro_sound.play()
        screen.blit(intro_bg,(0,0))
        
    #---MAIN GAME------
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

        #----SCORE----
        score(current_score)

        #----COLLISION----
        collision_checker = collision()
        if collision_checker:
            GAME_ACTIVE = False
            GAME_OVER = True

    #----GAME OVER----
    if GAME_OVER:
        #gameover_sound.play()
        screen.blit(gameover_bg,(0,0))
        if current_score < high_score:
            score_render(high_score)
        else:
           high_score = current_score
           score_render(high_score)

    clock.tick(60)
    pygame.display.update() 