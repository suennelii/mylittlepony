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
            show_game_over_screen()

        if self.rect.top < 0:
            self.rect.top = 0
            self.y_velocity = 0
            show_game_over_screen()

    def jump(self):
        self.y_velocity = self.jump_power
        particles.extend([Particle(self.rect.centerx, self.rect.centery) for _ in range(10)])

def show_game_over_screen():
    screen.fill(SKY_BLUE)
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, WHITE)
    text_rect = text.get_rect(center=(width / 2, height / 2))
    screen.blit(text, text_rect)

    play_button_text = font.render("Play Again", True, WHITE)
    play_button_rect = play_button_text.get_rect(center=(width / 2, height / 2 + 50))
    pygame.draw.rect(screen, WHITE, play_button_rect, border_radius=10)
    screen.blit(play_button_text, play_button_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button_rect.collidepoint(event.pos):
                    return

def show_start_screen():
    screen.fill(SKY_BLUE)
    font = pygame.font.Font(None, 36)
    title_text = font.render("My Little Jumping Pony", True, WHITE)
    title_text_rect = title_text.get_rect(center=(width / 2, height / 2 - 50))
    screen.blit(title_text, title_text_rect)

    play_button_text = font.render("Play", True, WHITE)
    play_button_rect = play_button_text.get_rect(center=(width / 2, height / 2 + 50))
    pygame.draw.rect(screen, WHITE, play_button_rect, border_radius=10)
    screen.blit(play_button_text, play_button_rect)

    pygame.display.flip()

    countdown_start_time = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button_rect.collidepoint(event.pos):
                    countdown_start_time = pygame.time.get_ticks()

        if countdown_start_time is not None:
            current_time = pygame.time.get_ticks()
            if current_time - countdown_start_time < countdown_duration:
                screen.fill(SKY_BLUE)
                countdown_seconds = (countdown_duration - (current_time - countdown_start_time)) // 1000 + 1
                countdown_text = str(countdown_seconds)
                font = pygame.font.Font(None, 100)
                text = font.render(countdown_text, True, WHITE)
                text_rect = text.get_rect(center=(width / 2, height / 2))
                screen.blit(text, text_rect)
            else:
                return

        pygame.display.flip()

# Spieler erstellen
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Countdown-Variablen
countdown_duration = 3000  # 3 Sekunden in Millisekunden

# Startbildschirm anzeigen
show_start_screen()

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
    screen.fill(SKY_BLUE)

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
