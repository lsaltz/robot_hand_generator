# Adapted from Josh Campbell by Marshall Saltz
# Date: 12-25-2022

#!/usr/bin/python3
from pybullet_utils import bullet_client as bc
import pybullet_data
import pybullet as p
import matplotlib.pyplot as plt
import time
import pybullet_data
import os
import json
import glob
import math
import random
import csv
from addict import Dict
import numpy as np

class sim_tester():
    

    def __init__(self, name, rt, ls, coords0, coords1):
        self.gripper_loc = rt
        self.gripper_name = name
        self.ls = ls
        self.list_of_gripper_vals = []
        self.coo0 = coords0
        self.coo1 = coords1
        self.directory = os.path.dirname(__file__)
        
    def initialize_environment(self, loc, name):
        pc = bc.BulletClient(connection_mode=p.DIRECT)    #or GUI for visual (slower)
        pc.configureDebugVisualizer(pc.COV_ENABLE_RENDERING,0)
        pc.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
        pc.setGravity(0, 0, 0)
        
        
        cubeStartPos = [0, 0, 1]
        cubeStartOrientation = pc.getQuaternionFromEuler([0, 0, 0])

        gripper = pc.loadURDF(f"{loc}/{name}.urdf", useFixedBase=1, flags=pc.URDF_USE_SELF_COLLISION_INCLUDE_PARENT) 
        
        pc.resetDebugVisualizerCamera(cameraDistance=.2, cameraYaw=180, cameraPitch=-91, cameraTargetPosition=[0, 0.1, 0.1])
                    
        
        #pc.changeDynamics(gripper, 0, jointLowerLimit=((math.pi)/4), jointUpperLimit=((5*math.pi)/4))
        #pc.changeDynamics(gripper, 3, jointLowerLimit=((3*math.pi)/4), jointUpperLimit=((7*math.pi)/4))
        #pc.changeDynamics(gripper, 1, jointLowerLimit=-(math.pi/2), jointUpperLimit=(math.pi/2))
        #pc.changeDynamics(gripper, 4, jointLowerLimit=-(math.pi/2), jointUpperLimit=(math.pi/2))
        max_link_0, max_link_1 = self.get_max_link(self.gripper_name)
        pc.changeDynamics(gripper, 0, jointLowerLimit=((math.pi)/2), jointUpperLimit=((5*math.pi)/4))
        
        pc.changeDynamics(gripper, max_link_0+1, jointLowerLimit=-(math.pi/2), jointUpperLimit=-(5*math.pi/4))
        return [gripper, pc, name]    
    
    def test_grippers(self):
        
        sims = []
        
        for l in self.ls:
            gripper_vals = Dict()
            name = l["name"]
            gripper_vals.name = name
            loc = f"../output/{name}/hand"
            sims.append(self.initialize_environment(loc, name))
            self.list_of_gripper_vals.append(gripper_vals)
            
        for s in sims:
            list_of_points_0, list_of_points_1 = self.debug_pts(s)   
        for i in range(len(self.coo0)):
            for s in sims: 
                worldPos = self.test_pts(self.coo1[i], self.coo0[i], s)
                collide_count = self.collide(s)
                self.return_points(worldPos, collide_count, s, list_of_points_0, list_of_points_1, i)
        for s in sims:
            pc = s[1]
            pc.disconnect()            
                
    def gui_test(self):
    
        co0, co1 = self.coo0, self.coo1
        physicsClient = p.connect(p.DIRECT)
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
        print(self.gripper_name)
        boxId = p.loadURDF(f"{self.gripper_loc}/{self.gripper_name}.urdf", useFixedBase=1, flags=p.URDF_USE_SELF_COLLISION_INCLUDE_PARENT) 
        gripper_vals.name = self.gripper_name
        gripper = boxId

          
        p.resetDebugVisualizerCamera(cameraDistance=.2, cameraYaw=180, cameraPitch=-91, cameraTargetPosition=[0, 0.1, 0.1])
                    
        
        list_of_points_1 = []
        list_of_points_0 = []
        

        for i in range(len(co0)):
            list_of_points_0.append(p.addUserDebugPoints([co0[i]], [[1, 0, 0]]))
            
            list_of_points_1.append(p.addUserDebugPoints([co1[i]], [[1, 0, 0]]))
        
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING,1)
        max_link_0, max_link_1 = self.get_max_link(self.gripper_name)
        p.changeDynamics(gripper, 0, jointLowerLimit=((math.pi)/2), jointUpperLimit=((5*math.pi)/4))
        
        p.changeDynamics(gripper, max_link_0+1, jointLowerLimit=-(math.pi/2), jointUpperLimit=-(5*math.pi/4))
        
        for i in range(len(co0)):
                         
            p.resetJointState(gripper, 0, targetValue=((5*math.pi)/4))
            p.resetJointState(gripper, 1, targetValue=(math.pi/2))
            
            p.resetJointState(gripper, max_link_0+1, targetValue=((3*math.pi)/4))
            p.resetJointState(gripper, max_link_0+2, targetValue=-(math.pi/2))
            
            idealJointPoses1 = p.calculateInverseKinematics(gripper, max_link_1, co1[i], maxNumIterations=3000)
            
            idealJointPoses0 = p.calculateInverseKinematics(gripper, max_link_0, co0[i], maxNumIterations=3000)
            
            
            for j in range(max_link_0+1):
                p.resetJointState(gripper, j, targetValue=idealJointPoses0[j])
                
            for j in range(max_link_0+1, max_link_1+1):
                p.resetJointState(gripper, j, targetValue=idealJointPoses1[j])
            offset_val = 3
            worldPos0 = p.getLinkState(gripper, max_link_0, computeForwardKinematics=1)
            worldPos1 = p.getLinkState(gripper, max_link_1, computeForwardKinematics=1)
            
            
            world_pos_0_x = round(worldPos0[0][0], offset_val)
            world_pos_0_y = round(worldPos0[0][1], offset_val)
            world_pos_1_x = round(worldPos1[0][0], offset_val)
            world_pos_1_y = round(worldPos1[0][1], offset_val)
            
            point_0_x = round(co0[i][0], offset_val)
            point_0_y = round(co0[i][1], offset_val)
            point_1_x = round(co1[i][0], offset_val)
            point_1_y = round(co1[i][1], offset_val)
            
            #print(worldPos0)
            #print("c0 ", co0[i])
            #print("c1 ", co1[i])
            #print(worldPos1)
            p.performCollisionDetection()
            add = 0
            nums = []
            """
            for links in range(p.getNumJoints(gripper)):
                num = p.getAABB(gripper, links)
                nums.append(p.getOverlappingObjects(num[0], num[1]))
                add = add + len(nums[links]) 
            """
            if world_pos_0_x == point_0_x and world_pos_0_y == point_0_y and world_pos_1_x == point_1_x and world_pos_1_y == point_1_y:
                
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
            
            time.sleep(1. / 240.)

        p.disconnect()
        success = (Lcount + Rcount) / (len(co0) + len(co1))
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
        
        return [success, str(self.gripper_name)+".json"]
        
    def debug_pts(self, sim):
        pc = sim[1]  
        list_of_points_1 = []
        list_of_points_0 = []
        
        for i in range(len(self.coo0)):
            list_of_points_0.append(pc.addUserDebugPoints([self.coo0[i]], [[1, 0, 0]]))
            
            list_of_points_1.append(pc.addUserDebugPoints([self.coo1[i]], [[1, 0, 0]]))
        pc.configureDebugVisualizer(pc.COV_ENABLE_RENDERING,1)
        return list_of_points_0, list_of_points_1
        
    def get_max_link(self, name):
        with open(f"../output/{name}/{name}.json", mode="r+") as f:
            dictionary = json.load(f)
            to_test = Dict(dictionary)
        f.close()
        
        max_link_0 = to_test.hand.finger_0.segment_qty - 1
        max_link_1 = max_link_0 + to_test.hand.finger_1.segment_qty
        return max_link_0, max_link_1
        
    def test_pts(self, co1, co0, sim):
        gripper = sim[0]
        pc = sim[1]
        max_link_0, max_link_1 = self.get_max_link(sim[2])
        
        pc.resetJointState(gripper, 0, targetValue=((5*math.pi)/4))
        pc.resetJointState(gripper, 1, targetValue=(math.pi/2))
            
        pc.resetJointState(gripper, max_link_0+1, targetValue=((3*math.pi)/4))
        pc.resetJointState(gripper, max_link_0+2, targetValue=-(math.pi/2))
        
        idealJointPoses1 = pc.calculateInverseKinematics(gripper, max_link_0, co1, maxNumIterations=3000)
        idealJointPoses0 = pc.calculateInverseKinematics(gripper, max_link_1, co0, maxNumIterations=3000)
        
        for i in range(len(idealJointPoses0)):     
            pc.resetJointState(gripper, i, targetValue=idealJointPoses[i])
            
        for i in range(len(idealJointPoses1)):
            pc.resetJointState(gripper, i, targetValue=idealJointPoses0[i])
        
        worldPos = pc.getLinkStates(gripper, [max_link_0, max_link_1], computeForwardKinematics=1)
        
        return worldPos
        
    def collide(self, sim):
        gripper = sim[0]
        pc = sim[1]
        nums = []
        pc.performCollisionDetection()
        add = 0
        for links in range(pc.getNumJoints(gripper)):
            num = pc.getAABB(gripper, links)
            nums.append(pc.getOverlappingObjects(num[0], num[1]))
            add = add + len(nums[links])   
        return add     
    
    def return_points(self, worldPos, add, sim, list_of_points_0, list_of_points_1, i):     
        gripper = sim[0]
        pc = sim[1]
        name = sim[2]
        offset_val = 2
        world_pos_0_x = round(worldPos[0][0][0], offset_val)
        world_pos_0_y = round(worldPos[0][0][1], offset_val)
        world_pos_1_x = round(worldPos[1][0][0], offset_val)
        world_pos_1_y = round(worldPos[1][0][1], offset_val)
            
        point_0_x = round(self.coo0[i][0], offset_val)
        point_0_y = round(self.coo0[i][1], offset_val)
        point_1_x = round(self.coo1[i][0], offset_val)
        point_1_y = round(self.coo1[i][1], offset_val)
           
        if world_pos_0_x == point_0_x and world_pos_0_y == point_0_y and world_pos_1_x == point_1_x and world_pos_1_y == point_1_y and add <= 20:
            
            pc.removeUserDebugItem(list_of_points_0[i])
            pc.removeUserDebugItem(list_of_points_1[i])
            pc.addUserDebugPoints([self.coo0[i]], [[0.016, 0.96, 0.99]])
            pc.addUserDebugPoints([self.coo1[i]], [[0.016, 0.96, 0.99]])
            for d in self.list_of_gripper_vals:
                if d["name"]==name:
                    d.finger_0.setdefault("reached", []).append((point_0_x, point_0_y))
                    d.finger_1.setdefault("reached", []).append((point_1_x, point_1_y))
                else:
                    pass   
        else:
             for d in self.list_of_gripper_vals:
                if d["name"]==name:
                    d.finger_0.setdefault("not_reached", []).append((point_0_x, point_0_y))
                    d.finger_1.setdefault("not_reached", []).append((point_1_x, point_1_y))      
                else:
                    pass
    def return_fitness(self):
       list_of_fitness = []
       for d in self.list_of_gripper_vals:
           Lcount = len(d.finger_1.reached)
           Rcount = len(d.finger_0.reached)
           success = (Lcount + Rcount) / (len(self.coo0) * 2)
           
           list_of_fitness.append((success, str(d["name"])+".json"))
       return list_of_fitness
               
    def main(self):
        
        self.test_grippers()
        
        list_of_fitness = self.return_fitness()
        for g in self.list_of_gripper_vals:        
            self.write_json(g.name, g)
            g.clear()
        print(list_of_fitness)
        return list_of_fitness
         
    def write_json(self, name, gripper_vals):
        with open(f"../points/{name}.json", "w") as f:
            new_json = ""
            new_json += json.dumps(gripper_vals, indent=4)
            f.write(new_json)
       
