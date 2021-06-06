import pygame
import random
import pymunk

pygame.init()

population = 0
right_population = 300
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
FPS = 90
space = pymunk.Space()
running = True

pygame.display.set_caption(" Nazi game")


class point():
    def __init__(self, x, y, elastic):
        self.x = x
        self.y = y
        self.body = pymunk.Body()
        self.body.position = x, y
        self.body.velocity = random.uniform(-100, 100), random.uniform(-100, 100)
        self.shape = pymunk.Circle(self.body, 3)
        self.shape.density = 1
        self.shape.elasticity = elastic
        space.add(self.body, self.shape)

    def draw(self, color):
        x, y = self.body.position
        pygame.draw.rect(screen, color, (int(x), int(y), 4, 4))


class wall:
    def __init__(self, p1, p2):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, p1, p2, 5)
        self.shape.elasticity = 1
        space.add(self.body, self.shape)


Points = [point(random.randint(0, 800), random.randint(0, 800), 1) for i in range(population)]

Right_Points = [point(random.randint(0, 800), random.randint(0, 800), 1) for i in range(right_population)]

Walls = [wall((0, 0), (0, 800)),
         wall((0, 0), (800, 0)),
         wall((0, 800), (800, 800)),
         wall((800, 0), (800, 800))]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((20, 5, 40))

    for point in Points:
        point.draw((255, 130, 210))

    for point in Right_Points:
        red = 1.2 * abs(point.body.velocity)
        if red > 255:
            red = 255
        point.draw((red, 0, 255 - red))

    pygame.display.update()
    clock.tick(FPS)
    space.step(1/FPS)