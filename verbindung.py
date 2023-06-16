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

# Himmel Größe
sky_height = height

# Wolken
clouds = []
for _ in range(6):
    cloud_x = random.randint(0, width)
    cloud_y = random.randint(0, int(sky_height / 2))
    cloud_speed = random.randint(1, 3)
    clouds.append((cloud_x, cloud_y, cloud_speed))

# Spielfigur laden
player_image = pygame.image.load("bbc.png.png")
player_width = 120
player_height = 120

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
        self.rect.center = (width / 2, height - player_height // 2)  # Spieler startet am unteren Bildschirmrand
        self.y_velocity = 0
        self.jump_power = -12

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

# Sterne-Klasse
class Star(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((player_width, player_height))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Setze zufällige Farbe für den Stern
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        pygame.draw.ellipse(self.image, self.color, (0, 0, player_width, player_height))

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.rect.x = width
            self.rect.y = random.randint(0, sky_height)

# Sterne erstellen
stars = pygame.sprite.Group()
for _ in range(10):
    star = Star(width + random.randint(100, 400), random.randint(0, sky_height))
    stars.add(star)
    all_sprites.add(star)

# Hauptprogramm
running = True
game_over = False
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_over and event.key == pygame.K_SPACE:
                player.jump()

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT]:
            player.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            player.rect.x += 5
        if keys[pygame.K_UP]:
            player.rect.y -= 5
        if keys[pygame.K_DOWN]:
            player.rect.y += 5

    if not game_over:
        screen.fill(SKY_BLUE)

        for i in range(len(clouds)):
            cloud_x, cloud_y, cloud_speed = clouds[i]
            cloud_x -= cloud_speed
            if cloud_x < -200:
                cloud_x = width
                cloud_y = random.randint(0, int(sky_height / 2))
                cloud_speed = random.randint(1, 3)
            clouds[i] = (cloud_x, cloud_y, cloud_speed)

            pygame.draw.ellipse(screen, WHITE, (cloud_x, cloud_y, 100, 50))
            pygame.draw.ellipse(screen, WHITE, (cloud_x + 25, cloud_y - 25, 100, 50))
            pygame.draw.ellipse(screen, WHITE, (cloud_x + 50, cloud_y, 100, 50))
            pygame.draw.ellipse(screen, WHITE, (cloud_x + 25, cloud_y + 25, 100, 50))

        for particle in particles:
            particle.update()
            particle.draw(screen)

        if pygame.sprite.spritecollide(player, obstacles, False):
            game_over = True

        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    if game_over:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        text = font.render("Game Over!", True, WHITE)
        text_rect = text.get_rect(center=(width / 2, height / 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)

pygame.quit()
