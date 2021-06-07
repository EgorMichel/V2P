import pygame
import random

pygame.init()

k1 = 10
k2 = 10
k3 = 1
population = k1 * k2 * k3

Helium_diam_absolut = 2.1 * 10 ** (-11)  # meters
meters_in_pixel = 2.1 * 10 ** (-11)  # 2,625 * 10 ** (-11)
Helium_diam_relative_max = 8
dt = 5*10 ** (-13)  # seconds
initial_velocity = 100  # meters / second
k_bolzman = 1.38 * 10 ** (-23)
eps_potential = 10.22 * k_bolzman  # Joules
sigma_potential = 2.556 * 10 ** (-10)  # meters
mass = 6.64 * 10 ** (-27)  # kg
pendulum = 0

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
        plus = int(255 - self.z / meters_in_pixel / 5)
        # print(int(x / meters_in_pixel), int(y / meters_in_pixel))
        pygame.draw.circle(screen, (color[0], 0, color[2]), (int(x / meters_in_pixel), int(y / meters_in_pixel)),
                           int(6 - self.z / meters_in_pixel / 200))


molecules = []

for i in range(k1):
    for j in range(k2):
        for k in range(k3):
            molecules.append(Molecule((35 + 70 * i) * meters_in_pixel,
                                      (35 + 70 * j) * meters_in_pixel,
                                      35 * meters_in_pixel,
                                      [random.uniform(-initial_velocity, initial_velocity),
                                       random.uniform(-initial_velocity, initial_velocity),
                                       random.uniform(-initial_velocity, initial_velocity)],
                                      mass))

# molecules = [Molecule(random.randint(0, width) * meters_in_pixel,
#                       random.randint(0, height) * meters_in_pixel,
#                       random.randint(0, depth) * meters_in_pixel,
#                       [random.randint(-initial_velocity, initial_velocity),
#                        random.randint(-initial_velocity, initial_velocity),
#                        random.randint(-initial_velocity, initial_velocity)],
#                       mass) for i in range(population)]


def render():
    screen.fill((20, 5, 40))
    for molecule in molecules:
        constant = 255 / (1 + initial_velocity ** 2 * 3) ** 0.5
        red = constant * abs(
            (molecule.velocity[0] ** 2 + molecule.velocity[1] ** 2 + molecule.velocity[2] ** 2) ** (1 / 2))
        if red > 255:
            red = 255
        molecule.draw((red, 0, 255 - red))


def distance(molecule1, molecule2):
    return ((molecule1.x - molecule2.x) ** 2 + (molecule1.y - molecule2.y) ** 2 +
            (molecule1.z - molecule2.z) ** 2) ** 0.5


def update():
    global pendulum
    average_speed = 0
    for molecule in molecules:
        average_speed += molecule.velocity[0] ** 2 + molecule.velocity[1] ** 2 + molecule.velocity[2] ** 2

        if molecule.x > width * meters_in_pixel or molecule.x < 0:
            molecule.velocity[0] *= -1
            pendulum += abs(2*molecule.velocity[0] * mass)

        if molecule.y > height * meters_in_pixel or molecule.y < 0:
            molecule.velocity[1] *= -1
            pendulum += abs(2 * molecule.velocity[1] * mass)

        if molecule.z > depth * meters_in_pixel or molecule.z < 0:
            molecule.velocity[2] *= -1
            pendulum += abs(2 * molecule.velocity[2] * mass)

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
                dist = distance(molecule, another_m)
                force = eps_potential * (
                            (-48 * sigma_potential ** 12) / dist ** 13 + (24 * sigma_potential ** 6) / dist ** 7)
                molecule.velocity[0] += dt * ((molecule.x - another_m.x) * force / dist) / mass
                molecule.velocity[1] += dt * ((molecule.y - another_m.y) * force / dist) / mass
                molecule.velocity[2] += dt * ((molecule.z - another_m.z) * force / dist) / mass

    for molecule in molecules:
        molecule.x += molecule.velocity[0] * dt
        molecule.y += molecule.velocity[1] * dt
        molecule.z += molecule.velocity[2] * dt
    return average_speed / population


time = 0
pressure = 0
cycles = 0
while running:
    cycles += 1
    time += dt
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    speed = update()
    T = (speed * mass / (3 * k_bolzman))
    print(time, "T =", T, "K")
    render()
    if cycles % 10 == 0:
        pressure = pendulum / (10 * dt * (height*width + height*depth + width*depth))
        pendulum = 0
    print(pressure, "Pa, theory: ", k_bolzman * T * population/(width*height*depth))

    pygame.display.update()
    clock.tick(FPS)
    #dt = 2*meters_in_pixel/(speed)**(1/2)