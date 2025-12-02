"""
Define torus here.
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

##### TODO 6/BONUS 6: Texture Mapping
# Requirements:
#   1. Set up each object's vertex texture coordinates(2D) to the self.vertices 9:11 columns
#   (i.e. the last two columns). Tell OpenGL how to interpret these two columns:
#   you need to set up attribPointer in the Displayable object's initialize method.
#   2. Generate texture coordinates for the torus and sphere. Use “./assets/marble.jpg” for the torus and
#   “./assets/earth.jpg” for the sphere as the texture image.
#   There should be no seams in the resulting texture-mapped model.

class DisplayableTorus(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    # stores current torus's information, read-only
    nsides = 0
    rings = 0
    innerRadius = 0
    outerRadius = 0
    color = None

    vertices = None
    indices = None

    def __init__(self, shaderProg, innerRadius=0.25, outerRadius=0.5, nsides=36, rings=36, color=ColorType.SOFTBLUE):
        super(DisplayableTorus, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(innerRadius, outerRadius, nsides, rings, color)

    def generate(self, innerRadius=0.25, outerRadius=0.5, nsides=36, rings=36, color=ColorType.SOFTBLUE):
        self.innerRadius = innerRadius
        self.outerRadius = outerRadius
        self.nsides = nsides
        self.rings = rings
        self.color = color

        R = outerRadius
        r = innerRadius

        # angles
        ringAngles = np.linspace(0, 2*np.pi, rings + 1)
        sideAngles = np.linspace(0, 2*np.pi, nsides + 1)
        v_data = []

        for i, theta in enumerate(ringAngles):
            for j, phi in enumerate(sideAngles):

                # position
                cosPhi = np.cos(phi)
                sinPhi = np.sin(phi)
                cosTheta = np.cos(theta)
                sinTheta = np.sin(theta)

                x = (R + r * cosPhi) * cosTheta
                y = (R + r * cosPhi) * sinTheta
                z =  r * sinPhi
                pos = [x, y, z]

                # normal
                nx = cosPhi * cosTheta
                ny = cosPhi * sinTheta
                nz = sinPhi
                normal = [nx, ny, nz]

                # uv mapping
                u = i / rings
                v = j / nsides
                uv = [u, v]

                v_data.append(pos + normal + list(color) + uv)
        self.vertices = np.array(v_data, dtype=np.float32)

        indexes = []
        def idx(st, sl):
            return st * (nsides + 1) + sl 
        
        for st in range(rings):
            for sl in range(nsides):
                sl_next = sl + 1
                st_next = st + 1

                indexes.append(idx(st, sl))
                indexes.append(idx(st_next, sl))
                indexes.append(idx(st, sl_next))

                indexes.append(idx(st_next, sl))
                indexes.append(idx(st_next, sl_next))
                indexes.append(idx(st, sl_next))
        self.indices = np.array(indexes)

    def draw(self):
        self.vao.bind()
        # TODO 1.1 is here, switch from vbo to ebo
        self.ebo.draw()
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
