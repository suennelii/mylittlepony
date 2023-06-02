import pygame

pygame.init()

screen_width = 1000
screen_height = 600

# Spielfigur laden
player_image = pygame.image.load("bbc.png.png")
player_width = 100
player_height = 100

# Startposition der Spielfigur
player_x = (screen_width - player_width) // 2
player_y = screen_height - player_height - 10

# Erstellen des Bildschirms
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mein Spiel")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_image, (player_width, player_height))
        self.rect = self.image.get_rect()
        self.rect.center = (player_x, player_y)
        self.y_velocity = 0
        self.jump_power = -10

    def update(self):
        self.y_velocity += 1
        self.rect.y += self.y_velocity

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.y_velocity = 0

    def jump(self):
        self.y_velocity = self.jump_power

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Hauptschleife
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

    all_sprites.update()

    screen.fill((255, 255, 255))

    all_sprites.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
