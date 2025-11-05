'''
Define Our class which is stores collision detection and environment information here
Created on Nov 1, 2018

:author: micou(Zezhou Sun)
:version: 2021.1.1

modified by Daniel Scrivener 08/2022
'''

import math
import Component
from ModelTank import Tank
from Point import Point
from Quaternion import Quaternion
import numpy as np


class EnvironmentObject:
    """
    Define properties and interface for a object in our environment
    """
    env_obj_list = []  # list<Environment>
    item_id = 0
    species_id = 0

    bound_radius = None
    bound_center = Point((0,0,0))

    def addCollisionObj(self, a):
        """
        Add an environment object for this creature to interact with
        """
        if isinstance(a, EnvironmentObject):
            self.env_obj_list.append(a)

    def rmCollisionObj(self, a):
        """
        Remove an environment object for this creature to interact with
        """
        if isinstance(a, EnvironmentObject):
            self.env_obj_list.remove(a)

    def animationUpdate(self):
        """
        Perform the next frame of this environment object's animation.
        """
        self.update()

    def stepForward(self):
        """
        Have this environment object take a step forward in the simulation.
        """
        return

    ##### TODO 4: Eyes on the road!
        # Requirements:
        #   1. Creatures should face in the direction they are moving. For instance, a fish should be facing the
        #   direction in which it swims. Remember that we require your creatures to be movable in 3 dimensions,
        #   so they should be able to face any direction in 3D space.
            
    def rotateDirection(self, v1):
        """
        change this environment object's orientation to v1.
        :param v1: targed facing direction
        :type v1: Point
        """
        v_initial = np.array([0.0, 0.0, 1.0])
        v_target = np.array(v1) 
        
        if np.linalg.norm(v_target) < 1e-6:
             self.setPostRotation(np.identity(4))
             return

        v_target_norm = v_target / np.linalg.norm(v_target)
        k = np.cross(v_initial, v_target_norm)
        axis_norm = np.linalg.norm(k)

        cos_angle = np.dot(v_initial, v_target_norm)
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        angle = math.acos(cos_angle)

        if axis_norm < 1e-6:
            if angle < 1e-6:
                rotation_matrix_4x4 = np.identity(4)
            else:
                rotation_axis = np.array([1.0, 0.0, 0.0])
                
                q_rot = Quaternion(0.0, rotation_axis[0], rotation_axis[1], rotation_axis[2])
                q_rot.normalize() 
                rotation_matrix_4x4 = q_rot.toMatrix()
        else:
            rotation_axis = k / axis_norm
            half_angle = angle / 2.0
            s_comp = math.cos(half_angle)
            v_comp_scale = math.sin(half_angle)
            
            q_rot = Quaternion(
                s_comp,
                rotation_axis[0] * v_comp_scale,
                rotation_axis[1] * v_comp_scale,
                rotation_axis[2] * v_comp_scale
            )
            q_rot.normalize()

            rotation_matrix_4x4 = q_rot.toMatrix()
        self.setPostRotation(rotation_matrix_4x4)
        
    def checkCollision(self, other_obj):
        """
        Check for collision using bounding spheres.
        :param other_obj: Another EnvironmentObject instance
        :return: True if collision occurred, False otherwise.
        """
        if isinstance(other_obj, Tank):
            return False
        center_to_center = other_obj.currentPos.coords - self.currentPos.coords
        distance = np.linalg.norm(center_to_center)
        min_distance = self.bound_radius + other_obj.bound_radius
        return distance < min_distance
    
    def reflectDirection(self, other_obj):
        """
        Calculate the reflection vector for the 'self' object upon collision with 'other_obj'.
        This assumes the reflection happens off a plane tangent to the collision point.
        """
        collision_normal = other_obj.currentPos.coords - self.currentPos.coords
        
        if np.linalg.norm(collision_normal) < 1e-6:
            return -self.direction

        collision_normal = collision_normal / np.linalg.norm(collision_normal)
        D = self.direction
        N = collision_normal
        
        dot_product = np.dot(D, N)
        reflection = D - 2 * dot_product * N
        
        return reflection / np.linalg.norm(reflection)
    
    def calculatePotentialForce(self, env_obj_list):
        """
        Calculate the net force vector from all other objects based on potential fields.
        :param env_obj_list: list of all EnvironmentObject instances (creatures)
        :return: a 3D numpy array representing the net force
        """
        net_force = np.array([0.0, 0.0, 0.0])
        
        PREY_FLEE_STRENGTH = 0.05
        PREDATOR_CHASE_STRENGTH = 0.04
        INFLUENCE_RADIUS = 3.0

        for other in env_obj_list:
            if other is self:
                continue

            delta_pos = other.currentPos.coords - self.currentPos.coords
            distance = np.linalg.norm(delta_pos)
            
            if distance > INFLUENCE_RADIUS or distance < 1e-6:
                continue
                
            direction_unit = delta_pos / distance
            potential_scale = 1.0 / (distance * distance)

            if self.species_id == 1: 
                if other.species_id == 2:
                    force = -direction_unit * PREY_FLEE_STRENGTH * potential_scale
                    net_force += force

            elif self.species_id == 2:
                if other.species_id == 1:
                    force = -direction_unit * PREDATOR_CHASE_STRENGTH * potential_scale
                    net_force += force
        return net_force