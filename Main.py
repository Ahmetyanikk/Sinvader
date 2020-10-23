import pygame
import random
import math
from pygame import  mixer
pygame.init()


screen=pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invaders")
logo=pygame.image.load('logo.png')
Background= pygame.image.load('Background.png')
mixer.music.load('backgroundMusic.mpeg')
mixer.music.play(-1)
pygame.display.set_icon(logo)
WHITE = (255,255,255)
BLACK = (0,0,0)


#Oyuncu
playerImg= pygame.image.load('player.png')
playerX=400
playerY=480
def Player(x,y):
    screen.blit(playerImg,(x,y))


#Düşman
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemy_number=5
for i in range(enemy_number):
     enemyImg.append(pygame.image.load('enemy.png'))
     enemyX.append(random.randint(0,736))
     enemyY.append(random.randint(50,150))
     enemyX_change.append(1)
def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))


#Lazer
laserImg= pygame.image.load('laser.png')
laserX = 0
laserY = 480
laserStatus = "ready"
laserY_Changes = -5
def fire_laser(x,y):
    global laserStatus
    laserStatus = "fire"
    screen.blit(laserImg, (x+24, y+32))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


#Skor
score_Value=0
font = pygame.font.Font('freesansbold.ttf', 32)

scoreX = 10
scoreY = 10
def show_score(x, y):
    score = font.render("Score : " + str(score_Value), True, (WHITE))
    screen.blit(score, (x, y))


#Game Over Yazısı
over_font = pygame.font.Font('freesansbold.ttf', 64)
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


#Döngü
carryOn = True
while carryOn:
    screen.fill(BLACK)
    screen.blit(Background, (0, 0))
    Player(playerX, playerY)


     #Tuşlar
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn =False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX-=20
            if event.key == pygame.K_RIGHT:
                playerX +=20
            if event.key == pygame.K_SPACE:
                laserSound=mixer.Sound('laser.mpeg')
                laserSound.play()
                laserX=playerX
                fire_laser(laserX, laserY)



    if playerX<=0:
        playerX=0
    if playerX>=736:
        playerX=736

    for i in range(enemy_number):
        if enemyY[i] > 440:
            for j in range(enemy_number):
                enemyY[j] = 2000
            game_over_text()
            break


        enemy(enemyX[i], enemyY[i],i)
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i]=1
            enemyY[i]+=20
        if enemyX[i] >= 736:
            enemyX_change[i]=-1
            enemyY[i] += 20
        collision = isCollision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            laserSound = mixer.Sound('invaderkilled.mpeg')
            laserSound.play()
            laserStatus = 'ready'
            laserY = 480
            score_Value += 10
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

    if laserY <= 0:
        laserY = 480
        laserStatus = "ready"
    if laserStatus == "fire":
        fire_laser(laserX, laserY)
        laserY += laserY_Changes
    show_score(scoreX,scoreY)



    pygame.display.update()
