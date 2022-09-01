import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
import random


x = np.zeros((100, 100, 100))

for i in range(20):
    for j in range(20):
        x[0, 40+i, 40+j] = random.choice([0, 0, 1])


rule = {
    0: {
        0: {
            0: 0,
            1: 1
        },
        1: {
            0: 1,
            1: 1
        }
    },
    1: {
        0: {
            0: 0,
            1: 1
        },
        1: {
            0: 1,
            1: 0
        }
    }
}

def update(x, k):
    L = 100
    for i in range(1, L-1):
        for j in range(1, L-1):
            x[k+1, i, j] = rule[x[k, i, j]][x[k, i+1, j]][x[k, i, j+1]] or rule[x[k, i, j]][x[k, i-1, j]][x[k, i, j-1]]

for i in range(99):
    update(x, i)


def board(k):
    for i in range(99):
        for j in range(99):
            if x[k, i, j] == 1:
                square(i, j)

def square(x, y):
    sq = np.array([
        [x, y],
        [x + 1, y],
        [x, y + 1],
        [x + 1, y + 1]
    ], dtype='float64')
    sq -= 50
    sq *= 0.02

    glBegin(GL_QUADS)
    for k in range(4):
        glVertex3fv((sq[k][0], sq[k][1],  0))
    glEnd()


def main():

    pygame.init()
    display = (1500,1000)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)


    gluPerspective(60, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -2)

    m = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        board(m % 100)

        pygame.display.flip()
        pygame.time.wait(100)

        m += 1

main()

