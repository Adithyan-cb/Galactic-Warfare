import pygame
import math
import random
import sys
import playerShip
import asteroids
import json
import os

#---SETUP----
pygame.init()
clock = pygame.time.Clock()
WIDTH = 800
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("space shooter")

#----MAIN GAME BACKGROUND AND SOUND----
image = pygame.image.load("assets/background/space-bg.png").convert()
space = pygame.transform.scale(image,(800,300))
bg_height = space.get_height()
scroll = 0
panel = math.ceil(HEIGHT / bg_height ) + 3
ingame_sound = pygame.mixer.Sound("audio/ingame.mp3")

#---GAME INTRO BACKGROUND AND SOUND---
intro_bg = pygame.image.load("assets/background/intro-bg.png").convert()
intro_sound = pygame.mixer.Sound("audio/bg-music.mp3")

#----GAME OVER BACKGROUND AND SOUND----
gameover_bg = pygame.image.load("assets/background/gameover-bg.png").convert()
gameover_sound = pygame.mixer.Sound("audio/gameover-sound.mp3")

# ------SCORE TRACKING AND SAVING----------
score_data = {"score":0}

if not os.path.exists("score.txt"):
    with open("score.txt","w") as score_file:
        json.dump(score_data,score_file)
    
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
big_asteroids = [100,150,200,250,300,350,400]
timer = pygame.USEREVENT + 1
pygame.time.set_timer(timer,1500)

#---STATE ACIVATORS---
GAME_ACTIVE = False
INTRO_ACTIVE = True
GAME_OVER = False

#----GAME LOOP----
while True:
    # ---QUITING AND SAING GAME SCORE---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if current_score >=  high_score:
                with open("score.txt","w") as score_file:
                    json.dump(score_data,score_file)
            pygame.quit()
            sys.exit()

        #---GAME RESTART---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                pygame.mixer.Sound.stop(intro_sound)
                INTRO_ACTIVE = False
                GAME_ACTIVE = True
        
        #---SPAWNING ASTEROIDS---
        if GAME_ACTIVE:
            if event.type == timer:
                for i in range(5):
                    asteroid_group.add(asteroids.Astroids(random.choice(meteros)))

                for scores in big_asteroids:
                    if current_score == scores:
                        asteroid_group.add(asteroids.Astroids("bigAsteroid"))
            
            if event.type == score_timer:
                current_score += 1
                
        #---WHEN THE GAME OVER---
        if GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    gameover_sound.stop()
                    if current_score > high_score:
                        with open("score.txt","w") as score_file:
                            json.dump(score_data,score_file)
                    GAME_ACTIVE = True
                    GAME_OVER = False
                    current_score = 0

    #----GAME INTRO-----
    if INTRO_ACTIVE:
        intro_sound.set_volume(0.5)
        intro_sound.play()
        screen.blit(intro_bg,(0,0))
        
    #---MAIN GAME------
    if GAME_ACTIVE:
        ingame_sound.set_volume(0.3)
        ingame_sound.play()
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
        ingame_sound.stop()
        gameover_sound.play()
        screen.blit(gameover_bg,(0,0))
        if current_score < high_score:
            score_render(high_score)
        else:
           high_score = current_score
           score_render(high_score)
    
    #---FPS---
    clock.tick(60)
    pygame.display.update() 
