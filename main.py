import random
from time import sleep
import pygame
import sys


pygame.font.init()
myFont = pygame.font.SysFont("monospace", 35)

pygame.init()

SIZE = WIDTH, HEIGHT = 640, 460
SCREEN = pygame.display.set_mode(SIZE)
SCREEN_CENTER = (WIDTH / 3, HEIGHT / 2)
pygame.display.set_caption("Almost Asteroids")

CLOCK = pygame.time.Clock()
PLAYERSPEED = 3
ENEMYSPEED = 2
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PLAYER = pygame.image.load("images/square.png")
PLAYER = pygame.transform.smoothscale(PLAYER, (30, 30))
PLAYERRECT = PLAYER.get_rect(center=(WIDTH/2, HEIGHT/2))

ENEMY = pygame.image.load("images/enemy.png")
ENEMYRECT = ENEMY.get_rect()
list_of_enemies = []


class Player():
    def __init__(self, PLAYERRECT, PLAYERSPEED):
        self.rect = PLAYERRECT
        self.speed = PLAYERSPEED

    def movement(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] or key[pygame.K_w]:
            self.rect.move_ip(0, -self.speed)
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            self.rect.move_ip(0, +self.speed)
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            self.rect.move_ip(-self.speed, 0)
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.rect.move_ip(+self.speed, 0)


class Enemy():
    def __init__(self):
        ENEMY = pygame.image.load("images/enemy.png")

    def spawn(self):
        pos_x = random.randint(0, WIDTH)
        pos_y = random.randint(10, HEIGHT)
        ENEMYRECT = ENEMY.get_rect(center=(pos_x, -pos_y))
        SCREEN.blit(ENEMY, ENEMYRECT)
        list_of_enemies.append(ENEMYRECT)


def game_over():
    SCREEN.fill(BLACK)
    for enemy in list_of_enemies:
        list_of_enemies.remove(enemy)
    text = "Game Over"
    label = myFont.render(text, 1, WHITE)
    SCREEN.blit(label, SCREEN_CENTER)
    pygame.display.update()
    pygame.time.delay(1500)


def drawGame():
    p = Player(PLAYERRECT, PLAYERSPEED)
    e = Enemy()

    while True:
        CLOCK.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        p.movement()

        SCREEN.fill(BLACK)
        SCREEN.blit(PLAYER, PLAYERRECT)

        if len(list_of_enemies) < 10:
            e.spawn()

        for rect in list_of_enemies:
            SCREEN.blit(ENEMY, rect)
            rect.move_ip(0, +ENEMYSPEED)

            if rect.top > HEIGHT:
                list_of_enemies.remove(rect)

            for enemy in list_of_enemies:
                if rect != enemy:
                    if rect.colliderect(enemy):
                        list_of_enemies.remove(rect)

            if rect.colliderect(PLAYERRECT):
                game_over()

        pygame.display.update()


drawGame()
