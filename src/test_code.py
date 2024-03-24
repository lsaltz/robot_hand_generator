import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib import path
from matplotlib.lines import Line2D
import main
import build_hand as bh
import matplotlib.patches as patches
import basic_load
from addict import Dict
from pybullet_utils import bullet_client as bc
import pybullet_data
import pybullet as p
import time
from scipy.spatial import ConvexHull
import math
"""
TODO:
1. check limits with graphing
2. cut back on redundant code
3. run 500x
4. figure out how to measure rotation (while running)
5. clean up sim test
"""




class WorkSpace_Test:

    def __init__(self, loc, name):
        
        
        self.loc = loc
        self.name = name
        
        
 
             
    def main(self):
    
        
        val = 0.03
        points0, points1 = self.coords(val)
        tc0, tc1 = self.run_sim(points0, points1)
        
        x_arr0 = np.split(tc0, len(tc0), 0)[0]
        y_arr0 =  np.split(tc0, len(tc0), 0)[1]
        x_arr1 = np.split(tc1, len(tc1), 0)[0]
        y_arr1 =  np.split(tc1, len(tc1), 0)[1]
        
        #inside_indicies0 = self.raycasting(x_arr0, y_arr0, points0)
        #inside_indicies1 = self.raycasting(x_arr0, y_arr1, points1)
        
        #fitness = self.fitness(inside_indicies0, inside_indicies1, points0, points1)
        
        return 0#fitness
     
     
    def coords(self, val):
        finger_z = 0.2
    
    
        total_height = 0.2
        coords1 = []
        coords2 = []
        bottom_x = -abs(total_height)
        bottom_y = 0
        row_length = finger_z - bottom_x
        column_length = finger_z - bottom_y
        row_points = int(row_length/val)
        column_points = int(column_length/val)
        n = 8
        rad = 0.039
      
        center_pt = [[x, y, 0] for x in np.linspace(bottom_x, finger_z, num=row_points) for y in np.linspace(bottom_y, finger_z, num=column_points)]
    
        x1 = [(c[0] + (np.cos(2*np.pi/n*x)*rad)) for c in center_pt for x in range(0, n+1)]
    
   
        y1 = [(c[1] + (np.sin(2*np.pi/n*x)*rad)) for c in center_pt for x in range(0, n+1)]
        z1 = np.linspace(0, 0, len(x1))
        coords1 = list(zip(x1, y1, z1))
        x2 = [(c[0] + (np.cos(2*np.pi/n*x+np.pi)*rad)) for c in center_pt for x in range(0, n+1)]
        y2 = [(c[1] - (np.sin(2*np.pi/n*x+np.pi)*rad)) for c in center_pt for x in range(0, n+1)]
    
        z2 = np.linspace(0, 0, len(x2))
        coords2 = list(zip(x2, y2, z2))
        c1 = np.reshape(np.asarray(coords1), (-1, n+1, 3)).tolist()
    
        c2 = np.reshape(np.asarray(coords2), (-1, n+1, 3)).tolist()
    
        c = []
    
        for i in range(len(center_pt)):
            c3 = [center_pt[i], c1[i], c2[i]]
            c.append(c3)
     
        return np.asarray(coords1), np.asarray(coords2)
        
    def move_theta(self, mi, ma, nj, pc, gripper):
        test_coords = []
        for i in range(mi, ma):
            #pc.setJointMotorControl2(gripper, nj, controlMode=p.POSITION_CONTROL, targetPosition=i*np.pi/180)
            pc.resetJointState(gripper, nj, targetValue=i*np.pi/180)
            pc.stepSimulation()
            worldPos = pc.getLinkState(gripper, 3, computeForwardKinematics=True)
            plt.scatter(worldPos[0][0], worldPos[0][1])
            x = worldPos[0][0]
            y = worldPos[0][1]
            test_coords.append([x,y])
            pc.addUserDebugPoints([worldPos[0]], [[1, 0, 0]])
            
            time.sleep(0.03)
        return test_coords
            
    def move_theta_reverse(self, mi, ma, nj, pc, gripper):
        test_coords = []
        for i in reversed(range(ma, mi)):
            #pc.setJointMotorControl2(gripper, nj, controlMode=p.POSITION_CONTROL, targetPosition=i*np.pi/180)
            pc.resetJointState(gripper, nj, targetValue=i*np.pi/180)
            pc.stepSimulation()
            worldPos = pc.getLinkState(gripper, 3, computeForwardKinematics=True)
            plt.scatter(worldPos[0][0], worldPos[0][1])
            x = worldPos[0][0]
            y = worldPos[0][1]
            test_coords.append([x,y])
            pc.addUserDebugPoints([worldPos[0]], [[1, 0, 0]])
            time.sleep(0.03)
        return test_coords
            
    def run_sim(self, points0, points1):
        test_coords0 = []
        test_coords1 = []
        pc = bc.BulletClient(connection_mode=p.GUI)    #or GUI for visual (slower)
        pc.configureDebugVisualizer(pc.COV_ENABLE_RENDERING,0)
        pc.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
        pc.setGravity(0, 0, 0)
        
        cubeStartPos = [0, 0, 1]
        cubeStartOrientation = pc.getQuaternionFromEuler([0, 0, 0])

        gripper = pc.loadURDF(f"{self.loc}/{self.name}.urdf", useFixedBase=1, flags=pc.URDF_USE_SELF_COLLISION_INCLUDE_PARENT) 
        
        pc.resetDebugVisualizerCamera(cameraDistance=.2, cameraYaw=180, cameraPitch=-91, cameraTargetPosition=[0, 0.1, 0.1])
        for po in points0:
            pc.addUserDebugPoints([po], [[0, 1, 0]])
            plt.scatter(po[0], po[1], color='blue')
        for po in points1:
            pc.addUserDebugPoints([po], [[0, 1, 0]])
            #plt.scatter(po[0], po[1], color='blue')
  
        pc.configureDebugVisualizer(pc.COV_ENABLE_RENDERING,1)        
    
        #step1
        """
        pc.resetJointState(gripper, 0, targetValue=(-135*math.pi/180))   
        pc.resetJointState(gripper, 1, targetValue=(0*math.pi/180))   
        pc.resetJointState(gripper, 2, targetValue=(0*(math.pi/180)))
        pc.resetJointState(gripper, 3, targetValue=(math.pi))  
        pc.resetJointState(gripper, 4, targetValue=(math.pi/2))   
        pc.resetJointState(gripper, 5, targetValue=(math.pi/2))
        pc.stepSimulation()
        time.sleep(3)
    
        #step 2
        #move_theta(-135, 0, 2, pc, gripper)
        #move_theta(-135, 0, 1, pc, gripper)
    
        #step3
        test_coords0.extend(self.move_theta(-135, -135+180, 0, pc, gripper))
        #step 4
    
        test_coords0.extend(self.move_theta(0, 135, 1, pc, gripper))
        test_coords0.extend(self.move_theta(0, 135, 2, pc, gripper))
    
        #step5
        test_coords0.extend(self.move_theta_reverse(-135+180, -135, 0, pc, gripper))
        #step6
        test_coords0.extend(self.move_theta_reverse(135, 0, 1, pc, gripper))
        test_coords0.extend(self.move_theta_reverse(135, 0, 2, pc, gripper))
        
        """
        
        pc.resetJointState(gripper, 0, targetValue=(math.pi))   
        pc.resetJointState(gripper, 1, targetValue=(math.pi/2))   
        pc.resetJointState(gripper, 2, targetValue=(math.pi/2))
        pc.resetJointState(gripper, 4, targetValue=(90*math.pi/180))  
        pc.resetJointState(gripper, 5, targetValue=(180*math.pi/180))   
        pc.resetJointState(gripper, 6, targetValue=(180*math.pi/180))
        time.sleep(3)
        
        test_coords1.extend(self.move_theta_reverse(315, 135, 4, pc, gripper))
        test_coords1.extend(self.move_theta_reverse(180, 45, 5, pc, gripper))
        test_coords1.extend(self.move_theta_reverse(180, 45, 6, pc, gripper))
        test_coords1.extend(self.move_theta(135, 315, 4, pc, gripper))
        test_coords1.extend(self.move_theta(45, 180, 5, pc, gripper))
        test_coords1.extend(self.move_theta(45, 180, 6, pc, gripper))
        
        p.disconnect()  
        return np.asarray(test_coords0), np.asarray(test_coords1)  
            
    def raycasting(self, x_arr, y_arr, points):
        
        inside_indices = []
        _eps = 0.00001
        _huge = np.inf
        for idx, i in enumerate(points):
            
            inside = 0
            for k,j in enumerate(x_arr):
        
                for edge in range(len(j)-1):
        
                    A = [x_arr[k][edge], y_arr[k][edge]]
                    B = [x_arr[k][edge+1], y_arr[k][edge+1]]
        
                    if A[1] > B[1]:
                        A, B = B, A
                    if i[1] == A[1]:
                        i[1] += _eps
                    if i[1] == B[1]:
                        i[1] -= _eps
                        
                    if i[1] > B[1] or i[1] < A[1] or i[0] > max(A[0], B[0]):    # The horizontal ray does not intersect with the edge
                        continue

                    if i[0] < min(A[0], B[0]):    # The ray intersects with the edge
                        inside +=1
                        continue

                    try:
                        m_edge = (B[1] - A[1]) / (B[0] - A[0])
                    except ZeroDivisionError:
                        m_edge = _huge

                    try:
                        m_point = (i[1] - A[1]) / (i[0] - A[0])
                    except ZeroDivisionError:
                        m_point = _huge

                    if m_point >= m_edge:    # The ray intersects with the edge
                        inside +=1
                        continue

            if inside%2 != 0:
                #self.inside_points.append(i)
                inside_indices.append(idx)
                
                
            else:
                #self.outside_points.append(i)
                plt.scatter(i[0],i[1], color='red')   
                   
        return inside_indices
        
    
    def fitness(self, inside_indicies_0, inside_indicies_1, points0, points1):
        
        idx = [i for i in inside_indicies_0 if i in inside_indicies_1]
        fitness = len(idx)/(len(points0))
        
        for p in idx:
            plt.scatter(points0[p][0], points0[p][1], color='green')           
            plt.scatter(points1[p][0], points1[p][1], color = 'yellow')
           
        return fitness     
    
    
     
if __name__ == "__main__":

    f = WorkSpace_Test("../output/hand_mut_gen_2_f/hand", "hand_mut_gen_2_f")
    fitness = f.main()
    plt.axis('equal')
    plt.show()
    print("done")
   

