"""
Model our creature and wrap it in one class
First version at 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1

Modified by Daniel Scrivener 08/2022
"""
import random
import numpy as np
from Component import Component
from Shapes import Cube, Sphere, Cone, Cylinder
from Point import Point
import ColorType as Ct
from EnvironmentObject import EnvironmentObject

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

##### TODO 1: Construct your two different creatures
# Requirements:
#   1. For the basic parts of your creatures, feel free to use routines provided with the previous assignment.
#   You are also free to create your own basic parts, but they must be polyhedral (solid).
#   2. The creatures you design should have moving linkages of the basic parts: legs, arms, wings, antennae,
#   fins, tentacles, etc.
#   3. Model requirements:
#         1. Predator: At least one (1) creature. Should have at least two moving parts in addition to the main body
#         2. Prey: At least two (2) creatures. The two prey can be instances of the same design. Should have at
#         least one moving part.
#         3. The predator and prey should have distinguishable different colors.
#         4. You are welcome to reuse your PA2 creature in this assignment.

class Prey(Component, EnvironmentObject):
    """
    A Linkage with animation enabled and is defined as an object in environment
    """
    components = None
    rotation_speed = None
    translation_speed = None
    step_size = 0.01

    def __init__(self, parent, position, shaderProg):
        self.parent = parent
        super(Prey, self).__init__(position)
        direction = np.random.random(3)
        # direction = [1, 0, 0]
        self.direction = direction / np.linalg.norm(direction)

        self.head = Sphere(Point((0, 0, 0)), shaderProg, [0.2, 0.1, 0.1], Ct.BLACK)
        self.eyeL = Sphere(Point((0.2, 0.1, 0.05)), shaderProg, [0.05, 0.05, 0.05], Ct.WHITE)
        self.head.addChild(self.eyeL)

        self.eyeR = Sphere(Point((0.2, 0.1, -0.05)), shaderProg, [0.05, 0.05, 0.05], Ct.WHITE)
        self.head.addChild(self.eyeR)
        
        arm1 = ModelArm(parent, Point((0, 0, 0)), shaderProg, 0.1)
        arm2 = ModelArm(parent, Point((0, 0, 0)), shaderProg, 0.1)
        arm2.setDefaultAngle(180, arm2.uAxis)
        arm2.setDefaultAngle(180, arm2.vAxis)

        self.components = arm1.components + arm2.components
        self.head = self.head
        self.addChild(self.head)
        self.head.addChild(arm1)
        self.head.addChild(arm2)

        self.rotation_speed = []
        for comp in self.components:

            comp.setRotateExtent(comp.uAxis, 0, 35)
            comp.setRotateExtent(comp.vAxis, -45, 45)
            comp.setRotateExtent(comp.wAxis, -45, 45)
            self.rotation_speed.append([0.5, 0, 0])

        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 0.2
        self.species_id = 1

    def animationUpdate(self):
        for i, comp in enumerate(self.components):
            comp.rotate(self.rotation_speed[i][0], comp.uAxis)
            comp.rotate(self.rotation_speed[i][1], comp.vAxis)
            comp.rotate(self.rotation_speed[i][2], comp.wAxis)
            if comp.uAngle in comp.uRange:  # rotation reached the limit
                self.rotation_speed[i][0] *= -1
            if comp.vAngle in comp.vRange:
                self.rotation_speed[i][1] *= -1
            if comp.wAngle in comp.wRange:
                self.rotation_speed[i][2] *= -1

        self.update()

    def stepForward(self, components, tank_dimensions, vivarium):
        nextPos = self.currentPos.coords + (self.direction * self.step_size)
        potential_force = self.calculatePotentialForce(self.env_obj_list)
        new_direction_vector = self.direction + potential_force
        self.direction = new_direction_vector / np.linalg.norm(new_direction_vector)
        
        nextPos = self.currentPos.coords + (self.direction * self.step_size)
        for other in self.env_obj_list:
            if other is self or not isinstance(other, EnvironmentObject):
                continue
            
            if self.checkCollision(other):
                if other.species_id == 2:
                    self.parent.vivarium.delObjInTank(self) 
                    return
                
                elif other.species_id == 1:
                    self.direction = self.reflectDirection(other)
                    nextPos = self.currentPos.coords + (self.direction * self.step_size)
                    break
        for i in range(3):
            if (abs(nextPos[i]) + self.bound_radius) >= tank_dimensions[i] / 2:
                self.direction[i] *= -1
                nextPos[i] = self.currentPos.coords[i] + self.direction[i] * self.step_size
        self.rotateDirection(self.direction)
        self.setCurrentPosition(Point(nextPos))


