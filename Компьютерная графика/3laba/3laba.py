import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL.Image import open

import numpy as np
import matplotlib.cm

def load_texture(filename):
    img = open(filename)
    img_data = img.tobytes('raw', 'RGB', 0, -1)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGB, img.size[0], img.size[1], GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return texture_id

def get_colors(cname, cnum=1):
    cnum_max = cnum + 2
    cmap = matplotlib.cm.get_cmap(cname, cnum_max)
    colors = np.array(cmap(np.linspace(1, 0, cnum_max)))
    colors = colors[1:cnum + 1, :3]
    return np.squeeze(colors)

class Cube:
    def __init__(self, texture_id=None):
        self.vertices = [(0, 0, 3),
                         (0, 1.5, 0),
                         (1.4, 0.44, 0),
                         (0.9, -1.2, 0),
                         (-0.9, -1.2, 0),
                         (-1.4, 0.44, 0)]

        self.faces = [(0, 1, 2),
                      (0, 2, 3),
                      (0, 3, 4),
                      (0, 4, 5),
                      (0, 5, 1),
                      (1, 2, 3),
                      (1, 3, 5),
                      (3, 4, 5)]

        self.edges = [(0, 1),
                      (0, 2),
                      (0, 3),
                      (0, 4),
                      (0, 5),
                      (1, 2),
                      (2, 3),
                      (3, 4),
                      (4, 5),
                      (5, 1)]

        self.colors = [(1, 0, 0),
                       (0, 1, 0),
                       (1, 1, 0),
                       (0, 0, 1),
                       (1, 0, 1),
                       (0, 1, 1),
                       (0, 1, 1),
                       (0, 1, 1)]

        self.uvs = [[(0, 0), (1, 0), (1, 1), (0, 1)],
                    [(0, 0), (1, 0), (1, 1), (0, 1)],
                    [(0, 0), (1, 0), (1, 1), (0, 1)],
                    [(0, 0), (1, 0), (1, 1), (0, 1)],
                    [(0, 0), (1, 0), (1, 1), (0, 1)],
                    [(0, 0), (1, 0), (1, 1), (0, 1)],
                    [(0, 0), (1, 0), (1, 1), (0, 1)],
                    [(0, 0), (1, 0), (1, 1), (0, 1)]]

        self.texture_id = texture_id

    def draw_edges(self):
        glBegin(GL_LINES)

        color = get_colors('Blues')
        glColor3f(*color)

        for edge in self.edges:
            glVertex3fv(self.vertices[edge[0]])
            glVertex3fv(self.vertices[edge[1]])
        glEnd()

    def draw_polygons(self):

        glBegin(GL_TRIANGLES)
        for fi, face in enumerate(self.faces):
            glColor3fv(self.colors[fi])
            for vi in face:
                glVertex3fv(self.vertices[vi])
        glEnd()

    def draw_texture(self):
        if self.texture_id is None:
            return
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glBegin(GL_TRIANGLES)
        glColor3f(1, 1, 1)
        for fi, face in enumerate(self.faces):
            for i, vi in enumerate(face):
                glTexCoord2fv(self.uvs[fi][i])
                glVertex3fv(self.vertices[vi])
        glEnd()
        glDisable(GL_TEXTURE_2D)

    def draw(self):
        glPushMatrix()
        glTranslatef(-3, 0, 0)
        glRotatef(-45, 1, 1, 1)
        glScalef(0.5, 0.5, 0.5)
        self.draw_edges()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(3, 0, 0)
        glRotatef(45, 1, 1, 1)
        glScalef(0.5, 0.5, 0.5)
        self.draw_polygons()
        glPopMatrix()
        self.draw_texture()


def main():
    pygame.init()
    size = (800, 600)
    screen = pygame.display.set_mode(size, OPENGL | HWSURFACE| DOUBLEBUF)

    aspect = size[0] / size[1]
    gluPerspective(45, aspect, 0.1, 50)
    glTranslatef(0, 0, -10)

    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_DEPTH_TEST)

    texture_id = load_texture('waves.png')
    cube = Cube(texture_id=texture_id)

    clock = pygame.time.Clock()

    is_rotate = True
    is_loop = True

    while is_loop:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_loop = False
            if event.type == KEYUP and event.key == K_q:
                is_loop = False
            if event.type == KEYUP and event.key == K_SPACE:
                is_rotate = not is_rotate
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if is_rotate:
            glRotatef(1, 2, 3, 2)

        cube.draw()
        pygame.display.flip()

    pygame.quit()


main()