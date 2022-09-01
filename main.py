import random
import pygame
import sys

pygame.font.init()
myFont = pygame.font.SysFont("monospace", 35)

pygame.init()

# setter alle variabler som skal brukes i spillet
SIZE = WIDTH, HEIGHT = 640, 460

SCREEN = pygame.display.set_mode(SIZE)
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


# lager en klasse for spilleren
class Player():
    def __init__(self, PLAYERRECT, PLAYERSPEED):
        self.rect = PLAYERRECT
        self.speed = PLAYERSPEED

    # lager en funksjon som gjør at spilleren kan bevege seg
    def movement(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] or key[pygame.K_w]:
            if PLAYERRECT.top > 0:
                self.rect.move_ip(0, -self.speed)

        if key[pygame.K_DOWN] or key[pygame.K_s]:
            if PLAYERRECT.bottom < HEIGHT:
                self.rect.move_ip(0, +self.speed)

        if key[pygame.K_LEFT] or key[pygame.K_a]:
            self.rect.move_ip(-self.speed, 0)

        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.rect.move_ip(+self.speed, 0)

        # aktiverer screen wrap for spilleren
        if PLAYERRECT.left > WIDTH:
            PLAYERRECT.centerx = (0)
        if PLAYERRECT.right < 0:
            PLAYERRECT.centerx = (WIDTH)


# lager en klasse for fiendene
class Enemy():
    def __init__(self):
        ENEMY = pygame.image.load("images/enemy.png")

    # lager en funksjon som bestemmer hvor fiendene skal starte og legger dem til i en liste over fiender
    def spawn(self):
        pos_x = random.randint(0, WIDTH)
        pos_y = random.randint(10, HEIGHT)
        ENEMYRECT = ENEMY.get_rect(center=(pos_x, -pos_y))
        SCREEN.blit(ENEMY, ENEMYRECT)
        list_of_enemies.append(ENEMYRECT)


# lager en funksjon som "tegner" spillet og håndterer mestepartn av logikken
def drawGame():
    score = 0
    p = Player(PLAYERRECT, PLAYERSPEED)
    PLAYERRECT.center = (WIDTH/2, HEIGHT/2)
    e = Enemy()
    while True:
        CLOCK.tick(60)
        score += 1

        # lukker spillet om spilleren trykker på krysset
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        p.movement()

        # gjør bakgrunnen svart og legger til spilleren på skjermen
        SCREEN.fill(BLACK)
        SCREEN.blit(PLAYER, PLAYERRECT)

        # legger til fiender på skjermen om det er mindre enn 10 fiender
        if len(list_of_enemies) < 10:
            e.spawn()

        # flytter finendene nedover skjermen
        for rect in list_of_enemies:
            SCREEN.blit(ENEMY, rect)
            rect.move_ip(0, +ENEMYSPEED)

            # fjerner fiender som har gått ut av skjermen
            if rect.top > HEIGHT:
                list_of_enemies.remove(rect)

            # fjerner fiende om den kolliderer med en annen fiende
            for enemy in list_of_enemies:
                if rect != enemy:
                    if rect.colliderect(enemy):
                        list_of_enemies.remove(rect)

            # sjekker om spilleren kolliderer med en fiende
            # hvis dette skjer, vises en boks med teksten "Game Over" og scoren vises under
            # spillet startes på nytt om spilleren trykker på spacebar
            if rect.colliderect(PLAYERRECT):
                list_of_enemies.clear()

                SCREEN.fill(BLACK)
                label = myFont.render("Game Over", 1, WHITE)
                SCREEN.blit(label, (WIDTH/2 - label.get_width() /
                            2, HEIGHT/2 - label.get_height()/2))

                label2 = myFont.render("score: "+str(score), 1, WHITE)
                SCREEN.blit(label2, (WIDTH/2 - label2.get_width()/2,
                            HEIGHT/2 - label2.get_height()/2 + 50))

                label3 = myFont.render("Press SPACE to restart", 1, WHITE)
                SCREEN.blit(label3, (WIDTH/2 - label3.get_width()/2,
                            HEIGHT/2 - label3.get_height()/2 + 100))

                pygame.display.update()

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                drawGame()

        pygame.display.update()


# starter spillet
drawGame()
