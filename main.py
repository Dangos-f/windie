import pygame
import random
import math

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLAYER_RADIUS = 15
BULLET_RADIUS = 5
BULLET_SPEED = 10
SHRINK_AMOUNT = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Shooting Game")
clock = pygame.time.Clock()

# Lock the window position
pygame.event.set_grab(True)


# Player class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = PLAYER_RADIUS
        self.bullets = []

    def draw(self, screen):
        f"""Отрисовка персонажа на холсте. {screen} -- объект экрана(холст)"""
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)
        for bullet in self.bullets:
            bullet.draw(screen)

    def move(self, dx, dy):
        """изменение координат. выполняет перемещение персонажа по экрану."""
        self.x += dx
        self.y += dy

    def shoot(self):
        """Создание и отрисовка пули.
        пуля летит по прямой траектори по направлению к курсору от персонажа."""
        bullet = Bullet(self.x, self.y)
        cursor_x, cursor_y = pygame.mouse.get_pos()
        bullet.set_velocity_towards_cursor(cursor_x, cursor_y)
        self.bullets.append(bullet)

    def update_bullets(self):
        """обработка соприкосновения пули с границей экрана.
        при соприкоснавении экран отодвигается от пули."""
        global WINDOW_WIDTH, WINDOW_HEIGHT
        for bullet in self.bullets:
            bullet.update()
            if bullet.is_outside_screen():
                self.bullets.remove(bullet)
                if bullet.x <= 0 or bullet.x >= WINDOW_WIDTH:
                    if bullet.x <= 0:
                        WINDOW_WIDTH += SHRINK_AMOUNT
                        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                    else:
                        WINDOW_WIDTH += SHRINK_AMOUNT
                        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                if bullet.y <= 0 or bullet.y >= WINDOW_HEIGHT:
                    if bullet.y <= 0:
                        WINDOW_HEIGHT += SHRINK_AMOUNT
                        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                    else:
                        WINDOW_HEIGHT += SHRINK_AMOUNT
                        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


# Bullet class
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = BULLET_RADIUS
        self.dx = 0
        self.dy = -BULLET_SPEED

    def draw(self, screen):
        f"""Отрисовка пули на холсте. принимает параметр {screen} -- холст"""
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)

    def update(self):
        """Обновление положения пули на экране.
        нужно, чтобы пуля постоянно летела, каждый кадр."""
        self.x += self.dx
        self.y += self.dy

    def is_outside_screen(self):
        """"это вообще волшебная функция. я хз как она работает, но явно не без божьей помощи.
        не совветую её трогать!"""
        return self.x < 0 or self.x > WINDOW_WIDTH or self.y < 0 or self.y > WINDOW_HEIGHT

    def set_velocity_towards_cursor(self, cursor_x, cursor_y):
        dx = cursor_x - self.x
        dy = cursor_y - self.y
        angle = math.atan2(dy, dx)
        self.dx = math.cos(angle) * BULLET_SPEED
        self.dy = math.sin(angle) * BULLET_SPEED


# Game loop
def game_loop():
    """Главный цикл программы со всеми обработчиками."""
    player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.shoot()

        # Keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move(0, -5)
        if keys[pygame.K_s]:
            player.move(0, 5)
        if keys[pygame.K_a]:
            player.move(-5, 0)
        if keys[pygame.K_d]:
            player.move(5, 0)

        player.update_bullets()

        screen.fill(BLACK)
        player.draw(screen)
        pygame.display.update()

        clock.tick(60)


# Start the game
game_loop()
