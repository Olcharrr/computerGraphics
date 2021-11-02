# pip install pygame
# pip install PyOpenGL PyOpenGL_accelerate

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()
size = (800, 800)
screen = pygame.display.set_mode(size, OPENGL | HWSURFACE | DOUBLEBUF)

aspect = size[0] / size[1]
length = 2
glOrtho(-length * aspect, length * aspect, -length, length, -length, length)

glEnable(GL_LINE_SMOOTH)

glClear(GL_COLOR_BUFFER_BIT)
glBegin(GL_LINES)
glColor3f(1, 0, 0)

glVertex3f(0, 1.5, 0)
glVertex3f(1, -1, 0)
glVertex3f(1, -1, 0)
glVertex3f(0, -0.8, 0)
glVertex3f(0, -0.8, 0)
glVertex3f(0, 1.5, 0)

glEnd()

pygame.display.flip()

loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False

pygame.quit()