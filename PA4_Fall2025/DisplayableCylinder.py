"""
Define cylinder here.
First version in 11/01/2021

:author: micou(Zezhou Sun), Daniel Scrivener
:version: 2025.11.11
"""

from Displayable import Displayable
from GLBuffer import VAO, VBO, EBO
from Point import Point
import numpy as np
import ColorType
import math
try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
    except ImportError:
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res:
                return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")


class DisplayableCylinder(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    # stores current torus's information, read-only
    sides = 0
    radius = 0
    height = 0
    color = None

    vertices = None
    indices = None

    def __init__(self, shaderProg, sides=36, radius=0.5, height=1, color=ColorType.SOFTBLUE):
        super(DisplayableCylinder, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(sides, radius, height, color)

    def generate(self, sides=36, radius=0.5, height=1, color=ColorType.SOFTBLUE):
        self.sides = sides
        self.radius = radius
        self.height = height
        self.color = color

        # half top half bottom
        halfH = height * 0.5
        tris = []

        # angles for each side
        angles = np.linspace(0, 2*np.pi, sides + 1)

        # sides
        for i in range(sides):
            # start and end angle
            a0 = angles[i]
            a1 = angles[i + 1]

            # wall normal, points outward
            n0 = [np.cos(a0), np.sin(a0), 0]
            n1 = [np.cos(a1), np.sin(a1), 0]

            # uv mapping
            u0 = i / sides
            u1 = (i + 1) / sides

            # 4 corners
            x0 = radius * np.cos(a0)
            y0 = radius * np.sin(a0)
            x1 = radius * np.cos(a1)
            y1 = radius * np.sin(a1)

            p0b = [x0, -halfH, y0]
            p1b = [x1, -halfH, y1]
            p0t = [x0, halfH, y0]
            p1t = [x1, halfH, y1]

            # two triangles
            tris.append(p0b + n0 + list(color) + [u0, 0])
            tris.append(p0t + n0 + list(color) + [u0, 1])
            tris.append(p1b + n1 + list(color) + [u1, 0])

            tris.append(p0t + n0 + list(color) + [u0, 1])
            tris.append(p1t + n1 + list(color) + [u1, 1])
            tris.append(p1b + n1 + list(color) + [u1, 0])

        # top
        top_center = [0, halfH, 0]
        # points up
        top_normal = [0, 1, 0]

        for i in range(sides):
            a0 = angles[i]
            a1 = angles[i + 1]

            x0 = radius * np.cos(a0)
            y0 = radius * np.sin(a0)
            x1 = radius * np.cos(a1)
            y1 = radius * np.sin(a1)

            p0 = [x0, halfH, y0]
            p1 = [x1, halfH, y1]

            # [0, 1]
            u0 = 0.5 + x0 / (2 * radius)
            v0 = 0.5 + y0 / (2 * radius)
            u1 = 0.5 + x1 / (2 * radius)
            v1 = 0.5 + y1 / (2 * radius)

            tris.append(top_center + top_normal + list(color) + [0.5, 0.5])
            tris.append(p0 + top_normal + list(color) + [u0, v0])
            tris.append(p1 + top_normal + list(color) + [u1, v1])

        bot_center = [0, -halfH, 0]
        bot_normal = [0, -1, 0]

        for i in range(sides):
            a0 = angles[i]
            a1 = angles[i + 1]

            x0 = radius * np.cos(a0)
            y0 = radius * np.sin(a0)
            x1 = radius * np.cos(a1)
            y1 = radius * np.sin(a1)

            p0 = [x0, -halfH, y0]
            p1 = [x1, -halfH, y1]

            u0 = 0.5 + x0 / (2 * radius)
            v0 = 0.5 + y0 / (2 * radius)
            u1 = 0.5 + x1 / (2 * radius)
            v1 = 0.5 + y1 / (2 * radius)

            tris.append(bot_center + bot_normal + list(color) + [0.5, 0.5])
            tris.append(p1 + bot_normal + list(color) + [u1, v1])
            tris.append(p0 + bot_normal + list(color) + [u0, v0])

        self.vertices = np.array(tris, dtype=np.float32)
        self.indices = np.zeros(0)

    def draw(self):
        self.vao.bind()
        # TODO 1.1 is here, switch from vbo to ebo
        self.vbo.draw()
        self.vao.unbind()

    def initialize(self):
        """
        Remember to bind VAO before this initialization. If VAO is not bind, program might throw an error
        in systems that don't enable a default VAO after GLProgram compilation
        """
        self.vao.bind()
        self.vbo.setBuffer(self.vertices, 11)
        self.ebo.setBuffer(self.indices)

        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("aPos"),
                                  stride=11, offset=0, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("aNormal"),
                                  stride=11, offset=3, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("aColor"),
                                  stride=11, offset=6, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("aTexture"),
                                  stride=11, offset=9, attribSize=2)
        # TODO/BONUS 6.1 is at here, you need to set attribPointer for texture coordinates
        # you should check the corresponding variable name in GLProgram and set the pointer
        self.vao.unbind()
