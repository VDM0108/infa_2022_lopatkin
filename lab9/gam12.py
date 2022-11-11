import math
from random import *

import pygame
from pygame.draw import *

from numpy import sign


FPS = 60

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x, y=(HEIGHT-80)):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        #self.limit = []
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 50
        self.x_acceleration = 0
        self.y_acceleration = 2

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.x - self.r <= 0:
            self.vx = abs(self.vx)
        if self.x + self.r >= WIDTH:
            self.vx = -abs(self.vx)
        if self.y - self.r + self.vy >= HEIGHT:
            self.vy = - abs(self.vy)
        if self.y + self.r + self.vy <= 0:
            self.vy = abs(self.vy)
        self.vy = self.vy + 2
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        # line(self.screen, (255, 0, 0), (0, min(self.limit)), (WIDTH, min(self.limit)), 1)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            balls.remove(self)
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x0 = 80
        self.y0 = HEIGHT - 80
        self.go = 0

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, x = self.x0)
        self.an = math.atan2((self.y0 - event.pos[1]), (event.pos[0] - self.x0))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = -self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2((self.y0 - event.pos[1]), (event.pos[0] - self.x0))
        if self.f2_on:
            self.color = (self.f2_power + 155, 0, 0)
        else:
            self.color = GREY
    def draw(self):
        polygon(screen, self.color, [[self.x0 - 5 * math.sin(self.an), self.y0 - 5 * math.cos(self.an)],
                                     [self.x0 + self.f2_power * math.cos(self.an) - 5 * math.sin(self.an),
                                      self.y0 - self.f2_power * math.sin(self.an) - 5 * math.cos(self.an)],
                                     [self.x0 + self.f2_power * math.cos(self.an) + 5 * math.sin(self.an),
                                      self.y0 - self.f2_power * math.sin(self.an) + 5 * math.cos(self.an)],
                                     [self.x0 + 5 * math.sin(self.an), self.y0 + 5 * math.cos(self.an)],
                                     ])
        circle(screen, (80, 80, 80), (self.x0 - 50, HEIGHT-20), 20)
        circle(screen, (80, 80, 80), (self.x0 + 50, HEIGHT-20), 20)
        circle(screen, (100, 100, 100), (self.x0, HEIGHT-70), 20)
        rect(screen, (131, 77, 24), (self.x0 - 50, HEIGHT-70, 100, 50))
        rect(screen, (100, 100, 100), (self. x0 - 50, HEIGHT-70, 100, 50), 5)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = (self.f2_power + 155, 0, 0)
        else:
            pass
            self.color = GREY


class Target:
    def __init__(self, screen):
        self.points = 0
        self.live = 1
        self.color = RED
        self.r = randint(5, 50)
        self.x = randint(self.r + 1, WIDTH - self.r - 1)
        self.y = randint(self.r + 1, HEIGHT - self.r - 1)
        self.vx = randint(5, 20)
        self.vy = randint(5, 20)

    def move(self):
        self.x += self.vx
        self.y += self.vy

        if self.y >= HEIGHT - self.r or self.y <= self.r:
            self.vy = -self.vy
        if self.x <= self.r or self.x >= WIDTH - self.r:
            self.vx = -self.vx

    def new_target(self):
        """ Инициализация новой цели. """
        self.live = 1
        self.x = randint(self.r + 1, WIDTH - self.r -1)
        self.y = randint(self.r + 1, HEIGHT - self.r - 1)
        self.r = randint(5, 50)
        self.vx = randint(5, 20)
        self.vy = randint(5, 20)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        circle(screen, self.color, (self.x, self.y), self.r)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
finished = False
i = 0

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    for b in balls:
        if b.live:
            b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    target.move()
    for b in balls:
        if b.live:
            b.move()
        else:
            balls.remove(b)
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()
    gun.power_up()

pygame.quit()