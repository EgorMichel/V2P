import pygame
import random

pygame.init()

population = 300
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
FPS = 90
running = True

pygame.display.set_caption("V2P")


class Molecule:
    def __init__(self, x, y, z, velocity, m):
        self.m = m
        self.x = x
        self.y = y
        self.z = z
        self.velocity = velocity

    def draw(self, color):
        x, y = self.x, self.y
        pygame.draw.circle(screen, color, (int(x), int(y)), 6 - self.z/200)


molecules = [Molecule(random.randint(0, 800), random.randint(0, 800), random.randint(0, 800), [random.randint(-5, 5),
                                                                                               random.randint(-5, 5),
                                                                random.randint(-5, 5)], 1) for i in range(population)]


def render():
    screen.fill((20, 5, 40))
    for molecule in molecules:
        red = 8.16 * abs((molecule.velocity[0]**2 + molecule.velocity[1]**2 + molecule.velocity[2]**2)**(1/2))
        if red > 255:
            red = 255
        molecule.draw((red, 0, 255 - red))


def update():
    for molecule in molecules:
        molecule.x += molecule.velocity[0]
        molecule.y += molecule.velocity[1]
        molecule.z += molecule.velocity[2]

        if molecule.x > 800 or molecule.x < 0:
            molecule.velocity[0] *= -1

        if molecule.y > 800 or molecule.y < 0:
            molecule.velocity[1] *= -1

        if molecule.z > 800 or molecule.z < 0:
            molecule.velocity[2] *= -1



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update()
    render()

    pygame.display.update()
    clock.tick(FPS)

