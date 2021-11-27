import pygame
import random
import math
from pygame import mixer

# intialize pygame
pygame.init()

# setting sc
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("bg.png")

mixer.music.load("bg.wav")
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("SpaceInvader by Anvin")
icon = pygame.image.load("alien.png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load("spaceship.png")
playerX = 368
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 200))
    enemyX_change.append(0.6)
    enemyY_change.append(45)

# bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.6
bullet_state = "ready"

count = 0
scorevalue = 0

font = pygame.font.Font("game_over.ttf", 70)
textX = 8
textY = 13

over_font = pygame.font.Font("game_over.ttf", 150)

playagain_font = pygame.font.Font("game_over.ttf", 50)


# highscore_font = pygame.font.Font("game_over.ttf", 70)

def show_score(x, y):
    score = font.render("Score : " + str(scorevalue), True, (255, 255, 255))
    screen.blit(score, (x, y))


# def show_highscore():
# highscore = highscore_font.render("High Score : " + hs, True, (255, 255, 255))
# sc.blit(highscore, (500, 13))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (230, 250))


def playagain_text():
    over_text = playagain_font.render(" Press 'Q' to Play Again ", True, (255, 255, 255))
    screen.blit(over_text, (293, 320))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyX - bulletX), 2) + math.pow((enemyY - bulletY), 2))
    if distance < 27:
        return True
    else:
        return False


score = 0
over = True
# game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # keystroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.9
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.9
            if event.key == pygame.K_q:
                print("enter")
                for i in range(num_of_enemies):
                    scorevalue = 0
                    over = True
                    enemyX[i] = random.randint(0, 735)
                    enemyY[i] = random.randint(50, 200)
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("bullet.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):
        if enemyY[i] > 430:
            over = False
            for j in range(num_of_enemies):
                enemyY[i] = 2000
            if count % 2 == 0:
                game_over_text()
            playagain_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.4
            enemyY[i] += enemyY_change[i]

        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            if over:
                scorevalue += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 200)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 15:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    count += 1

    player(playerX, playerY)
    show_score(textX, textY)
    # show_highscore()
    pygame.display.update()
