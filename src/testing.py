# Adapted from Josh Campbell by Marshall Saltz
# Date: 12-25-2022

#!/usr/bin/python3
import pybullet as p
import time
import pybullet_data
import os
import json
import glob
from math import pi
import random
class sim_tester():
    """Simulator class to test different hands in."""

    def __init__(self, gripper_name, gripper_loc):
        """Initialize the sim_tester class.

        Args:
            gripper_name (str): The name of the gripper to be pulled into the simulator enviroment
            gripper_loc (str): The location of the top hand directory in the output directory
        """
        self.gripper_name = gripper_name
        self.gripper_loc = gripper_loc
        
        self.directory = os.path.dirname(__file__)
 

    """
    This runs the simulation, opens the gripper urdf into the simulation, generates a sphere, 
    measures the fitness score based off contact made at two points, and generates new spheres at random positions
    if one gets knocked to far away for the gripper to reach.
    """
    def main(self, start):
        executionTime = 0
         

        success = 0
        physicsClient = p.connect(p.DIRECT)  # or p.GUI for graphical version
        p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
        p.setGravity(0, 0, 0)
        LinkId = []
        cubeStartPos = [0, 0, 1]
        cubeStartOrientation = p.getQuaternionFromEuler([0, 0, 0])

        boxId = p.loadURDF(f"{self.gripper_loc}/{self.gripper_name}.urdf", useFixedBase=1, flags=p.URDF_USE_SELF_COLLISION)#, baseOrientation=p.getQuaternionFromEuler([0, pi/2, pi/2]))

        gripper = boxId

            
        p.resetDebugVisualizerCamera(cameraDistance=.2, cameraYaw=180, cameraPitch=-91, cameraTargetPosition=[0, 0.1, 0.1])
        appleC = p.createCollisionShape(p.GEOM_SPHERE,radius=0.02)
        appleV = p.createVisualShape(p.GEOM_SPHERE, radius=0.02, rgbaColor=[1,0,0,1])
        apple = p.createMultiBody(appleC,appleV,basePosition=[random.uniform(-0.01,0.08),random.uniform(-0.01,0.08),0.01],flags=p.URDF_USE_SELF_COLLISION)
                    
        p.changeDynamics(apple, -1, mass=0.0001)
            
            

           # links_list = []
            
        for i in range(0, p.getNumJoints(gripper)):
               # links_list.append(int(i))       
            p.setJointMotorControl2(gripper, i, p.POSITION_CONTROL, targetPosition=1.5)
            linkName = p.getJointInfo(gripper, i)[12].decode("ascii")
            #idealfinger0Contact = 1 
            #ideaFinger1Contact = 1 #CHANGE THIS TO NUMBER OF FINGER SEGMENTS 
            #finger0ContactPoints = 0
            #finger1ContactPoints = 0
            idealContactPoints = 2
       
        while p.isConnected() and executionTime < 15:
                
            p.performCollisionDetection(physicsClient)
            contactPoints = len(p.getContactPoints(gripper, apple))
         
            points = p.getClosestPoints(gripper, apple, 0.25)

            if points == ():
                appleC = p.createCollisionShape(p.GEOM_SPHERE,radius=0.02)
                appleV = p.createVisualShape(p.GEOM_SPHERE, radius=0.02, rgbaColor=[1,0,0,1])
                apple = p.createMultiBody(appleC,appleV,basePosition=[random.uniform(-0.01,0.08),random.uniform(-0.01,0.08),0.01],flags=p.URDF_USE_SELF_COLLISION)
                p.changeDynamics(apple, -1, mass=0.0001)


                #idealpos = []
                #idealkin = []
                #links_list=[]
                
            if contactPoints >= idealContactPoints:
                    #for i in range(0, p.getNumJoints(gripper)):
                        #links_list.append(p.getLinkState(gripper, i))                 
                        #idealpos.append(links_list[i][4])
                        #target = ()
                        #target = idealpos[i]
                        #idealkin=p.calculateInverseKinematics(gripper, i, targetPosition=target, maxNumIterations=100)
                    #for i in range(len(idealkin)):
                        #var = idealkin[i]
                        #p.setJointMotorControl2(gripper, i, p.POSITION_CONTROL, targetPosition=var, force=1)  
                    #p.removeBody(apple)
                success+=1                        
                print("Successful Contact made: ", success)
                    
                   
                    
               
                    
                
            else:
                for i in range(0, p.getNumJoints(gripper)):
                    p.setJointMotorControl2(gripper, i, p.POSITION_CONTROL, targetPosition=random.uniform(-2,2), force=1)
                    
            p.stepSimulation()
            time.sleep(1. / 240.)

            executionTime = (time.time() - start)
       
        p.disconnect()
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

"""
                for i in range(0, p.getNumJoints(gripper)):
                    if "finger0" in str(linkName):
                        p.performCollisionDetection(physicsClient)
                        finger0ContactPoints = len(p.getContactPoints(bodyA=gripper,bodyB=apple))
                                     
                    if "finger1" in str(linkName):
                        p.performCollisionDetection(physicsClient)
                        finger1ContactPoints = len(p.getContactPoints(bodyA = gripper, bodyB=apple, linkIndexA=i))
"""   