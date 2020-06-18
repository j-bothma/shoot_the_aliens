import pygame
from pygame import mixer
from random import randrange
import math

# Initializer game
pygame.init()

# Screen
screen = pygame.display.set_mode((800, 600))

# Background and sound
background = pygame.image.load("background.jpg")
mixer.music.load("405220__shortiefoeva2__playground-runaround.mp3")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Shoot those damn Aliens")
icon = pygame.image.load("jet.png")
pygame.display.set_icon(icon)

# Player
player_image = pygame.image.load("jet64.png")
player_x = 370
player_y = 450
player_change_x = 0
player_change_y = 0

# Enemy
enemy_image = []
enemy_x = []
enemy_y = []
enemy_change_x = []
enemy_change_y = []

for i in range(6):
    enemy_image.append(pygame.image.load("spaceship.png"))
    enemy_x.append(randrange(0, 736))
    enemy_y.append(randrange(50, 100))
    enemy_change_x.append(3)
    enemy_change_y.append(40)

# Bullet
bullet_state = "ready"
bullet_image = pygame.image.load("bomb.png")
bullet_x = 0
bullet_y = 480
bullet_change_x = 0
bullet_change_y = -10

# Score
score = 0
font = pygame.font.Font("freesansbold.ttf", 25)
score_x = 10
score_y = 10

# Game Over
over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    display_score = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(display_score, (x, y))


def game_over(x, y):
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (x, y))


# Display player
def player(x, y):
    screen.blit(player_image, (x, y))


# Display enemy
def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))


# Display bullet
def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x + 16, y - 50))


# Detect collision between enemy and bullet
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    if distance < 35:
        return True


# Loop to keep window open
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # Mapping keys to actions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_change_x = -5
            if event.key == pygame.K_RIGHT:
                player_change_x = 5
            if event.key == pygame.K_SPACE and bullet_state is "ready":
                bullet_x = player_x
                bullet(bullet_x, bullet_y)
                bullet_sound = mixer.Sound("277218__thedweebman__8-bit-laser.wav")
                bullet_sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_change_x = 0

    # Player movement and limits
    player_x += player_change_x
    if player_x < 0 or player_x > 736:
        player_change_x = 0
    player(player_x, player_y)

    # Enemy movement and limits
    for x in range(6):

        # Game Over
        if enemy_y[x] > 440:
            for j in range(6):
                enemy_y[j] = 2000
            game_over(200, 250)
            break

        enemy_x[x] += enemy_change_x[x]
        if enemy_x[x] <= 0:
            enemy_change_x[x] = 3
            enemy_y[x] += enemy_change_y[x]
        elif enemy_x[x] >= 736:
            enemy_change_x[x] = -3
            enemy_y[x] += enemy_change_y[x]
        enemy(enemy_x[x], enemy_y[x], x)

        # Collision
        collision = is_collision(enemy_x[x], enemy_y[x], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound("448226__inspectorj__explosion-8-bit-01.wav")
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score += 1
            enemy_x[x] = randrange(0, 736)
            enemy_y[x] = randrange(50, 100)

    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    # Bullet movement and limits
    if bullet_state is "fire":
        bullet(bullet_x, bullet_y)
        bullet_y += bullet_change_y

    show_score(score_x, score_y)
    pygame.display.update()
