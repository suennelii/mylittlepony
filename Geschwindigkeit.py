import pygame

# Initialisiere Pygame
pygame.init()

# Definiere die Bildschirmgröße
screen_width = 1000
screen_height = 1000

# Erstelle den Bildschirm
screen = pygame.display.set_mode((screen_width, screen_height))

# Setze den Hintergrund auf weiß
screen.fill((0,0,0))

# Zeichne eine waagerechte Linie
line_color = (255, 255, 255)
line_start = (0, 750)
line_end = (screen_width - 1, 750)
line_width = 10
pygame.draw.line(screen, line_color, line_start, line_end, line_width)

# Aktualisiere den Bildschirm
pygame.display.flip()

# Warte, bis das Fenster geschlossen wird
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Beende Pygame
pygame.quit()
