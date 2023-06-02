import pygame

# Initialisierung von Pygame
pygame.init()

# Bildschirmgröße
screen_width = 800
screen_height = 600

# Farben definieren
black = (0, 0, 0)
white = (255, 255, 255)

# Spielfigur laden
player_image = pygame.image.load("bbc.png.png")
player_width = 64
player_height = 64

# Startposition der Spielfigur
player_x = (screen_width - player_width) // 2
player_y = screen_height - player_height - 10

# Erstellen des Bildschirms
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mein Spiel")

image = pygame.image.load("bbc.png.png")

# Hauptschleife
running = True
while running:
    # Ereignisse überprüfen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Tasteneingaben überprüfen
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= 5
    if keys[pygame.K_RIGHT]:
        player_x += 5
    if keys[pygame.K_UP]:
        player_y -= 5
    if keys[pygame.K_DOWN]:
        player_y += 5

    # Bildschirm löschen
    screen.fill(white)

    # Spielfigur anzeigen
    screen.blit(player_image, (player_x, player_y))

    # Bildschirm aktualisieren
    pygame.display.flip()

# Pygame beenden
pygame.quit()
