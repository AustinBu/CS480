import math
import random

import numpy as np

import ColorType
from Scene import Scene
from Component import Component
from Light import Light
from Material import Material
from Point import Point
import GLUtility

from DisplayableCube import DisplayableCube
from DisplayableEllipsoid import DisplayableEllipsoid
from DisplayableSphere import DisplayableSphere
from DisplayableCylinder import DisplayableCylinder
from DisplayableTorus import DisplayableTorus

class SceneThree(Scene):
    lights = None
    lightCubes = None
    shaderProg = None
    glutility = None


    def __init__(self, shaderProg):
        super().__init__(Point((0, 0, 0)))
        self.party = 0
        self.shaderProg = shaderProg
        self.glutility = GLUtility.GLUtility()

        # ambient lighting contribution from the scene
        self.sceneAmbient = np.array([1, 1, 1])

        cube = Component(Point((-0.8, 0, -0.8)), DisplayableCube(shaderProg, 1.0))
        m1 = Material(np.array((0.0, 0.05, 0.1, 1.0)), np.array((0, 0.3, 0.6, 1)),
                      np.array((0, 0.3, 0.6, 1.0)), 64)
        cube.setMaterial(m1)
        cube.renderingRouting = "lighting"
        self.addChild(cube)

        torus = Component(Point((0.8, 0, -0.8)), DisplayableTorus(shaderProg, 0.15, 0.3, 36, 36, ColorType.SOFTRED))
        m2 = Material(np.array((0.1, 0., 0., 1.0)), np.array((0.3, 0.05, 0.05, 1)),
                      np.array((0.3, 0.3, 0.3, 1.0)), 64)
        torus.setMaterial(m2)
        torus.renderingRouting = "lighting"
        
        torus.rotate(90, torus.uAxis)
        self.addChild(torus)


        ellipsoid = Component(Point((0.8, 0, 0.8)), DisplayableEllipsoid(shaderProg, color=ColorType.SOFTGREEN))
        m3 = Material(np.array((0.0, 0.1, 0.05, 1.0)), np.array((0, 0.6, 0.3, 1)),
                      np.array((0, 0.2, 0.1, 1)), 4)
        ellipsoid.setMaterial(m3)
        ellipsoid.renderingRouting = "lighting"
        self.addChild(ellipsoid)

        cylinder = Component(Point((-0.8, 0, 0.8)), DisplayableCylinder(shaderProg, color=ColorType.ORANGE))
        m4 = Material(np.array((0.1, 0.02, 0.01, 1.0)), np.array((0.3, 0.2, 0.1, 1)),
                      np.array((0.3, 0.2, 0.1, 1.0)), 64)
        cylinder.setMaterial(m4)
        cylinder.renderingRouting = "lighting"
        self.addChild(cylinder)

        plane = Component(Point((0, -2., 0.)), DisplayableCube(shaderProg, 5, 0.1, 5, ColorType.GRAY))
        m5 = Material(np.array((0.1, 0.1, 0.1, 1.0)), np.array((0.2, 0.2, 0.2, 1)),
                      np.array((0.2, 0.2, 0.2, 1.0)), 64)
        plane.setMaterial(m5)
        plane.renderingRouting = "lighting"
        self.addChild(plane)

        l0_pos = np.array([0., 2.0, 0.])
        l0 = Light(l0_pos, np.array([*ColorType.WHITE, 1.0]), infiniteDirection=np.array((0.,-1.,0.)))
        # l0 = Light(l0_pos, np.array([0, 0, 0, 1.0]), spotDirection=np.array((0.,-1.,0.)), spotAngleLimit=30*np.pi/180)
        lightCube0 = Component(Point(l0_pos), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.WHITE))
        lightCube0.renderingRouting = "vertex"

        l1_pos = np.array([-2., 0., 0.])
        l1 = Light(l1_pos, np.array([*ColorType.RED, 1.0]), infiniteDirection=np.array((1.,0.,0.)))
        # l1 = Light(l1_pos, np.array([0, 0, 0, 1.0]))
        lightCube1 = Component(Point(l1_pos), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.RED))
        lightCube1.renderingRouting = "vertex"

        l2_pos = np.array([2., 0., 0.])
        l2 = Light(l2_pos, np.array([*ColorType.BLUE, 1.0]), infiniteDirection=np.array((-1.,0.,0.)))
        # l2 = Light(l2_pos, np.array([0, 0, 0, 1.0]))
        lightCube2 = Component(Point(l2_pos), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.BLUE))
        lightCube2.renderingRouting = "vertex"

        self.addChild(lightCube0)
        self.addChild(lightCube1)
        self.addChild(lightCube2)
        self.lights = [l0, l1, l2]
        self.toggles = [True, True, True]
        self.lightCubes = [lightCube0, lightCube1, lightCube2]

        self.shapes = [cube, torus, ellipsoid, cylinder]

    def animationUpdate(self):
        move = np.array([-0.01, 0, -0.01])
        self.party += 1
        if self.party > 75:
            move *= -1
        if self.party > 150:
            self.party = 0
        counter = 0
        for c in self.shapes:
            c.setCurrentPosition(Point(c.currentPos.getCoords() + move))
            if counter % 2 == 0:
                move[0] *= -1
            else:
                move [2] *= -1
            counter += 1
        pass

    def toggleLight(self, index):
        self.shaderProg.clearAllLights()
        self.shaderProg.setVec3("sceneAmbient", self.sceneAmbient)
        self.toggles[index] = not self.toggles[index]
        for i, v in enumerate(self.lights):
            if self.toggles[i]:
                self.shaderProg.setLight(i, v)

    def initialize(self):
        self.shaderProg.clearAllLights()
        self.shaderProg.setVec3("sceneAmbient", self.sceneAmbient)
        for i, v in enumerate(self.lights):
            self.shaderProg.setLight(i, v)
        super().initialize()
