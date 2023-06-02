import pygame
import random
import time

# Bildschirmeinstellungen
WIDTH = 1000
HEIGHT = 1000
FPS = 30

# Farben
WHITE = (255, 255, 255)

# Initialisierung von Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gleichseitige Dreiecke")
clock = pygame.time.Clock()

class Dreieck(pygame.sprite.Sprite):
    def __init__(self, size, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size, size))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(0, 750 - size)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right <= 0:
            self.rect.x = WIDTH
            self.rect.y = random.randint(0, 750 - self.rect.height)

all_sprites = pygame.sprite.Group()
size = 50
speed = 3

# Erzeuge 5 Dreiecke
for _ in range(5):
    dreieck = Dreieck(size, speed)
    all_sprites.add(dreieck)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Aktualisiere die Geschwindigkeit alle 15 Sekunden
    if pygame.time.get_ticks() % 15000 == 0:
        speed += 3

    all_sprites.update()

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
