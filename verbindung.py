import pygame
import random

# Initialize pygame
pygame.init()

# Set up the game window
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
blue = (0, 0, 255)
red = (255, 0, 0)

# Snake class
class Snake:
    def __init__(self):
        self.size = 1
        self.positions = [(width // 2, height // 2)]
        self.direction = random.choice(["up", "down", "left", "right"])

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        x, y = self.get_head_position()
        if self.direction == "up":
            y -= 10
        elif self.direction == "down":
            y += 10
        elif self.direction == "left":
            x -= 10
        elif self.direction == "right":
            x += 10
        self.positions.insert(0, (x, y))
        if len(self.positions) > self.size:
            self.positions.pop()

    def change_direction(self, direction):
        if direction == "up" and self.direction != "down":
            self.direction = "up"
        elif direction == "down" and self.direction != "up":
            self.direction = "down"
        elif direction == "left" and self.direction != "right":
            self.direction = "left"
        elif direction == "right" and self.direction != "left":
            self.direction = "right"

    def draw(self, window):
        for position in self.positions:
            pygame.draw.rect(window, red, (position[0], position[1], 10, 10))

# Object class
class Object:
    def __init__(self):
        self.position = (random.randint(0, width-10), random.randint(0, height-10))

    def draw(self, window):
        pygame.draw.rect(window, blue, (self.position[0], self.position[1], 10, 10))

# Set up the game
snake = Snake()
obj = Object()
clock = pygame.time.Clock()

# Game loop
game_over = False
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                snake.change_direction("up")
            elif event.key == pygame.K_s:
                snake.change_direction("down")
            elif event.key == pygame.K_a:
                snake.change_direction("left")
            elif event.key == pygame.K_d:
                snake.change_direction("right")

    # Move the snake
    snake.move()

    # Check for collisions
    if snake.get_head_position() == obj.position:
        snake.size += 1
        obj = Object()

    # Check for self-collision or border collision
    if (
        snake.get_head_position() in snake.positions[1:]
        or snake.get_head_position()[0] < 0
        or snake.get_head_position()[0] >= width
        or snake.get_head_position()[1] < 0
        or snake.get_head_position()[1] >= height
    ):
        game_over = True

    # Draw on the window
    window.fill((0, 0, 0))
    snake.draw(window)
    obj.draw(window)
    pygame.display.update()

    # Set the game speed
    clock.tick(20)

# Quit the game
pygame.quit()