class Predator(Component, EnvironmentObject):
    """
    Predator
    """
    components = None
    rotation_speed = [1, 0, 0]
    translation_speed = None
    step_size = 0.012

    def __init__(self, parent, position, shaderProg):
        super(Predator, self).__init__(position)
        direction = np.random.random(3)
        self.direction = direction / np.linalg.norm(direction)

        self.body = Sphere(Point((0, 0, 0)), shaderProg, [0.3, 0.2, 0.2], Ct.GREEN)
        self.addChild(self.body)

        self.head = Sphere(Point((0, 0.15, 0.25)), shaderProg, [0.15, 0.15, 0.15], Ct.GREEN)
        self.body.addChild(self.head)

        self.eyeL = Sphere(Point((0.07, 0.1, 0.05)), shaderProg, [0.05, 0.05, 0.05], Ct.WHITE)
        self.head.addChild(self.eyeL)

        self.eyeR = Sphere(Point((-0.07, 0.1, 0.05)), shaderProg, [0.05, 0.05, 0.05], Ct.WHITE)
        self.head.addChild(self.eyeR)

        self.legL_pivot = Sphere(Point((0.15, -0.1, -0.15)), shaderProg, [0.01, 0.01, 0.01])
        self.body.addChild(self.legL_pivot)
        self.legL = Cylinder(Point((0, 0, 0)), shaderProg, [0.05, 0.25, 0.05], Ct.DARKGREEN)
        self.legL_pivot.addChild(self.legL)

        self.legR_pivot = Sphere(Point((-0.15, -0.1, -0.15)), shaderProg, [0.01, 0.01, 0.01])
        self.body.addChild(self.legR_pivot)
        self.legR = Cylinder(Point((0, 0, 0)), shaderProg, [0.05, 0.25, 0.05], Ct.DARKGREEN)
        self.legR_pivot.addChild(self.legR)

        self.legL_pivot.setRotateExtent(self.legL.uAxis, -35, 35)
        self.legR_pivot.setRotateExtent(self.legR.uAxis, -35, 35)
        self.components = [self.legL_pivot, self.legR_pivot]

        self.body.default_vAngle = 90

        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 0.5
        self.species_id = 2

    def animationUpdate(self):
        for comp in self.components:
            comp.rotate(self.rotation_speed[0], comp.uAxis)
            if comp.uAngle in comp.uRange:
                self.rotation_speed[0] *= -1
        self.update()

    def stepForward(self, components, tank_dimensions, vivarium):
        potential_force = self.calculatePotentialForce(self.env_obj_list)
        new_direction_vector = self.direction + potential_force
        self.direction = new_direction_vector / np.linalg.norm(new_direction_vector)

        nextPos = self.currentPos.coords + (self.direction * self.step_size)
        for other in self.env_obj_list:
            if other is self or not isinstance(other, EnvironmentObject):
                continue

            if self.checkCollision(other):
                
                if other.species_id == 1:
                    self.step_size *= 1.05
                    self.step_size = min(self.step_size, 0.02)
                    break 
                
                elif other.species_id == 2:
                    self.direction = self.reflectDirection(other)
                    nextPos = self.currentPos.coords + (self.direction * self.step_size)
                    break
        nextPos = self.currentPos.coords + (self.direction * self.step_size)
        for i in range(3):
            if (abs(nextPos[i]) + self.bound_radius) >= tank_dimensions[i] / 2:
                self.direction[i] *= -1
                nextPos[i] = self.currentPos.coords[i] + self.direction[i] * self.step_size
        self.setCurrentPosition(Point(nextPos))
        self.rotateDirection(self.direction)

class ModelArm(Component):
    """
    Define our linkage model
    """

    components = None
    contextParent = None

    def __init__(self, parent, position, shaderProg, linkageLength=0.5, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        link1 = Cube(Point((0, 0, 0)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE1)
        link2 = Cube(Point((0, 0, linkageLength)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE2)
        link3 = Cube(Point((0, 0, linkageLength)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE3)
        link4 = Cube(Point((0, 0, linkageLength)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE4)

        self.addChild(link1)
        link1.addChild(link2)
        link2.addChild(link3)
        link3.addChild(link4)

        self.components = [link1, link2, link3, link4]
