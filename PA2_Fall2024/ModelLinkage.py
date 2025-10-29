"""
Model our creature and wrap it in one class.
First version on 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1

----------------------------------

Modified by Daniel Scrivener 09/2023
"""

from Component import Component
from Point import Point
import ColorType as Ct
from Shapes import *
import numpy as np


class ModelLinkage(Component):
    """
    Define our linkage model
    """

    ##### TODO 2: Model the Creature
    # Build the class(es) of objects that could utilize your built geometric object/combination classes. E.g., you could define
    # three instances of the cyclinder trunk class and link them together to be the "limb" class of your creature. 
    #
    # In order to simplify the process of constructing your model, the rotational origin of each Shape has been offset by -1/2 * dz,
    # where dz is the total length of the shape along its z-axis. In other words, the rotational origin lies along the smallest 
    # local z-value rather than being at the translational origin, or the object's true center. 
    # 
    # This allows Shapes to rotate "at the joint" when chained together, much like segments of a limb. 
    #
    # In general, you should construct each component such that it is longest in its local z-direction: 
    # otherwise, rotations may not behave as expected.
    #
    # Please see Blackboard for an illustration of how this behavior works.

    components = None
    contextParent = None

    # TOROKO IF SHE LOCKED IN
    def __init__(self, parent, position, shaderProg, display_obj=None):
        super().__init__(position, display_obj)
        self.contextParent = parent

        # linkageLength = 0.5
        # link1 = Cube(Point((0, 0, 0)), shaderProg, [0.2, 0.2, linkageLength], Ct.DARKORANGE1)
        # link2 = Cube(Point((0, 0, linkageLength)), shaderProg, [0.2, 0.2, linkageLength], Ct.DARKORANGE2)
        # link3 = Cube(Point((0, 0, linkageLength)), shaderProg, [0.2, 0.2, linkageLength], Ct.DARKORANGE3)
        # link4 = Cube(Point((0, 0, linkageLength)), shaderProg, [0.2, 0.2, linkageLength], Ct.DARKORANGE4)

        # self.addChild(link1)
        # link1.addChild(link2)
        # link2.addChild(link3)
        # link3.addChild(link4)
        

        # self.componentList = [link1, link2, link3, link4]
        # self.componentDict = {
        #     "link1": link1,
        #     "link2": link2,
        #     "link3": link3,
        #     "link4": link4
        # }

        body = Cube(Point((0, 0, -1)), shaderProg, [0.6, 0.7, 0.3], Ct.GREEN)
        neck = Cube(Point((0, 0.4, 0)), shaderProg, [0.5, 0.2, 0.25], Ct.GREEN)
        head = Cube(Point((0, 0.3, 0)), shaderProg, [0.8, 0.5, 0.3], Ct.WHITE)
        hat = Cone(Point((0, 0.2, 0.2)), shaderProg, [0.1, 0.1, 0.2], Ct.BLUE)
        propeller = Cube(Point((0, 0, 0.15)), shaderProg, [0.1, 0.4, 0.05], Ct.YELLOW)
        leftEar = Cube(Point((-0.45, 0, 0)), shaderProg, [0.2, 0.4, 0.2], Ct.BLACK)
        rightEar = Cube(Point((0.45, 0, 0)), shaderProg, [0.2, 0.4, 0.2], Ct.BLACK)

        leftArmJoint1 = Sphere(Point((-0.4, 0.2, 0)), shaderProg, [0.01, 0.01, 0.01], Ct.BLACK)
        leftArmBlock1 = Cube(Point((0, -0.1, 0)), shaderProg, [0.2, 0.5, 0.2], Ct.BLACK)
        rightArmJoint1 = Sphere(Point((0.4, 0.2, 0)), shaderProg, [0.01, 0.01, 0.01], Ct.BLACK)
        rightArmBlock1 = Cube(Point((0, 0, 0)), shaderProg, [0.2, 0.3, 0.2], Ct.BLACK)
        rightArmJoint2 = Sphere(Point((0, -0.15, 0)), shaderProg, [0.01, 0.01, 0.01], Ct.BLACK)
        rightArmBlock2 = Cube(Point((0, -0.07, 0)), shaderProg, [0.1, 0.14, 0.1], Ct.GRAY)
        rightArmJoint3 = Sphere(Point((0, -0.05, 0)), shaderProg, [0.01, 0.01, 0.01], Ct.BLACK)
        rightArmBlock3 = Cube(Point((0, -0.07, 0)), shaderProg, [0.1, 0.14, 0.1], Ct.YELLOW)
    
        leftFoot = Cube(Point((-0.2, -0.45, 0.05)), shaderProg, [0.2, 0.2, 0.4], Ct.BLACK)
        rightFoot = Cube(Point((0.2, -0.45, 0.05)), shaderProg, [0.2, 0.2, 0.4], Ct.BLACK)

        leftEye = Sphere(Point((-0.2, 0, 0.1)), shaderProg, [0.1, 0.1, 0.1], Ct.BLACK)
        rightEye = Sphere(Point((0.2, 0, 0.1)), shaderProg, [0.1, 0.1, 0.1], Ct.BLACK)

        self.addChild(body)
        body.addChild(neck)
        neck.addChild(head)
        head.addChild(hat)
        hat.addChild(propeller)
        head.addChild(leftEar)
        head.addChild(rightEar)

        body.addChild(leftArmJoint1)
        leftArmJoint1.addChild(leftArmBlock1)
        body.addChild(rightArmJoint1)
        rightArmJoint1.addChild(rightArmBlock1)
        rightArmBlock1.addChild(rightArmJoint2)
        rightArmJoint2.addChild(rightArmBlock2)
        rightArmBlock2.addChild(rightArmJoint3)
        rightArmJoint3.addChild(rightArmBlock3)

        body.addChild(leftFoot)
        body.addChild(rightFoot)

        head.addChild(leftEye)
        head.addChild(rightEye)

        self.componentList = [body, neck, head, hat, leftEar, rightEar, leftArmJoint1, rightArmJoint1, rightArmJoint2, rightArmJoint3, leftFoot, rightFoot]
        self.componentDict = {
            "body": body,
            "neck": neck,
            "head": head,
            "hat": hat,
            "leftEar": leftEar,
            "rightEar": rightEar,
            "leftArm1": leftArmJoint1,
            "rightArm1": rightArmJoint1,
            "rightArm2": rightArmJoint2,
            "rightArm3": rightArmJoint3,
            "leftFoot": leftFoot,
            "rightFoot": rightFoot,
        }


        ##### TODO 4: Define creature's joint behavior
        # Requirements:
        #   1. Set a reasonable rotation range for each joint,
        #      so that creature won't intersect itself or bend in unnatural ways
        #   2. Orientation of joint rotations for the left and right parts should mirror each other.
        neck.setRotateExtent(self.uAxis, -8, 12)
        neck.setRotateExtent(self.vAxis, -8, 8)
        neck.setRotateExtent(self.wAxis, -8, 8)

        head.setRotateExtent(self.uAxis, 0, 0)
        head.setRotateExtent(self.vAxis, 0, 0)
        head.setRotateExtent(self.wAxis, 0, 0)

        leftArmJoint1.setRotateExtent(self.uAxis, -120, 30)
        leftArmJoint1.setRotateExtent(self.vAxis, 0, 0)
        leftArmJoint1.setRotateExtent(self.wAxis, -90, 0)

        rightArmJoint1.setRotateExtent(self.uAxis, -120, 30)
        rightArmJoint1.setRotateExtent(self.vAxis, 0, 0)
        rightArmJoint1.setRotateExtent(self.wAxis, 0, 90)
        rightArmJoint2.setRotateExtent(self.uAxis, -30, 0)
        rightArmJoint2.setRotateExtent(self.vAxis, 0, 0)
        rightArmJoint2.setRotateExtent(self.wAxis, -30, 0)
        rightArmJoint3.setRotateExtent(self.uAxis, -30, 0)
        rightArmJoint3.setRotateExtent(self.vAxis, 0, 0)
        rightArmJoint3.setRotateExtent(self.wAxis, -30, 0)

        leftFoot.setRotateExtent(self.uAxis, -5, 15)
        leftFoot.setRotateExtent(self.vAxis, -15, 15)
        leftFoot.setRotateExtent(self.wAxis, 0, 0)
        rightFoot.setRotateExtent(self.uAxis, -5, 15)
        rightFoot.setRotateExtent(self.vAxis, -15, 15)
        rightFoot.setRotateExtent(self.wAxis, 0, 0)

        leftEar.setRotateExtent(self.uAxis, 0, 0)
        leftEar.setRotateExtent(self.vAxis, 0, 0)
        leftEar.setRotateExtent(self.wAxis, -45, 0)
        rightEar.setRotateExtent(self.uAxis, 0, 0)
        rightEar.setRotateExtent(self.vAxis, 0, 0)
        rightEar.setRotateExtent(self.wAxis, 0, 45)

        hat.setRotateExtent(self.uAxis, -90, -90)
        hat.setRotateExtent(self.wAxis, 0, 0)