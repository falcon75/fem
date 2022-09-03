import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np


x0 = np.array([
    [-1, -1],
    [-1, 1],
    [1, -1],
    [1, 1]
])

steps = 500
particles = 4
mass = 0.5
elasticity = 1
delta = 0.005
g = 9.81

x = np.zeros((steps, particles, 2)) 
v = np.zeros((steps, particles, 2))
radii = np.array([0.2 for _ in range(particles)])

x[0][0] = np.array([0.2, 0.5])
x[0][1] = np.array([-0.3, 0.5])
x[0][2] = np.array([0, 1])

bar_y = -1

for t in range(steps-1):

    for p in range(particles):

        force = -mass*g
        xn = x[t][p] + delta*v[t][p]
        collision = False

        for q in range(particles):

            if q == p:
                continue

            sep = xn - x[t][q] 

            if np.linalg.norm(sep) < radii[p] + radii[q] + 0.02:
                collision = True
                v[t+1][p] = -elasticity*np.dot(v[t][p], sep)*sep + (v[t][p] - np.dot(v[t][p], sep)*sep)
                x[t+1][p] = x[t][p] + delta*v[t+1][p] + 0.01*sep/np.linalg.norm(sep)
                break

        if xn[1] - bar_y < radii[p]:
            collision = True
            v[t+1][p] = v[t][p]
            v[t+1][p][1] = -elasticity*v[t][p][1]
            x[t+1][p] = x[t][p]

        if not collision:
            v[t+1][p] = v[t][p]
            v[t+1][p][1] = v[t][p][1] + delta*(1/mass)*force
            x[t+1][p] = xn


def draw(x, t):

    glBegin(GL_LINES)
    glVertex3fv((-5, -1, 0))
    glVertex3fv((5, -1, 0))
    glEnd()

    for i in range(len(x[t])):
        cx, cy = x[t][i][0], x[t][i][1]
        circle(cx, cy, radii[i], 50)

def circle(cx, cy, r, N):
    glBegin(GL_LINE_LOOP)
    for k in range(N):
        theta = (k/N)*2*np.pi
        x = r*np.cos(theta)
        y = r*np.sin(theta)
        glVertex2f(x + cx, y + cy)
    glEnd()


def main():

    pygame.init()
    display = (1200, 800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)


    gluPerspective(60, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -5)

    m = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        draw(x, m%steps)

        pygame.display.flip()
        pygame.time.wait(int(1000*delta))

        m += 1

main()