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

    def __init__(self):
        """Initialize the sim_tester class.

        Args:
            gripper_name (str): The name of the gripper to be pulled into the simulator enviroment
            gripper_loc (str): The location of the top hand directory in the output directory
        """
        self.gripper_name = gripper_name
        self.gripper_loc = gripper_loc
        
        self.directory = os.path.dirname(__file__)
 

    def main(self, start):
         
        success = 0
        physicsClient = p.connect(p.GUI)  # or p.DIRECT for non-graphical version
        p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
        p.setGravity(0, 0, 0)
        LinkId = []
        cubeStartPos = [0, 0, 1]
        cubeStartOrientation = p.getQuaternionFromEuler([0, 0, 0])

        boxId = p.loadURDF(f"{self.gripper_loc}hand/{self.gripper_name}.urdf", useFixedBase=1, flags=p.URDF_USE_SELF_COLLISION)#, baseOrientation=p.getQuaternionFromEuler([0, pi/2, pi/2]))

        gripper = boxId

        
        p.resetDebugVisualizerCamera(cameraDistance=.2, cameraYaw=180, cameraPitch=-91, cameraTargetPosition=[0, 0.1, 0.1])
        appleC = p.createCollisionShape(p.GEOM_SPHERE,radius=0.02)
        appleV = p.createVisualShape(p.GEOM_SPHERE, radius=0.02, rgbaColor=[1,0,0,1])
        apple = p.createMultiBody(appleC,appleV,basePosition=[0.01,0.1,0.01],flags=p.URDF_USE_SELF_COLLISION)
                
        p.changeDynamics(apple, -1, mass=0.0001)
        
        
        
        """
        Goal: Get highest number of contact points
        """
       # links_list = []
        
        for i in range(0, p.getNumJoints(gripper)):
           # links_list.append(int(i))       
            p.setJointMotorControl2(gripper, i, p.POSITION_CONTROL, targetPosition=1.5)
            linkName = p.getJointInfo(gripper, i)[12].decode("ascii")
            if "finger0" in str(linkName):
                p.performCollisionDetection(physicsClient)
                finger0ContactPoints = len(p.getContactPoints(bodyA=gripper,bodyB=apple, linkIndexA=i))
                idealfinger0Contact = 2
                p.setJointMotorControl2(gripper, i, p.POSITION_CONTROL, targetPosition=-1.5)                
            if "finger1" in str(linkName):
                p.performCollisionDetection(physicsClient)
                finger1ContactPoints = len(p.getContactPoints(bodyA = gripper, bodyB=apple, linkIndexA=i))
                ideaFinger1Contact = 2 #CHANGE THIS TO NUMBER OF FINGER SEGMENTS
            
        while p.isConnected():
            
            points = p.getClosestPoints(gripper, apple, 0.25)

            if points == ():
                appleC = p.createCollisionShape(p.GEOM_SPHERE,radius=0.02)
                appleV = p.createVisualShape(p.GEOM_SPHERE, radius=0.02, rgbaColor=[1,0,0,1])
                apple = p.createMultiBody(appleC,appleV,basePosition=[random.uniform(-0.01,0.1),random.uniform(-0.01,0.1),0.01],flags=p.URDF_USE_SELF_COLLISION)
                p.changeDynamics(apple, -1, mass=0.0001)


            idealpos = []
            idealkin = []
            links_list=[]
            
            while finger0ContactPoints >= idealfinger0Contact and finger1ContactPoints >= ideaFinger1Contact:
                for i in range(0, p.getNumJoints(gripper)):
                    links_list.append(p.getLinkState(gripper, i))                 
                    idealpos.append(links_list[i][4])
                    target = ()
                    target = idealpos[i]
                    idealkin=p.calculateInverseKinematics(gripper, i, targetPosition=target, maxNumIterations=100)
                for i in range(len(idealkin)):
                    var = idealkin[i]
                    p.setJointMotorControl2(gripper, i, p.POSITION_CONTROL, targetPosition=var, force=1)               
                print("Successful Contact made")
                
               
                success+=1
                break
            break
            
            if "finger0" in str(linkName):
                p.performCollisionDetection(physicsClient)
                finger0ContactPoints = len(p.getContactPoints(bodyA=gripper,bodyB=apple, linkIndexA=i))            
            if "finger1" in str(linkName):
                p.performCollisionDetection(physicsClient)
                finger1ContactPoints = len(p.getContactPoints(bodyA = gripper, bodyB=apple, linkIndexA=i))
            for i in range(0, p.getNumJoints(gripper)):
                p.setJointMotorControl2(gripper, i, p.POSITION_CONTROL, targetPosition=random.uniform(-2,2), force=1)
            
            p.stepSimulation()
            time.sleep(1. / 240.)

        executionTime = time.time() - start
        
        return executionTime/success
        p.disconnect()
        
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

