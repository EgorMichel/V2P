import pygame
import random
import matplotlib.pyplot as plt
import numpy as np
import gc

k1 = 5
k2 = 5
k3 = 5
population = k1 * k2 * k3

pi = np.pi
G = 6.6743 * 10 ** (-11)  # (-11)
Helium_diam_absolut = 2.1 * 10 ** (-11)  # meters
b = 23.6 * 10 ** -6
a = 0.00338
mu = 0.004
meters_in_pixel = 0.8 * 10 ** (-11)  # 2,625 * 10 ** (-11)
Helium_diam_relative_max = 8
dt = 8 * 10 ** (-14)  # seconds
k_bolzman = 1.38 * 10 ** (-23)
eps_potential = 10.22 * k_bolzman  # Joules
sigma_potential = 2.556 * 10 ** (-10)  # meters
mass = 6.64 * 10 ** (-27)  # kg
pendulum = 0
velocities = []
free_run_length = []
nu = population * mass / mu

width = 800
height = 800
depth = 800

Volume = ((width * height * depth) * meters_in_pixel ** 3)
Area = 2 * (width * height + width * depth + height * depth) * meters_in_pixel ** 2


pygame.init()

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
FPS = 60
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
        # print(int(x / meters_in_pixel), int(y / meters_in_pixel))
        pygame.draw.circle(screen, (color[0], 0, color[2]), (int(x / meters_in_pixel), int(y / meters_in_pixel)),
                           int(6 - self.z / meters_in_pixel / 200))


def render(molecules_):
    screen.fill((20, 5, 40))
    for molecule in molecules_:
        constant = 255 / (1 + initial_velocity ** 2 * 3) ** 0.5
        red = constant * abs(
            (molecule.velocity[0] ** 2 + molecule.velocity[1] ** 2 + molecule.velocity[2] ** 2) ** (1 / 2))
        if red > 255:
            red = 255
        molecule.draw((red, 0, 255 - red))


def distance(molecule1, molecule2):
    return ((molecule1.x - molecule2.x) ** 2 + (molecule1.y - molecule2.y) ** 2 +
            (molecule1.z - molecule2.z) ** 2) ** 0.5


def maxwell(v_, t_):
    return 4 * pi * (mass / (2 * pi * k_bolzman * t_)) ** 1.5 * v_ ** 2 * np.exp(-mass * v_ ** 2 / (2 * k_bolzman * t_))


def update(molecules_):
    global pendulum
    global velocities
    sum_speed_squared = 0
    for molecule in molecules_:
        current_speed = molecule.velocity[0] ** 2 + molecule.velocity[1] ** 2 + molecule.velocity[2] ** 2
        sum_speed_squared += current_speed

        velocities.append(current_speed ** 0.5)

        if molecule.x > width * meters_in_pixel or molecule.x < 0:
            molecule.velocity[0] *= -1
            pendulum += abs(2 * molecule.velocity[0] * mass)

        if molecule.y > height * meters_in_pixel or molecule.y < 0:
            molecule.velocity[1] *= -1
            pendulum += abs(2 * molecule.velocity[1] * mass)

        if molecule.z > depth * meters_in_pixel or molecule.z < 0:
            molecule.velocity[2] *= -1
            pendulum += abs(2 * molecule.velocity[2] * mass)

        for another_m in molecules_:
            if abs(another_m.x - molecule.x) > 0 \
                    or abs(another_m.y - molecule.y) > 0 \
                    or abs(another_m.z - molecule.z) > 0:
                # molecule.velocity[0] += G * another_m.m * (another_m.x - molecule.x) * dt \
                #                         / ((distance(molecule, another_m)) ** 3)
                #
                # molecule.velocity[1] += G * another_m.m * (another_m.y - molecule.y) * dt \
                #                         / ((distance(molecule, another_m)) ** 3)
                #
                # molecule.velocity[2] += G * another_m.m * (another_m.z - molecule.z) * dt \
                #                         / ((distance(molecule, another_m)) ** 3)
                dist = distance(molecule, another_m)
                force = (24 * eps_potential * sigma_potential ** 6) / (dist ** 7) * (
                        (((-2) * (sigma_potential ** 6)) / (dist ** 6)) + 1)
                molecule.velocity[0] += dt * ((another_m.x - molecule.x) * force / dist) / mass
                molecule.velocity[1] += dt * ((another_m.y - molecule.y) * force / dist) / mass
                molecule.velocity[2] += dt * ((another_m.z - molecule.z) * force / dist) / mass

    for molecule in molecules_:
        molecule.x += molecule.velocity[0] * dt
        molecule.y += molecule.velocity[1] * dt
        molecule.z += molecule.velocity[2] * dt
    return sum_speed_squared / population


