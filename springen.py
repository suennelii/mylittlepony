import pygame
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("springen")
colour = (255, 0, 255)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.y_velocity = 0
        self.jump_power = -10

    def update(self):
        self.y_velocity += 1  # Gravitation
        self.rect.y += self.y_velocity

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.y_velocity = 0

    def jump(self):
        self.y_velocity = self.jump_power
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    all_sprites.update()
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
