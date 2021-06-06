import pygame
import random

pygame.init()

population = 100

Helium_diam_absolut = 2.1 * 10 ** (-10)  # meters
meters_in_pixel = 2 * 10 ** (-12)  # 2,625 * 10 ** (-11)
Helium_diam_relative_max = 8
dt = 10 ** (-14)  # seconds
initial_velocity = 1000  # meters / second
k_bolzman = 1.38 * 10 ** (-23)
eps_potential = 10.22 * k_bolzman  # Joules
sigma_potential = 2.556 * 10 ** (-10)  # meters

width = 800
height = 800
depth = 800

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
FPS = 60
running = True

G = 6.6743 * 10 ** (-11)  # (-11)

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
        pygame.draw.circle(screen, color, (int(x / meters_in_pixel), int(y / meters_in_pixel)),
                           int(6 - self.z / meters_in_pixel / 200))


molecules = [Molecule(random.randint(0, width) * meters_in_pixel,
                      random.randint(0, height) * meters_in_pixel,
                      random.randint(0, depth) * meters_in_pixel,
                      [random.randint(-initial_velocity, initial_velocity),
                       random.randint(-initial_velocity, initial_velocity),
                       random.randint(-initial_velocity, initial_velocity)],
                      6.64 * 10 ** (-27)) for i in range(population)]


def render():
    screen.fill((20, 5, 40))
    for molecule in molecules:
        constant = 255 / (initial_velocity ** 2 * 3) ** 0.5
        red = constant * abs(
            (molecule.velocity[0] ** 2 + molecule.velocity[1] ** 2 + molecule.velocity[2] ** 2) ** (1 / 2))
        if red > 255:
            red = 255
        molecule.draw((red, 0, 255 - red))


def distance(molecule1, molecule2):
    return ((molecule1.x - molecule2.x) ** 2 + (molecule1.y - molecule2.y) ** 2 +
            (molecule1.z - molecule2.z) ** 2) ** 0.5


def update():
    for molecule in molecules:
        for another_m in molecules:
            if another_m.x != molecule.x and another_m.y != molecule.y and another_m.z != molecule.z:
                # molecule.velocity[0] += G * another_m.m * (another_m.x - molecule.x) * dt \
                #                         / ((distance(molecule, another_m)) ** 3)
                #
                # molecule.velocity[1] += G * another_m.m * (another_m.y - molecule.y) * dt \
                #                         / ((distance(molecule, another_m)) ** 3)
                #
                # molecule.velocity[2] += G * another_m.m * (another_m.z - molecule.z) * dt \
                #                         / ((distance(molecule, another_m)) ** 3)
                molecule.velocity[0] += (-48 * eps_potential * sigma_potential ** 12
                                         + 24 * eps_potential * sigma_potential ** 6
                                         * distance(molecule, another_m) ** 6) \
                                        * (another_m.x - molecule.x) / (distance(molecule, another_m) ** 14)

                molecule.velocity[0] += (-48 * eps_potential * sigma_potential ** 12
                                         + 24 * eps_potential * sigma_potential ** 6
                                         * distance(molecule, another_m) ** 6) \
                                        * (another_m.y - molecule.y) / (distance(molecule, another_m) ** 14)

                molecule.velocity[0] += (-48 * eps_potential * sigma_potential ** 12
                                         + 24 * eps_potential * sigma_potential ** 6
                                         * distance(molecule, another_m) ** 6) \
                                        * (another_m.z - molecule.z) / (distance(molecule, another_m) ** 14)

        molecule.x += molecule.velocity[0] * dt
        molecule.y += molecule.velocity[1] * dt
        molecule.z += molecule.velocity[2] * dt

        if molecule.x > width * meters_in_pixel or molecule.x < 0:
            molecule.velocity[0] *= -1

        if molecule.y > height * meters_in_pixel or molecule.y < 0:
            molecule.velocity[1] *= -1

        if molecule.z > depth * meters_in_pixel or molecule.z < 0:
            molecule.velocity[2] *= -1


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    update()
    render()

    pygame.display.update()
    clock.tick(FPS)
