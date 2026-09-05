import pygame
import numpy as np
from pygame.locals import *
from pygame import mixer

pygame.init()

mixer.music.load("background.wav")
mixer.music.play(-1)

Screen                  = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invador")

WHITE                   = (255,255,255)
RED                     = (255,0,0)
GREEN                   = (0,255,0)
GREY                    = (128,128,128)

isLeft                  = False
isRight                 = False
isUp                    = False
isDown                  = False
isShoot                 = False

spaceship               = pygame.image.load("MC.png")
spaceship_position_x    = 368
spaceship_position_y    = 480

alien                   = []
alien_position_x        = []
alien_position_y        = []
alien_position_change_x = []
alien_position_change_y = []
num_of_enemies = 0
for i in range(10):
    alien.append(pygame.image.load("alien.png"))
    alien_position_x.append(np.random.randint(0,736))
    alien_position_y.append(np.random.randint(0,200))
    alien_position_change_x.append(0.5)
    alien_position_change_y.append(10)

bullet                  = pygame.image.load("bullet.png")
bullet_x                = spaceship_position_x
bullet_y                = spaceship_position_y
bullet_x_change         = 0
bullet_y_change         = 2

score_value             = 0
font                    = pygame.font.Font("freesansbold.ttf",16)
text_position_x         = 10
text_position_y         = 10

def display_score(x,y):
    score = font.render("SCORE : " + str(score_value),True,WHITE)
    Screen.blit(score,(x,y))

def player(x,y):
    Screen.blit(spaceship,(x,y))

def enemy(x,y,i):
    Screen.blit(alien[i],(x,y))

def fire_bullet(x,y):
    global isShoot
    isShoot = True
    Screen.blit(bullet,(x+24,y-10))

def player_Events():
    global isLeft                  
    global isRight               
    global isUp                    
    global isDown
    global isShoot                 
    if event.type == KEYDOWN:
        if event.key in(K_UP,K_w):
            isUp = True
        elif event.key in (K_DOWN,K_s):
            isDown = True
        elif event.key in (K_LEFT,K_a):
            isLeft = True
        elif event.key in (K_RIGHT,K_d):
            isRight = True
    
    elif event.type == KEYUP:
        if event.key in(K_UP,K_w):
            isUp = False
        elif event.key in (K_DOWN,K_s):
            isDown = False
        elif event.key in (K_LEFT,K_a):
            isLeft = False
        elif event.key in (K_RIGHT,K_d):
            isRight = False

def execute_player_movement():
    global isLeft                
    global isRight                
    global isUp                    
    global isDown
    global isShoot
    global spaceship_position_x
    global spaceship_position_y
    global bullet_y
    global bullet_x
    
    if isLeft == True and isUp == True :
        spaceship_position_x -= 0.5 
        spaceship_position_y -= 0.5
        if spaceship_position_y < 0:
            spaceship_position_y = 0
        elif spaceship_position_x < 0:
            spaceship_position_x = 0
    elif isLeft == True and isDown == True :
        spaceship_position_x -= 0.5 
        spaceship_position_y += 0.5
    elif isRight == True and isDown == True :
        spaceship_position_x += 0.5 
        spaceship_position_y += 0.5
    elif isRight == True and isUp == True :
        spaceship_position_x += 0.5 
        spaceship_position_y -= 0.5      
    
    elif isLeft == True :
        spaceship_position_x -= 0.5
        if spaceship_position_x < 0:
           spaceship_position_x = 0
    elif isRight == True :
        spaceship_position_x += 0.5
        if spaceship_position_x > (800-64):
            spaceship_position_x = (800-64)
    elif isUp == True :
        spaceship_position_y -= 0.5
        if spaceship_position_y < 0 :
            spaceship_position_y = 0
    elif isDown == True :
        spaceship_position_y += 0.5
        if spaceship_position_y > (600-64):
            spaceship_position_y = (600-64)

def enemy_movements():
    global alien_position_x
    global alien_position_y
    global alien_position_change_x
    global alien_position_change_y

    alien_position_x[i] += alien_position_change_x[i]
    if alien_position_x[i] <= 0 :
        alien_position_y[i] += alien_position_change_y[i] 
        alien_position_change_x[i] = 0.5
    elif alien_position_x[i] >= 736 :
        alien_position_y[i] += alien_position_change_y[i] 
        alien_position_change_x[i] = -0.5

def bullet_Events():
    global isShoot
    global spaceship_position_x
    global spaceship_position_y
    global bullet_x
    global bullet_y
    if event.type == KEYDOWN:
        if isShoot == False:
            if event.key == K_SPACE:
                bullet_x = spaceship_position_x
                bullet_y = spaceship_position_y
                fire_bullet(bullet_x,bullet_y)        

def bullet_movements():
    global isShoot
    global bullet_x
    global bullet_y
    if bullet_y <= 0 :
        isShoot = False 
        bullet_y = 480

    if isShoot == True:
        fire_bullet(bullet_x,bullet_y)
        bullet_y -= bullet_y_change

def isCollision(x_enemy,y_enemy,x_bullet,y_bullet):
    distance = np.sqrt(((x_enemy-x_bullet)**2) + ((y_enemy-y_bullet)**2))
    if distance <= 25:
        return True
    else:
        False

def level():
    global score_value
    global num_of_enemies
    if 0 <= score_value < 5 :
        num_of_enemies = 5
    elif 5 <= score_value <20:
        num_of_enemies = 4
    elif 20<= score_value <50 :
        num_of_enemies = 6    

def isGameOver(player_x,player_y,enemy_x,enemy_y):
    distance = np.sqrt((player_x - enemy_x)**2 + (player_y - enemy_y)**2)
    if distance < 20 :
        return True
    else :
        return False


run = True
while run:
    Screen.fill((30,30,30))

    player(spaceship_position_x,spaceship_position_y)
    for i in range(num_of_enemies):
        enemy(alien_position_x[i],alien_position_y[i],i)
        enemy_movements()
        collison = isCollision(alien_position_x[i],alien_position_y[i],bullet_x,bullet_y)
        if collison:
            boom = mixer.Sound("explosion.wav")
            boom.play()
            isShoot = False
            bullet_y = 480
            score_value += 1
            alien_position_x[i] = np.random.randint(0,736)
            alien_position_y[i] = np.random.randint(0,200)
        for k in range(num_of_enemies):
            game_over = isGameOver(spaceship_position_x,spaceship_position_y,alien_position_x[i],alien_position_y[i])
            if game_over:
                for j in range(num_of_enemies):
                    alien_position_y[j] = 1000
    
    for event in pygame.event.get():
        if event.type == QUIT :
            run = False

        player_Events()
        bullet_Events()
    
    execute_player_movement()
    
    bullet_movements()
    level()
    display_score(text_position_x,text_position_y)
    pygame.display.update()