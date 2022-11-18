from random import *
import pygame
from pygame.draw import *

pygame.font.init()


# создаём класс
class Ball:
    def __init__(self):
        self.alive = True



        self.radius = randint(10, 30)
        self.pos = (randint(0 + self.radius, screen_size[0] - self.radius), randint(0 + self.radius, screen_size[1] - self.radius))
        self.x_velocity = randint(-5, 5)
        self.y_velocity = randint(-5, 5)

        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        GREEN = (0, 255, 255)
        YELLOW = (255, 255, 0)
        MAGENTA = (255, 0, 255)
        CYAN = (0, 255, 255)
        COLORS = [RED, BLUE, GREEN, YELLOW, MAGENTA, CYAN]
        self.color = COLORS[randint(0, len(COLORS) - 1)]

    # рисование мишени
    def new_ball(self):
        circle(screen, self.color, self.pos, self.radius)
    # расчёт координаты при движении
    def move(self):
        self.pos = (self.pos[0] + self.x_velocity, self.pos[1] + self.y_velocity)
        self.new_ball()

        # отталкивание от стены
        if self.pos[0] <= self.radius or self.pos[0] >= screen_size[0] - self.radius:
            self.x_velocity = -self.x_velocity
        if self.pos[1] <= self.radius or self.pos[1] >= screen_size[1] - self.radius:
            self.y_velocity = -self.y_velocity


    # попадание по мишени
    def hit(self, cords):
        if (cords[0] - self.pos[0]) ** 2 + (cords[1] - self.pos[1]) ** 2 <= (self.radius + gun_radius) ** 2 or (cords[0] - self.pos[0] - self.x_velocity) ** 2 + (cords[1] - self.pos[1] - self.y_velocity) ** 2 <= (self.radius + gun_radius) ** 2:
                return True



FPS = 120
screen_size = (1000, 800)
screen = pygame.display.set_mode(screen_size)

my_font = pygame.font.SysFont('microsoftttaile', 24)

clock = pygame.time.Clock()
finished = False

Balls = []
count = 3
Score = 0
gun_radius = 10

for i in range(count):
    Balls.append(Ball())


def kill(s, c):
    for i in s:
        if i.alive and i.hit(c):
            i.alive = False
            return True


while not finished:
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and kill(Balls, event.pos):
                Score += 1
                add_count = choice([1, 1, 1, 2])
                for k in range(add_count):
                    Balls.append(Ball())

        if event.type == pygame.MOUSEMOTION:  # прицел
            circle(screen, (200, 200, 200), event.pos, gun_radius, 2)

    for j in Balls:
        if j.alive:
            j.move()

    text_surface = my_font.render(str(Score), True, (255, 0, 0))  # счётчик
    screen.blit(text_surface, (10, 10))

    pygame.display.update()
pygame.quit()