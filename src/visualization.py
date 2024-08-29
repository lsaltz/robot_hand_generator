#!/usr/bin/python3
# Adapted from Josh Campbell by Marshall Saltz
"""
Pybullet Citation:
coumans2021,
author =   {Erwin Coumans and Yunfei Bai},
title =    {PyBullet, a Python module for physics simulation for games, robotics and machine learning},
howpublished = {url{http://pybullet.org}},
year = {2016--2021}
"""
from pybullet_utils import bullet_client as bc
import pybullet_data
import pybullet as p
import time
import pybullet_data
import os
import json
import math
from addict import Dict
import params
import numpy as np


class Visualize_Sim():
    """
    Class for visualizing gripper tests.
    To change which gripper is visualized, go to
    the bottom of this file and change the gripper name
    and run this file as the main one.
    Not really applicable to area test.
    """

    def __init__(self, name):
        """
        Initializes class.
        Parameters:
            name - gripper name (no file extension)
        """
        self.gripper_name = name
        self.data = self.get_data() # get gripper data
        self.center_pts = []    # gripper center points
        self.width = self.data.width    # palm width
        self.precision = 0.05   #visualization point separation


    def initialize_environment(self, loc):
        """
        Initializes pybullet environment.
        Parameters:
            loc - gripper location
        Returns:
            gripper - gripper ID
        """
        pc = p.connect(p.GUI)
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING,0)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
        p.setGravity(0, 0, 0)
        gripper = p.loadURDF(f"{loc}/{self.gripper_name}.urdf", useFixedBase=1, flags=p.URDF_USE_SELF_COLLISION_INCLUDE_PARENT) 
        p.resetDebugVisualizerCamera(cameraDistance=.2, cameraYaw=180, cameraPitch=-91, cameraTargetPosition=[0, 0.1, 0.1])
        cubeStartPos = [0, 0, 1]
        cubeStartOrientation = p.getQuaternionFromEuler([0, 0, 0])

        return gripper    
    
    
    def main(self):
        """
        Runs the simulation.
        """
        loc = f"../output/{self.gripper_name}/hand"
        gripper_id = self.initialize_environment(loc)
        self.coordinates()
        if params.flag == "angle":
            right_coords, left_coords = self.angles_coordinates()
        else:
            right_coords, left_coords = self.straight_coordinates()
        self.debug_pts(right_coords, left_coords)  
        for i in range(len(right_coords)):
            self.test_pts(right_coords[i], left_coords[i], gripper_id)
            p.stepSimulation()
            time.sleep(0.5)
        p.disconnect()  


    def coordinates(self):
        """
        Generates center coordinates for plotting.
        """
        val = self.precision
        x_out0, y_out0 = np.split(np.asarray(self.data.coord_space_right), 2, axis=1)
        x_out1, y_out1 = np.split(np.asarray(self.data.coord_space_left), 2, axis=1)
        top_x = max(max(self.data.coord_space_left, key=lambda point:point[0])[0], max(self.data.coord_space_right, key=lambda point:point[0])[0]) + params.trim_val
        bottom_x = min(min(self.data.coord_space_left, key=lambda point:point[0])[0], min(self.data.coord_space_right, key=lambda point:point[0])[0]) - params.trim_val
        top_y = max(max(self.data.coord_space_left, key=lambda point:point[1])[1], max(self.data.coord_space_right, key=lambda point:point[1])[1]) + params.trim_val
        bottom_y = min(min(self.data.coord_space_left, key=lambda point:point[1])[1], min(self.data.coord_space_right, key=lambda point:point[1])[1]) - params.trim_val
        row_length = top_x - bottom_x
        column_length = top_y - bottom_y
        row_points = int(row_length/val)
        column_points = int(column_length/val)
        
        self.center_pts = [[x, y] for x in np.linspace(bottom_x, top_x, num=row_points) for y in np.linspace(bottom_y, top_y, num=column_points)]
        self.center_pts = [pt for pt in self.center_pts if not ( pt[0] < self.width/2 and pt[0] > -abs(self.width)/2 and pt[1] <0) or (pt[0] < min(x_out0) or pt[0] > max(x_out0)) and (pt[0] < min(x_out1) or pt[0] > max(x_out1))
                           or (pt[1] < min(y_out0) or pt[1] > max(y_out0)) and (pt[1] < min(y_out1) or pt[1] > max(y_out1))]


    def debug_pts(self, r, l): 
        """
        Draws points in simulation.
        Parameters:
            r - right finger coordinates to attempt to reach
            l - left finger coordinates to attempt to reach
        """
        
        for i in range(len(self.data.coord_space_right)):
            p.addUserDebugPoints([[self.data.coord_space_right[i][0], self.data.coord_space_right[i][1], 0]], [[0, 0, 1]])

        for i in range(len(self.data.coord_space_left)):
            p.addUserDebugPoints([[self.data.coord_space_left[i][0], self.data.coord_space_left[i][1], 0]], [[0, 0, 1]])

        for i in range(len(self.center_pts)):
            p.addUserDebugPoints([[self.center_pts[i][0], self.center_pts[i][1], 0]], [[1, 0, 1]], pointSize=0.5)

        for i in range(len(r)):
            p.addUserDebugPoints([[r[i][0], r[i][1], 0]], [[1, 1, 1]], pointSize=5)
        for i in range(len(l)):
            p.addUserDebugPoints([[l[i][0], l[i][1], 0]], [[0, 1, 1]], pointSize=5)
        """
        if params.flag == "angle":
            self.plot_angles()
        elif params.flag == "straight":
            self.plot_straight()
        """
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING,1)

    
    def plot_angles(self):
        """
        Plots reached angle coordinates.
        """
        x = self.data.angle_data.centersx
        y = self.data.angle_data.centersy
        angles_coords = list(zip(x, y))
        for i in range(len(angles_coords)):
            p.addUserDebugPoints([[angles_coords[i][0], angles_coords[i][1], 0]], [[0, 1, 0]])


    def plot_straight(self):
        """
        Plots reached straight coordinates.
        """
        idx =  self.data.straight_data
        for pt in idx:
            p.addUserDebugPoints([[self.center_pts[pt][0], self.center_pts[pt][1], 0]], [[0, 1, 0]])

        
    def get_max_link(self):
        """
        Gets maximum link index for both fingers.
        Returns:
            max_link_0 - finger 0 max link index
            max_link_1 - finger 1 max link index
        """
        with open(f"../output/{self.gripper_name}/{self.gripper_name}.json", mode="r+") as f:
            dictionary = json.load(f)
            to_test = Dict(dictionary)
        f.close()
        
        max_link_0 = to_test.hand.finger_0.segment_qty - 1
        max_link_1 = max_link_0 + to_test.hand.finger_1.segment_qty

        return max_link_0, max_link_1
        

    def test_pts(self, co0, co1, gripper):
        """
        Runs through a GUI display of the gripper attempting to reach points.
        Parameters:
            co0 - right finger coordinates to reach
            co1 - left finger coordinates to reach
            gripper - gripper ID
        """
        max_link_0, max_link_1 = self.get_max_link()
        
        p.resetJointState(gripper, 0, targetValue=((5*math.pi)/4))
        p.resetJointState(gripper, 1, targetValue=(math.pi/2))
            
        p.resetJointState(gripper, max_link_0+1, targetValue=((3*math.pi)/4))
        p.resetJointState(gripper, max_link_0+2, targetValue=-(math.pi/2))
        
        idealJointPoses0 = p.calculateInverseKinematics(gripper, max_link_0, [co0[0], co0[1], 0], maxNumIterations=30000)
        idealJointPoses1 = p.calculateInverseKinematics(gripper, max_link_1, [co1[0], co1[1], 0], maxNumIterations=30000)
        
        for j in range(max_link_0+1):
            p.resetJointState(gripper, j, targetValue=idealJointPoses0[j])
                
        for j in range(max_link_0+1, max_link_1+1):
            p.resetJointState(gripper, j, targetValue=idealJointPoses1[j])
        
        
    def angles_coordinates(self):
        """
        Builds an array of coordinates to test for angles test.
        Returns:
            right_angles - right coordinates at n angles to check
            left_angles - left coordinates at n angles to check
        """
        val = self.precision    # precision at which to test (mm) distance between each coordinate 
        rad = params.radius  # radius of imaginary cube to reach
        right_coords = np.asarray(self.data.coord_space_right)
        left_coords = np.asarray(self.data.coord_space_left)
        # separated lists of outline coords
        x_out0, y_out0 = np.split(right_coords, 2, axis=1)  
        x_out1, y_out1 = np.split(left_coords, 2, axis=1)
        top_x = max(max(left_coords, key=lambda point:point[0])[0], max(right_coords, key=lambda point:point[0])[0]) + params.trim_val
        bottom_x = min(min(left_coords, key=lambda point:point[0])[0], min(right_coords, key=lambda point:point[0])[0]) - params.trim_val
        top_y = max(max(left_coords, key=lambda point:point[1])[1], max(right_coords, key=lambda point:point[1])[1]) + params.trim_val
        bottom_y = min(min(left_coords, key=lambda point:point[1])[1], min(right_coords, key=lambda point:point[1])[1]) - params.trim_val
        row_length = top_x - bottom_x
        column_length = top_y - bottom_y
        row_points = int(row_length/val)
        column_points = int(column_length/val)
        n = params.angles_count   # angles around the center point to check
        
        
        # generate coords around center_pt for right finger
        angles = np.linspace(0, 2*np.pi, n, endpoint=False) # angles list
        x0 = [(c[0] + (np.cos(a)*rad)) for c in self.center_pts for a in angles] 
        y0 = [(c[1] + (np.sin(a)*rad)) for c in self.center_pts for a in angles]
        coords0 = list(zip(x0, y0))

        # generate coords for left finger (shifted by 180 degrees)
        angles = [a+np.pi for a in angles]
        x1 = [(c[0] + (np.cos(a)*rad)) for c in self.center_pts for a in angles]
        y1 = [(c[1] + (np.sin(a)*rad))for c in self.center_pts for a in angles]
        coords1 = list(zip(x1, y1))
        
        right_angles = np.reshape(np.asarray(coords0), (-1, 2))
        left_angles = np.reshape(np.asarray(coords1), (-1, 2))

        return right_angles, left_angles

      
    def straight_coordinates(self):
        """
        Builds an array of coordinates to test for straight test.
        Returns:
            r - right coordinates [[x,y],...]
            l - left coordinates [[x,y],...]
        """
        val = self.precision
        right_coords = np.asarray(self.data.coord_space_right)
        left_coords = np.asarray(self.data.coord_space_left)
        x_out0, y_out0 = np.split(np.asarray(right_coords), 2, axis=1)
        x_out1, y_out1 = np.split(np.asarray(left_coords), 2, axis=1)
        top_x = max(max(left_coords, key=lambda point:point[0])[0], max(right_coords, key=lambda point:point[0])[0]) + params.trim_val
        bottom_x = min(min(left_coords, key=lambda point:point[0])[0], min(right_coords, key=lambda point:point[0])[0]) - params.trim_val
        top_y = max(max(left_coords, key=lambda point:point[1])[1], max(right_coords, key=lambda point:point[1])[1]) + params.trim_val
        bottom_y = min(min(left_coords, key=lambda point:point[1])[1], min(right_coords, key=lambda point:point[1])[1]) - params.trim_val
        row_length = top_x - bottom_x
        column_length = top_y - bottom_y
        row_points = int(row_length/val)
        column_points = int(column_length/val)
        rad = params.radius

        x0 = [(c[0] + rad) for c in self.center_pts]
        y0 = [c[1] for c in self.center_pts]
        coords0 = list(zip(x0, y0))
        
        x1 = [(c[0] - rad) for c in self.center_pts]
        y1 = [c[1] for c in self.center_pts]
        coords1 = list(zip(x1, y1))
        
        r = np.asarray(coords0)
        l = np.asarray(coords1)
        
        return r, l
    

    def get_data(self):
        """
        Gets points data of gripper.
        Returns:
            data - Dict() of received data
        """
        with open(f"../points/{self.gripper_name}.json", mode="r") as p:
            data = Dict(json.load(p))
            p.close()

        return data

        
if __name__ == "__main__":
    print("Input gripper name with no file extension: ")
    name = input()
    vs = Visualize_Sim(name)
    vs.main()