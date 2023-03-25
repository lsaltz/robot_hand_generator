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
from math import pi
import random

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
 

    """
    This runs the simulation, opens the gripper urdf into the simulation, generates a sphere, 
    measures the fitness score based off contact made at two points, and generates new spheres at random positions
    if one gets knocked to far away for the gripper to reach.
    """       
    def coordinate_array(self):
        finger_z = self.rob_dic.finger_z + 0.25
        val = 0.01
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
        row_points = int(row_length/0.005)
        column_points = int(column_length/0.005)
        
        valx1 = 0
        valx2 = 0.05
        x1 = top
        
        while x1 > 0-finger_z: 
            x1 = ((finger_z+val)-valx1)
            x2 = ((finger_z+val)-valx2)
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
        return coords1, coords2
        
    def main(self, generation):
        co0, co1 = self.coordinate_array()
        physicsClient = p.connect(p.DIRECT)  # or p.GUI for graphical version
        p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
        p.setGravity(0, 0, 0)
        LinkId = []
        cubeStartPos = [0, 0, 1]
        cubeStartOrientation = p.getQuaternionFromEuler([0, 0, 0])

        boxId = p.loadURDF(f"{self.gripper_loc}/{self.gripper_name}.urdf", useFixedBase=1, flags=p.URDF_USE_SELF_COLLISION_INCLUDE_PARENT)#, baseOrientation=p.getQuaternionFromEuler([0, pi/2, pi/2]))

        gripper = boxId

            
        p.resetDebugVisualizerCamera(cameraDistance=.2, cameraYaw=180, cameraPitch=-91, cameraTargetPosition=[0, 0.1, 0.1])
                    
       
        p.changeDynamics(gripper, 3, jointLowerLimit=-1.5, jointUpperLimit=1.4)
        p.changeDynamics(gripper, 0, jointLowerLimit=-1.5, jointUpperLimit=1.4)
        Lcount = 0
        Rcount = 0  
        name = self.gripper_name + ".png"        
        if generation % 50 == 0:
            figure, axis = plt.subplots(2, 1)
            axis[0].set_title("Finger 0")
            axis[1].set_title("Finger 1")
            for i in range(len(co0)):
            
                axis[0].scatter(co0[i][0], co0[i][1], color='red')
                axis[1].scatter(co1[i][0], co1[i][1], color='red')
            for i in range(len(co0)):

                idealJointPoses = p.calculateInverseKinematics2(gripper, [2, 5], [co0[i],co1[i]], maxNumIterations=3000)
                
                p.setJointMotorControlArray(gripper, [0, 1, 2, 3, 4, 5], p.POSITION_CONTROL, targetPositions=idealJointPoses)
                worldPos = p.getLinkStates(gripper, [2, 5], computeForwardKinematics=1)
          
                if (worldPos[0][0][0] <= co0[i][0]+0.05 and worldPos[0][0][0] >= co0[i][0]-0.05) and (worldPos[0][0][1] <= co0[i][1]+0.05 and worldPos[0][0][1] >= co0[i][1]-0.05):
                    print("R Reached!")
                    Rcount = Rcount + 1
                    axis[0].scatter(co0[i][0], co0[i][1], color='green')
                else:
                    print("R not reached")
                
                      
                if (worldPos[1][0][0] <= co1[i][0]+0.05 and worldPos[1][0][0] >= co1[i][0]-0.05) and (worldPos[1][0][1] <= co1[i][1]+0.05 and worldPos[1][0][1] >= co1[i][1]-0.005):
                    print("L Reached!")
                    Lcount = Lcount + 1
                    axis[1].scatter(co1[i][0], co1[i][1], color='green')
                else:
                    print("L not reached")
                           
                p.stepSimulation()
                time.sleep(1. / 240.)
            print(Lcount)

            print(Rcount)

            print(len(co0))
            
            plt.savefig(f"../output/{name}")
        else:
            for i in range(len(co0)):

                idealJointPoses = p.calculateInverseKinematics2(gripper, [2, 5], [co0[i],co1[i]], maxNumIterations=3000)
                
                p.setJointMotorControlArray(gripper, [0, 1, 2, 3, 4, 5], p.POSITION_CONTROL, targetPositions=idealJointPoses)
                worldPos = p.getLinkStates(gripper, [2, 5], computeForwardKinematics=1)
          
                if (worldPos[0][0][0] <= co0[i][0]+0.05 and worldPos[0][0][0] >= co0[i][0]-0.05) and (worldPos[0][0][1] <= co0[i][1]+0.05 and worldPos[0][0][1] >= co0[i][1]-0.05):
                    print("R Reached!")
                    Rcount = Rcount + 1
                else:
                    print("R not reached")
                
                      
                if (worldPos[1][0][0] <= co1[i][0]+0.05 and worldPos[1][0][0] >= co1[i][0]-0.05) and (worldPos[1][0][1] <= co1[i][1]+0.05 and worldPos[1][0][1] >= co1[i][1]-0.005):
                    print("L Reached!")
                    Lcount = Lcount + 1
                else:
                    print("L not reached")
                           
                p.stepSimulation()
                time.sleep(1. / 240.)
                
            print(Lcount)

            print(Rcount)

            print(len(co0))
            
        p.disconnect()
        success = Lcount + Rcount
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

