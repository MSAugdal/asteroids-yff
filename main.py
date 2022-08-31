import random
from time import sleep
import pygame
import sys

with open("score.txt", "r") as f:
    highScore = f.read()  # Read all file in case values are not on a single line
    highScore_int = [int(x) for x in highScore.split()
                     ]  # Convert strings to ints
score = 0

pygame.font.init()
myFont = pygame.font.SysFont("monospace", 35)

pygame.init()

SIZE = WIDTH, HEIGHT = 640, 460
SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Almost Asteroids")

CLOCK = pygame.time.Clock()
PLAYERSPEED = 3
ENEMYSPEED = 2
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PLAYER = pygame.image.load("images/square.png")
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
    text = "Game Over"
    label = myFont.render(text, 1, WHITE)
    SCREEN.blit(label, (350, 350))

    end_score = "Score:" + str(score)
    label_2 = myFont.render(end_score, 1, WHITE)
    SCREEN.blit(label_2, (350, 250))

    with open("score.txt", "w") as f:
        for content in highScore_int:
            if content < score:
                f.write(score)
                hs = "You got the highscore. well done!"
                label_3 = myFont.render(hs, 1, WHITE)
                # Or any other position you want!
                SCREEN.blit(label_3, (350, 150))
                pygame.display.update()

            else:
                hs = "The highscore is: ", content
                label_3 = myFont.render(hs, 1, WHITE)
                # Or any other position you want!
                SCREEN.blit(label_3, (350, 150))
                pygame.display.update()

    sleep(10)
    sys.exit()


def drawGame(score):
    p = Player(PLAYERRECT, PLAYERSPEED)
    e = Enemy()

    while True:
        CLOCK.tick(60)

        score += 1

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
                pygame.quit()
                sys.exit()

        pygame.display.update()


drawGame(score)
