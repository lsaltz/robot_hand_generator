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

#figure out why left finger goes so far
#figure out raycasting
#send plots to chat-->degrees of darkness for centerpoint(distinct rainbow colors like a gradient)
#incorporate ea
#finish writing by end of term
#get metrics and plot together for next monday
#finalize plots before integration into ea
#COLLECT ALL DATA
class WorkSpace_Test:

    def __init__(self, loc, name, l1, l2, l3, width, height):
        
        
        self.loc = loc
        self.name = name
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.l4 = 0.012959999999999998 + 0.0108
        self.l5 = 0.06768 + 0.0108
        self.l6 = 0.06336 + 0.0108
        self.width = width
        self.height = height
        
 
             
    def main(self, right_coords, left_coords):
    
        
        val = 0.03
        cent, r, l = self.coords(val)
        
        ri = self.build_coord_space_right()
        le = self.build_coord_space_left()
        #print(ri)
        
        x_arr0 = np.split(ri, 2, 1)[0]
        
        y_arr0 =  np.split(ri, 2, 1)[1]
        
        x_arr1 = np.split(le, 2, 1)[0]
        y_arr1 =  np.split(le, 2, 1)[1]
        
        
        inside_indicies0 = self.raycasting(x_arr0, y_arr0, r)
        
        inside_indicies1 = self.raycasting(x_arr1, y_arr1, l)
        
        fitness, i0, i1 = self.fitness(inside_indicies0, inside_indicies1, r, l)
        tc0, tc1 = self.run_sim(cent, right_coords, left_coords, i0, i1)
        
        return fitness
     
    def build_coord_space_right(self):
        
        right_coords = []
        
        for i in range(-135, -135+180):
            right_coords.append(self.mathy_thing(i, 0, 0))
        for i in range(0, 90):
            right_coords.append(self.mathy_thing(-135+180, i, 0))
        for i in range(0, 90):
            right_coords.append(self.mathy_thing(-135+180, 90, i))
        for i in reversed(range(-135, -135+180)):
            right_coords.append(self.mathy_thing(i, 90, 90))
        for i in reversed(range(0, 90)):
            right_coords.append(self.mathy_thing(-135, i, 90))
        for i in reversed(range(0, 90)):
            right_coords.append(self.mathy_thing(-135, 0, i))
        r = []
        for i in right_coords:
        
            plt.scatter(i[0], i[1], color='blue')
        
        return np.asarray(right_coords)
        
    def build_coord_space_left(self):
        left_coords = []
        
        for i in reversed(range(135-180, 135)):
            left_coords.append(self.mathy_thing1(i, 0, 0))
        for i in reversed(range(-90, 0)):
            left_coords.append(self.mathy_thing1(135-180, i, 0))
        for i in reversed(range(-90, 0)):
            left_coords.append(self.mathy_thing1(135-180, -90, i))
        for i in range(135-180, 135):
            left_coords.append(self.mathy_thing1(i, -90, -90))
        for i in range(-90, 0):
            left_coords.append(self.mathy_thing1(135, i, -90))
        for i in range(-90, 0):
            left_coords.append(self.mathy_thing1(135, 0, i))
        l = []
        for i in left_coords:
            
            plt.scatter(i[0], i[1], color='blue')
        return np.asarray(left_coords)
        
    def mathy_thing(self, theta1, theta2, theta3):
        theta1 = np.pi * theta1 / 180
        theta2 = np.pi * theta2 / 180
        theta3 = np.pi * theta3 / 180
        val = 90 * np.pi/180
        #width = 0.05386
        
        x = self.l1 *np.cos(theta1 + val) + self.l2*np.cos(theta1+theta2 + val) + self.l3*np.cos(theta1 + theta2 + theta3 + val) + self.width/2
        y = self.l1 * np.sin(theta1 + val) + self.l2*np.sin(theta1 + theta2 + val) + self.l3*np.sin(theta1 + theta2 + theta3 + val)
        
        
        return [x, y] 
    
    def mathy_thing1(self, theta1, theta2, theta3):
        theta1 = np.pi * theta1 / 180
        theta2 = np.pi * theta2 / 180
        theta3 = np.pi * theta3 / 180
        val = 90 * np.pi/180
        #width = 0.05386
        
        x = self.l4 *np.cos(theta1 + val) + self.l5*np.cos(theta1+theta2 + val) + self.l6*np.cos(theta1 + theta2 + theta3 + val) - self.width/2
        y = self.l4 * np.sin(theta1 + val) + self.l5*np.sin(theta1 + theta2 + val) + self.l6*np.sin(theta1 + theta2 + theta3 + val)
        
        
        return [x, y] 
        
    def coords(self, val):
        finger_z = 0.2
    
    
        total_height = 0.2
        coords1 = []
        coords2 = []
        bottom_x = -abs(total_height)
        bottom_y = -abs(total_height)
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
        coords1 = list(zip(x1, y1))
        x2 = [(c[0] + (np.cos(2*np.pi/n*x+np.pi)*rad)) for c in center_pt for x in range(0, n+1)]
        y2 = [(c[1] - (np.sin(2*np.pi/n*x+np.pi)*rad)) for c in center_pt for x in range(0, n+1)]
    
        z2 = np.linspace(0, 0, len(x2))
        coords2 = list(zip(x2, y2))
        c1 = np.reshape(np.asarray(coords1), (-1, n+1, 2)).tolist()
    
        c2 = np.reshape(np.asarray(coords2), (-1, n+1, 2)).tolist()
    
        c = []
        r = []
        l = []
        
        for i in center_pt:
            if i[0] < self.width/2 and i[0] > -abs(self.width)/2 and i[1] <0:
                center_pt.remove(i)
            else:
                c.append(i)
                plt.scatter(i[0], i[1], color="red")
        r = np.asarray(coords1)
        l = np.asarray(coords2)
        
        return c, r, l
        
    def move_theta(self, mi, ma, nj, pc, gripper):
        test_coords = []
        for i in range(mi, ma):
            #pc.setJointMotorControl2(gripper, nj, controlMode=p.POSITION_CONTROL, targetPosition=i*np.pi/180)
            pc.resetJointState(gripper, nj, targetValue=i*np.pi/180)
            pc.stepSimulation()
            if nj <4:
                worldPos = pc.getLinkState(gripper, 3, computeForwardKinematics=True)
            else:
                worldPos = pc.getLinkState(gripper, 7, computeForwardKinematics=True)
            #plt.scatter(worldPos[0][0], worldPos[0][1])
            x = worldPos[0][0]
            y = worldPos[0][1]
            test_coords.append([x,y])
            pc.addUserDebugPoints([worldPos[0]], [[1, 0, 0]])
            
            time.sleep(0.0001)
        return test_coords
            
    def move_theta_reverse(self, mi, ma, nj, pc, gripper):
        test_coords = []
        for i in reversed(range(ma, mi)):
            #pc.setJointMotorControl2(gripper, nj, controlMode=p.POSITION_CONTROL, targetPosition=i*np.pi/180)
            pc.resetJointState(gripper, nj, targetValue=i*np.pi/180)
            pc.stepSimulation()
            if nj <4:
                worldPos = pc.getLinkState(gripper, 3, computeForwardKinematics=True)
            else:
                worldPos = pc.getLinkState(gripper, 7, computeForwardKinematics=True)
            #plt.scatter(worldPos[0][0], worldPos[0][1])
            x = worldPos[0][0]
            y = worldPos[0][1]
            test_coords.append([x,y])
            pc.addUserDebugPoints([worldPos[0]], [[1, 0, 0]])
            time.sleep(0.0001)
        return test_coords
            
    def run_sim(self, cent, right_coords, left_coords, idx0, idx1):
        test_coords0 = []
        test_coords1 = []
        pc = bc.BulletClient(connection_mode=p.GUI)    #or GUI for visual (slower)
        pc.configureDebugVisualizer(pc.COV_ENABLE_RENDERING,0)
        pc.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
        pc.setGravity(0, 0, 0)
        
        cubeStartPos = [0, 0, 1]
        cubeStartOrientation = pc.getQuaternionFromEuler([0, 0, 0])

        gripper = pc.loadURDF(f"{self.loc}/{self.name}.urdf", useFixedBase=1)#, flags=p.URDF_USE_SELF_COLLISION) 
        
        pc.resetDebugVisualizerCamera(cameraDistance=.2, cameraYaw=180, cameraPitch=-91, cameraTargetPosition=[0, 0.1, 0.1])
        for i in idx0:
            pc.addUserDebugPoints([[i[0], i[1], 0]], [[0, 1, 0]])
        for i in idx1:
            pc.addUserDebugPoints([[i[0], i[1], 0]], [[0, 1, 1]])
            #plt.scatter(po[0], po[1], color='blue')
        #for po in points1:
            #pc.addUserDebugPoints([[po[0], po[1], 0]], [[0, 1, 0]])
            #plt.scatter(po[0], po[1], color='blue')
        for pp in right_coords:
            pc.addUserDebugPoints([[pp[0], pp[1], 0]], [[0, 1, 0]])
        for pp in left_coords:
            pc.addUserDebugPoints([[pp[0], pp[1], 0]], [[0, 0, 1]])
        pc.configureDebugVisualizer(pc.COV_ENABLE_RENDERING,1)        
    
        #step1
        
        pc.resetJointState(gripper, 0, targetValue=(-135*math.pi/180))   
        pc.resetJointState(gripper, 1, targetValue=(0*math.pi/180))   
        pc.resetJointState(gripper, 2, targetValue=(0*(math.pi/180)))
          
        pc.resetJointState(gripper, 4, targetValue=(math.pi))   
        #pc.resetJointState(gripper, 5, targetValue=(math.pi/2))
        pc.stepSimulation()
        time.sleep(1)
        
        
    
        #step3
        test_coords0.extend(self.move_theta(-135, -135+180, 0, pc, gripper))
        #step 4
    
        test_coords0.extend(self.move_theta(0, 90, 1, pc, gripper))
        test_coords0.extend(self.move_theta(0, 90, 2, pc, gripper))
    
        #step5
        test_coords0.extend(self.move_theta_reverse(-135+180, -135, 0, pc, gripper))
        #step6
        test_coords0.extend(self.move_theta_reverse(90, 0, 1, pc, gripper))
        test_coords0.extend(self.move_theta_reverse(90, 0, 2, pc, gripper))
        
        
        
        #pc.resetJointState(gripper, 0, targetValue=(math.pi))   
        pc.resetJointState(gripper, 1, targetValue=(-135*math.pi/180))   
        #pc.resetJointState(gripper, 2, targetValue=(0))
        pc.resetJointState(gripper, 4, targetValue=(135*math.pi/180))  
        pc.resetJointState(gripper, 5, targetValue=(0*math.pi/180))   
        pc.resetJointState(gripper, 6, targetValue=(0*math.pi/180))
        time.sleep(1)
        

        test_coords1.extend(self.move_theta_reverse(135, 135-180, 4, pc, gripper))
        #step 4
    
        test_coords1.extend(self.move_theta_reverse(0, -90, 5, pc, gripper))
        test_coords1.extend(self.move_theta_reverse(0, -90, 6, pc, gripper))
    
        #step5
        test_coords1.extend(self.move_theta(135-180, 135, 4, pc, gripper))
        #step6
        test_coords1.extend(self.move_theta(-90, 0, 5, pc, gripper))
        test_coords1.extend(self.move_theta(-90, 0, 6, pc, gripper))
        
        p.disconnect()  
        return np.asarray(right_coords), np.asarray(left_coords)  
            
    def raycasting(self, x_arr, y_arr, points):
        
        inside_indices = []
        _eps = 0.00001
        _huge = np.inf
        for idx, i in enumerate(points):
            
            inside = 0
            for j in range(len(x_arr)-1):
        
                #for edge in range(len(j)-1):
                    
                A = [x_arr[j], y_arr[j]]
                B = [x_arr[j+1], y_arr[j+1]]
        
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
                #print(inside)
                #self.inside_points.append(i)
                inside_indices.append(idx)
                
                
            #else:
                #self.outside_points.append(i)
                #plt.scatter(i[0],i[1], color='red')   
                   
        return inside_indices
        
    
    def fitness(self, inside_indicies_0, inside_indicies_1, points0, points1):
        
        idx = [i for i in inside_indicies_0 if i in inside_indicies_1]
        #fitness = len(idx)/(len(points0))
        i0 = []
        i1=[]
        po = []
        for p in idx:
            
            if points0[p][0] < self.width/2 and points0[p][0] > -abs(self.width)/2 and points0[p][1] <0:
                print("removed")
                points0.pop(p)
            else:
                plt.scatter(points0[p][0], points0[p][1], color='green') 
                i0.append(p)                
            if points1[p][0] < self.width/2 and points1[p][0] > -abs(self.width)/2 and points1[p][1] <0:
                print("removed")
                points1.pop(p)
            else:
                      
                plt.scatter(points1[p][0], points1[p][1], color = 'yellow')
                i1.append(p)
        fitness = ((len(i0)+len(i1))/2)/((len(points0)+len(points1))/2)       
        return fitness, points0, points1     
    
    
     
if __name__ == "__main__":
    #[0.06912, 0.0648, 0.01008]
    #palm leng 0.05386
    #h 0.053
    width = 0.05386
    height = 0.053
    l1 = 0.06911999999999999 + 0.0108# + 0.00925
    l2 = 0.0648 + 0.0108# + 0.00925
    l3 = 0.01008 + 0.0108
    f = WorkSpace_Test("../output/hand_mut_gen_2_f/hand", "hand_mut_gen_2_f", l1, l2, l3, width, height)
    #fitness = f.main()
    right_coords = f.build_coord_space_right()
    left_coords = f.build_coord_space_left()
    fitness = f.main(right_coords, left_coords)
    print(fitness)
    plt.axis('equal')
    plt.show()
    print("done")
   

