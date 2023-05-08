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
"""
TODO:
Chang
"""
class sim_tester():
    """Simulator class to test different hands in."""

    def __init__(self, gripper_name, gripper_loc, rob_dic):
        """Initialize the sim_tester class.

        Args:
            gripper_name (str): The name of the gripper to be pulled into the simulator enviroment
            gripper_loc (str): The location of the top hand directory in the output directory
        """
        self.gripper_name = gripper_name
        self.gripper_loc = gripper_loc
        self.rob_dic = rob_dic
        self.directory = os.path.dirname(__file__)
 

     
    def coordinate_array(self):
        finger_z = self.rob_dic.finger_z + 0.25
        val = 0.03    #distance between points being generated, has to be > valx2
        palm_z = self.rob_dic.palm_z
        total_height = self.rob_dic.total_height
        coords1 = []
        coords2 = []
        top = total_height + 0.25
        bottom = -abs(palm_z/2)
        bottom_point_right = ((0-finger_z), 0, (bottom))
        top_point_right = ((0-finger_z), 0, (top))
        bottom_point_left = (finger_z, 0, (bottom))
        top_point_left = (finger_z, 0, (top))
        area = (finger_z + finger_z) * top
        row_length = area/(top-bottom)
        column_length = area/(finger_z * 2)
        row_points = int(row_length/val)
        column_points = int(column_length/val)
        
        #size of cube, offset between fingers   
        #valx1 = 0
        xoffset = 0.125
        coords1 = [[x1, y1, 0] for x1 in np.linspace(-abs(total_height), finger_z, num=row_points) for y1 in np.linspace(bottom, finger_z, num=column_points)]
        coords2 = [[x2, y2, 0] for x2 in np.linspace(-abs(total_height) - xoffset, finger_z, num=row_points) for y2 in np.linspace(bottom, finger_z, num=column_points)]

        """
        while x1 > 0-finger_z: 
            x1 = ((finger_z+val)-valx1)    #x coordinate finger 0
            x2 = ((finger_z+val)-valx2)    #x coordinate finger 1
            valx1 = valx1 + val
            valx2 = valx2 + val
            valy1 = 0
            valy2 = 0
            y1 = bottom
            
            while y1 < top:

                y1 = ((bottom-val)+valy1)
                y2 = ((bottom-val)+valy2)
                valy1 = valy1 + val
                valy2 = valy2 + val
                coords1.append([x1, y1, 0])
                coords2.append([x2, y2, 0])
        """
        return coords1, coords2

    def main(self, generation):
        co0, co1 = self.coordinate_array()
        physicsClient = p.connect(p.DIRECT)
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING,0)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
        p.setGravity(0, 0, 0)
        LinkId = []
        reachedL = []
        reachedR = []
        Rcount = 0
        Lcount = 0
        gripper_vals = Dict()
        cubeStartPos = [0, 0, 1]
        cubeStartOrientation = p.getQuaternionFromEuler([0, 0, 0])

        boxId = p.loadURDF(f"{self.gripper_loc}/{self.gripper_name}.urdf", useFixedBase=1, flags=p.URDF_USE_SELF_COLLISION_INCLUDE_PARENT) 
        gripper_vals.name = self.gripper_name
        gripper = boxId

          
        p.resetDebugVisualizerCamera(cameraDistance=.2, cameraYaw=180, cameraPitch=-91, cameraTargetPosition=[0, 0.1, 0.1])
                    
       
        #p.changeDynamics(gripper, 3, jointLowerLimit=-1.5, jointUpperLimit=1.5)
        #p.changeDynamics(gripper, 0, jointLowerLimit=-1.5, jointUpperLimit=1.5)
        list_of_points_1 = []
        list_of_points_0 = []
        
        """
        1. get center of mass/collision parameters for each link
        2. set each joint to those mass/collision parameters
        """
        for i in range(len(co0)):
            list_of_points_0.append(p.addUserDebugPoints([co0[i]], [[1, 0, 0]]))
            
            list_of_points_1.append(p.addUserDebugPoints([co1[i]], [[1, 0, 0]]))
        
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING,1)

        for i in range(len(co0)):
            idealJointPoses1 = p.calculateInverseKinematics(gripper, 5, co1[i], maxNumIterations=3000)
            idealJointPoses0 = p.calculateInverseKinematics(gripper, 2, co0[i], maxNumIterations=3000)
                
            #p.setJointMotorControlArray(gripper, [0, 1, 2], p.POSITION_CONTROL, targetPositions=[idealJointPoses0[0], idealJointPoses0[1], idealJointPoses0[2]])
            #p.setJointMotorControlArray(gripper, [3, 4, 5], p.POSITION_CONTROL, targetPositions=[idealJointPoses1[3], idealJointPoses1[4], idealJointPoses1[5]])
            p.resetJointState(gripper, 0, targetValue=idealJointPoses0[0])
            p.resetJointState(gripper, 1, targetValue=idealJointPoses0[1])
            p.resetJointState(gripper, 2, targetValue=idealJointPoses0[2])
            p.resetJointState(gripper, 3, targetValue=idealJointPoses1[3])
            p.resetJointState(gripper, 4, targetValue=idealJointPoses1[4])
            p.resetJointState(gripper, 5, targetValue=idealJointPoses1[5])
            worldPos = p.getLinkStates(gripper, [2, 5], computeForwardKinematics=1)
            y = []
            x = []
            z = []
            joint_axis = []
            """
            distanceFromOrigin = []
            joint_length = 0.165/2

            
            distanceFromOrigin0 = sqrt(worldPos[0][0][0]**2 + worldPos[0][0][1]**2)
            distanceFromOrigin1 = sqrt(worldPos[1[0][0]**2 + worldPos[1][0][1]**2)
            distanceFromOrigin2 = sqrt(worldPos[2][0][0]**2 + worldPos[2][0][1]**2)
            distanceFromOrigin3 = sqrt(worldPos[3][0][0]**2 + worldPos[3][0][1]**2)
            distanceFromOrigin4 = sqrt(worldPos[4][0][0]**2 + worldPos[4][0][1]**2)
            distanceFromOrigin5 = sqrt(worldPos[5][0][0]**2 + worldPos[5][0][1]**2)
            
            for links in range(p.getNumJoints(gripper)):
                #distanceFromOrigin.append(math.sqrt(worldPos[links][0][0]**2 + worldPos[links][0][1]**2))
                x.append(worldPos[links][0][0])
                y.append(worldPos[links][0][1])
                for link2 in reversed(p.getNumJoints(gripper)):
                     if links != link2:
                         
                         if x[links] < x[link2] and y[links] < y[link2]:
                         elif x[links] < x[link2] and y[links > y[link2]:
                             p.changeDynamics(
                         elif x[links] > x[link2] and y[links] < y[link2]:
                         elif x[links] > x[link2] and y[links] > y[link2]:

                         
                
                
                """
            nums = []
            #constraintID = []
            #worldPosBase = p.getBasePositionAndOrientation(gripper)
            p.performCollisionDetection()
            add = 0
            for links in range(p.getNumJoints(gripper)):
                #joint_axis = p.getJointInfo(gripper, links)[14]
                #p.createConstraint(gripper, -1, 0, 0, JOINT_REVOLUTE, joint_axis[0], 
                worldPos1 = p.getLinkState(gripper, links, computeForwardKinematics=1)
               
                #x.append(worldPos1[links][0][0])
                #y.append(worldPos1[links][0][1])
                #z.append(worldPos1[links][0][2])
                #y.append(worldPos[links][0][1])
                
                num = p.getAABB(gripper, links)
                nums.append(p.getOverlappingObjects(num[0], num[1]))
                #constraintID.append(p.createConstraint(gripper, -1, gripper, links, p.JOINT_REVOLUTE, joint_axis, worldPosBase, worldPos1[links][0]))
                
                add = add + len(nums[links])
                #print(f"{links}: {nums}")
            #constraintID.clear()

            if (abs(worldPos[0][0][0]) <= abs(co0[i][0])+0.01 and abs(worldPos[0][0][0]) >= abs(co0[i][0])-0.01) and (abs(worldPos[0][0][1]) <= abs(co0[i][1])+0.01 and abs(worldPos[0][0][1]) >= abs(co0[i][1])-0.01) and (abs(worldPos[1][0][0]) <= abs(co1[i][0])+0.01 and abs(worldPos[1][0][0]) >= abs(co1[i][0])-0.01) and (abs(worldPos[1][0][1]) <= abs(co1[i][1])+0.01 and abs(worldPos[1][0][1]) >= abs(co1[i][1])-0.01) and (add <= 22):
                
                           
                reachedR.append((co0[i][0], co0[i][1]))
                reachedL.append((co1[i][0], co1[i][1]))
                p.removeUserDebugItem(list_of_points_0[i])
                p.removeUserDebugItem(list_of_points_1[i])
                p.addUserDebugPoints([co0[i]], [[0.016, 0.96, 0.99]])
                p.addUserDebugPoints([co1[i]], [[0.016, 0.96, 0.99]])
                Rcount = Rcount + 1 
                Lcount = Lcount + 1            
                
               
                
                
            p.stepSimulation()
            nums.clear()
            time.sleep(1. / 240.)

        p.disconnect()
        success = (Lcount + Rcount) / (len(co0) * 2)
        gripper_vals.fitness = success
        gripper_vals.finger_0.reached = reachedR
        gripper_vals.finger_1.reached = reachedL
        gripper_vals.finger_0.not_reached = co0
        gripper_vals.finger_1.not_reached = co1
        
        with open(f"../output/{self.gripper_name}.json", "w") as f:
            new_json = ""
            new_json += json.dumps(gripper_vals, indent=4)
            f.write(new_json)
            f.close()
        gripper_vals.clear()
        return success                


                          
        
        
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