molecules = []
times = []
p_idl = []
p_exp = []
p_vdw = []
temperatures = []

num1x = width / k1
num1y = height / k2
num1z = depth / k3
initial_velocity = 100

iterations = 4
print(iterations)
while iterations < 10:
    iterations += 1
    initial_velocity = 100  # meters / second

    running = True

    molecules = []
    times = []
    p_idl = []
    p_exp = []
    p_vdw = []
    temperatures = []

    num1x = width / k1
    num1y = height / k2
    num1z = depth / k3

    for i in range(k1):
        for j in range(k2):
            for k in range(k3):
                molecules.append(Molecule((num1x / 2 + num1x * i) * meters_in_pixel,
                                          (num1y / 2 + num1y * j) * meters_in_pixel,
                                          (num1z / 2 + num1z * k) * meters_in_pixel,
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

    time = 0
    pressure = 0
    cycles = 0
    cycles_for_report = 100
    while running:
        # if cycles / cycles_for_report == 50:
        #     running = False
        cycles += 1
        time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        avg_speed_squared = update(molecules)

        render(molecules)

        if cycles % cycles_for_report == 0 and cycles > 0:
            T = (avg_speed_squared * mass / (3 * k_bolzman))
            print("Time:", time, "T =", T, "K")
            pressure = pendulum / (cycles_for_report * dt * Area)
            pendulum = 0
            ideal_pressure = k_bolzman * T * population / Volume
            vdw_pressure = 8.31 * nu * T / (Volume - b * nu) - a * nu ** 2 / Volume ** 2
            if abs(pressure - ideal_pressure) > 2 * ideal_pressure:
                print("Simulation has been broken")
                continue
            print(pressure, "Pa, ideal: ", ideal_pressure, 'Pa, VdW:', vdw_pressure)
            temperatures.append(T)
            p_idl.append(ideal_pressure)
            p_exp.append(pressure)
            p_vdw.append(vdw_pressure)
            times.append(time)

        pygame.display.update()
        clock.tick(FPS)
        # dt = 2*meters_in_pixel/(speed)**(1/2)

    # fig, ax = plt.subplots()
    # ax.plot(times, p_exp)
    #
    # line1 = ax.plot(times, p_exp, label='pressure from pendulum')
    # line2 = ax.plot(times, p_idl, label='pressure from ideal')
    # line3 = ax.plot(times, p_vdw, label='pressure from Van der Waals')
    #
    # error_idl = abs(sum(p_exp) / len(p_exp) - sum(p_idl) / len(p_idl)) / (sum(p_idl) / len(p_idl))
    # error_vdw = abs(sum(p_exp) / len(p_exp) - sum(p_vdw) / len(p_vdw)) / (sum(p_vdw) / len(p_vdw))
    # T = round(sum(temperatures) / len(temperatures), 2)
    # ax.set(xlabel='time (s)', ylabel='pressure (Pa)',
    #        title='T = {0} K, error_idl = {1}% error_VdW = {2}%'.format(
    #            str(T), str(round(error_idl * 100, 2)), str(round(error_vdw * 100, 2))))
    #
    # ax.grid()
    # ax.legend()
    # fig.savefig("Helium_" + str(T) + ".png")
    # # plt.show()
    #
    # max_velocity = max(velocities)
    # length = len(velocities)
    # velocities_maxwell = []
    #
    # for v in range(int(max_velocity)):
    #     for i in range(int(maxwell(v, T) * 10000)):
    #         velocities_maxwell.append(v)
    #
    # fig2, ax2 = plt.subplots()
    # ax2.hist(velocities, alpha=0.5, label='Experiment', bins=20, density=True)
    # ax2.hist(velocities_maxwell, alpha=0.5, label='Maxwell', bins=20, density=True)
    # ax2.set(xlabel='Speed', ylabel='Density',
    #         title='Helium, T = {0} K, speed distribution'.format(str(T)))
    # ax2.legend()
    # fig2.savefig("Helium_hist" + str(T) + ".png")
    #
    # # plt.show()

    print(iterations)
    gc.collect()
