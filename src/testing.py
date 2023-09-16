# Adapted from Josh Campbell by Marshall Saltz
# Date: 12-25-2022

#!/usr/bin/python3
import pybullet as p
import matplotlib.pyplot as plt
import time
import pybullet_data
import os
import json
import glob
import math
#from math import pi
import random
import csv
from addict import Dict
import numpy as np

class sim_tester():
    """Simulator class to test different hands in."""

    def __init__(self, gripper_name, gripper_loc, rob_dic, coords0, coords1):
        """Initialize the sim_tester class.

        Args:
            gripper_name (str): The name of the gripper to be pulled into the simulator enviroment
            gripper_loc (str): The location of the top hand directory in the output directory
        """
        self.gripper_name = gripper_name
        self.gripper_loc = gripper_loc
        self.coo0 = coords0
        self.coo1 = coords1
        self.directory = os.path.dirname(__file__)
    
    """
    The testing function. Uses user debug to provide a visual of the coordinate points.
    Uses resetJointState to first add bias in hand position then for faster solving
    """
    def main(self, generation):
        co0, co1 = self.coo0, self.coo1
        physicsClient = p.connect(p.DIRECT)    #or GUI for visual (slower)
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING,0)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
        p.setGravity(0, 0, 0)
        LinkId = []
        reachedL = []
        reachedR = []
        nr_R = []
        nr_L = []
        Rcount = 0
        Lcount = 0
        gripper_vals = Dict()
        cubeStartPos = [0, 0, 1]
        cubeStartOrientation = p.getQuaternionFromEuler([0, 0, 0])

        boxId = p.loadURDF(f"{self.gripper_loc}/{self.gripper_name}.urdf", useFixedBase=1, flags=p.URDF_USE_SELF_COLLISION_INCLUDE_PARENT) 
        gripper_vals.name = self.gripper_name
        gripper = boxId

          
        p.resetDebugVisualizerCamera(cameraDistance=.2, cameraYaw=180, cameraPitch=-91, cameraTargetPosition=[0, 0.1, 0.1])
                    
        p.changeDynamics(gripper, 0, jointLowerLimit=((math.pi)/4), jointUpperLimit=((5*math.pi)/4))
        p.changeDynamics(gripper, 3, jointLowerLimit=((3*math.pi)/4), jointUpperLimit=((7*math.pi)/4))
        p.changeDynamics(gripper, 1, jointLowerLimit=-(math.pi/2), jointUpperLimit=(math.pi/2))
        p.changeDynamics(gripper, 4, jointLowerLimit=-(math.pi/2), jointUpperLimit=(math.pi/2))
        list_of_points_1 = []
        list_of_points_0 = []
        

        for i in range(len(co0)):
            list_of_points_0.append(p.addUserDebugPoints([co0[i]], [[1, 0, 0]]))
            
            list_of_points_1.append(p.addUserDebugPoints([co1[i]], [[1, 0, 0]]))
        
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING,1)

        for i in range(len(co0)):
                         
            p.resetJointState(gripper, 0, targetValue=((5*math.pi)/4))
            p.resetJointState(gripper, 1, targetValue=(math.pi/2))
            
            p.resetJointState(gripper, 3, targetValue=((3*math.pi)/4))
            p.resetJointState(gripper, 4, targetValue=-(math.pi/2))
            
            idealJointPoses1 = p.calculateInverseKinematics(gripper, 5, co1[i], maxNumIterations=3000)
            idealJointPoses0 = p.calculateInverseKinematics(gripper, 2, co0[i], maxNumIterations=3000)
             
            p.resetJointState(gripper, 0, targetValue=idealJointPoses0[0])
            p.resetJointState(gripper, 1, targetValue=idealJointPoses0[1])
            p.resetJointState(gripper, 2, targetValue=idealJointPoses0[2])
            p.resetJointState(gripper, 3, targetValue=idealJointPoses1[3])
            p.resetJointState(gripper, 4, targetValue=idealJointPoses1[4])
            p.resetJointState(gripper, 5, targetValue=idealJointPoses1[5])
            worldPos = p.getLinkStates(gripper, [2, 5], computeForwardKinematics=1)
            joint_axis = []
            nums = []
            p.performCollisionDetection()
            add = 0
            for links in range(p.getNumJoints(gripper)):
                num = p.getAABB(gripper, links)
                nums.append(p.getOverlappingObjects(num[0], num[1]))
                add = add + len(nums[links])   
            offset_val = 3
            
            world_pos_0_x = round(worldPos[0][0][0], offset_val)
            world_pos_0_y = round(worldPos[0][0][1], offset_val)
            world_pos_1_x = round(worldPos[1][0][0], offset_val)
            world_pos_1_y = round(worldPos[1][0][1], offset_val)
            
            point_0_x = round(co0[i][0], offset_val)
            point_0_y = round(co0[i][1], offset_val)
            point_1_x = round(co1[i][0], offset_val)
            point_1_y = round(co1[i][1], offset_val)
            
            if world_pos_0_x == point_0_x and world_pos_0_y == point_0_y and world_pos_1_x == point_1_x and world_pos_1_y == point_1_y and add <= 16:
                reachedR.append((point_0_x, point_0_y))
                reachedL.append((point_1_x, point_1_y))
                p.removeUserDebugItem(list_of_points_0[i])
                p.removeUserDebugItem(list_of_points_1[i])
                p.addUserDebugPoints([co0[i]], [[0.016, 0.96, 0.99]])
                p.addUserDebugPoints([co1[i]], [[0.016, 0.96, 0.99]])
                Rcount = Rcount + 1 
                Lcount = Lcount + 1            
            else:
                nr_R.append((point_0_x, point_0_y))
                nr_L.append((point_1_x, point_1_y))
            p.stepSimulation()
            nums.clear()
            time.sleep(1. / 240.)

        p.disconnect()
        success = (Lcount + Rcount) / (len(co0) * 2)
        gripper_vals.finger_0.reached = reachedR
        gripper_vals.finger_1.reached = reachedL
        gripper_vals.finger_0.not_reached = nr_R
        gripper_vals.finger_1.not_reached = nr_L
        
        with open(f"../points/{self.gripper_name}.json", "w") as f:
            new_json = ""
            new_json += json.dumps(gripper_vals, indent=4)
            f.write(new_json)
        f.close()
        gripper_vals.clear()
        
        return (success, str(self.gripper_name)+".json")           


def read_json(file_loc):
    """Read contents of a given json file.

    Args:
        file_loc (str): Full path to the json file including the file name.

    Returns:
        dictionary: dictionary that contains the content from the json.
    """
    with open(file_loc, "r") as read_file:
        file_contents = json.load(read_file)
    return file_contents
