import pygame
import random

# Initialisierung
pygame.init()

# Bildschirmgröße
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Farben
SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
GRASS_GREEN = (34, 139, 34)

# Himmel und Wiese Größenverhältnis
sky_height = height * 0.7
grass_height = height * 0.3

# Wolken
clouds = []
for _ in range(6):
    cloud_x = random.randint(0, width)
    cloud_y = random.randint(0, int(sky_height / 2))
    cloud_speed = random.randint(1, 3)
    clouds.append((cloud_x, cloud_y, cloud_speed))

# Spielfigur laden
player_image = pygame.image.load("bbc.png.png")
player_width = 100
player_height = 100

# Partikel-Effekt
particles = []

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(1, 3)
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.vel_x = random.uniform(-1, 1)
        self.vel_y = random.uniform(-1, 1)
        self.alpha = 255
        self.duration = random.randint(30, 60)

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.alpha -= 255 / self.duration
        if self.alpha <= 0:
            particles.remove(self)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

# Spielerklasse
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_image, (player_width, player_height))
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)
        self.y_velocity = 0
        self.jump_power = -10

    def update(self):
        self.y_velocity += 1
        self.rect.y += self.y_velocity

        if self.rect.bottom > height:
            self.rect.bottom = height
            self.y_velocity = 0

    def jump(self):
        self.y_velocity = self.jump_power
        particles.extend([Particle(self.rect.centerx, self.rect.centery) for _ in range(10)])

# Spieler erstellen
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Hauptprogramm
running = True
clock = pygame.time.Clock()
while running:
    # Ereignisse überprüfen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player.rect.x += 5
    if keys[pygame.K_UP]:
        player.rect.y -= 5
    if keys[pygame.K_DOWN]:
        player.rect.y += 5

    # Hintergrund zeichnen
    screen.fill(SKY_BLUE)  # Himmel
    pygame.draw.rect(screen, GRASS_GREEN, (0, height - grass_height, width, grass_height))  # Wiese

    # Wolken bewegen
    for i in range(len(clouds)):
        cloud_x, cloud_y, cloud_speed = clouds[i]
        cloud_x -= cloud_speed
        if cloud_x < -200:
            cloud_x = width
            cloud_y = random.randint(0, int(sky_height / 2))
            cloud_speed = random.randint(1, 3)
        clouds[i] = (cloud_x, cloud_y, cloud_speed)

        # Wolken zeichnen
        pygame.draw.ellipse(screen, WHITE, (cloud_x, cloud_y, 100, 50))
        pygame.draw.ellipse(screen, WHITE, (cloud_x + 25, cloud_y - 25, 100, 50))
        pygame.draw.ellipse(screen, WHITE, (cloud_x + 50, cloud_y, 100, 50))
        pygame.draw.ellipse(screen, WHITE, (cloud_x + 25, cloud_y + 25, 100, 50))

    # Partikel-Effekte aktualisieren und zeichnen
    for particle in particles:
        particle.update()
        particle.draw(screen)

    all_sprites.update()
    all_sprites.draw(screen)

    # Aktualisiere den Bildschirm
    pygame.display.flip()
    clock.tick(60)  # Begrenze die Bildrate auf 60 FPS

# Pygame beenden
pygame.quit()
