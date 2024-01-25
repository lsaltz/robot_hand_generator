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

    def __init__(self, links, width, finger_name, points):
        self.link0 = links[0]
        self.link1 = links[1]
        self.link2 = links[2]
        self.finger_name = finger_name
        self.width = width
        self.points = points
        self.N = 100
        self.cube = 0.039
        self.h = 0.032
        self.inside_points = []
        self.outside_points = []
        
        
        
    def decide_angles(self, index):
        if self.finger_name == "finger_0":
            if index == 0:
                theta1 = -135
                theta2 = 135
            else:
                theta1 = 0
                theta2 = 180
            
        else:
            theta1 = 45
            theta2 = 225
            
        return theta1, theta2
        
    
    def make_angle_arrays(self, theta1, theta2):
        
        theta_rad = [theta1, theta2]
        theta_rad = [i * np.pi/180 for i in theta_rad]
        theta_arr = np.linspace(theta1,theta2, self.N)
        theta_arr = theta_arr * np.pi/180
        
        return theta_arr, theta_rad 
        
    
    def build_workspace_right(self, theta_arr, theta_arr2, theta_arr3):
    
        x3 = np.zeros(2*len(theta_arr), len(theta_ar)
        y3 = np.zeros(2*len(theta_arr))
        
        """
        for i in range(len(theta_arr)):
            
           
            for j in range(len(theta_arr2)):
                x1 = self.link0*np.cos(theta_arr[i])
                y1 = self.link0*np.sin(theta_arr[i])
                x2 = x1 + self.link1*np.cos(theta_arr2[j]+theta_arr[i])
                y2 = y1 + self.link1*np.sin(theta_arr2[j]+theta_arr[i])
                
          
                # if i in(0, 2*len(theta_arr)-1) or j in(0,(len(theta_arr)-1)):
                    
                x3[j] = (x2 + self.link2*np.cos(theta_arr3[j] + theta_arr2[j]+theta_arr[j]) + self.width)
                y3[j] = (y2 + self.link2*np.sin(theta_arr3[j] + theta_arr2[j]+theta_arr[j]) + self.h)

        """
        for i in range(0,2):
            for j in range(0, len(theta_arr)):
                x_arr[i,j] = self.width + self.link0*np.cos(theta_arr[j]) + self.link1*np.cos(theta_arr[j] + theta_rad2[i]) + self.link2*np.cos(theta_arr2[j] + theta_rad2[i] + theta_rad2[i])
                y_arr[i,j] = self.link0*np.sin(theta_arr[j]) + self.link1*np.sin(theta_arr[j] + theta_rad2[i]) + self.link2*np.sin(theta_arr[j] + theta_rad[i] + theta_rad2[i]) + self.h
            for k in range(0, len(theta_arr)):
                x_arr[i+2,k] = self.width + self.link0*np.cos(theta_rad[i]) + self.link1*np.cos(theta_arr2[k] + theta_rad[i]) + self.link2*np.cos(theta_arr2[k] + theta_rad[i] + theta_arr[k])
                y_arr[i+2,k] = self.link0*np.sin(theta_rad[i]) + self.link1*np.sin(theta_arr2[k] + theta_rad[i]) + self.link2*np.sin(theta_arr2[k] + theta_rad[i] + theta_arr[k]) + self.h
        
        #plt.plot(x3, y3, color='blue') 
        
        return x3, y3         
    
    
    def build_workspace_left(self, theta_arr, theta_rad):
        x_arr = np.zeros((2*len(theta_arr), len(theta_arr)))
        y_arr = np.zeros((2*len(theta_arr), len(theta_arr)))
        
        for i in range(0,2):
            for j in range(0, len(theta_arr)):
                x_arr[i,j] = self.link0*np.cos(theta_arr[j]) - self.link1*np.cos(theta_arr[j]+ theta_rad[i]) + self.link2*np.cos(theta_arr[j]+ theta_rad[i] + theta_rad[i])
                
                y_arr[i,j] = self.link0*np.sin(theta_arr[j]) - self.link1*np.sin(theta_arr[j]+ theta_rad[i]) + self.link2*np.sin(theta_arr[j]+ theta_rad[i] + theta_rad[i])
            for k in range(0, len(theta_arr)):
                x_arr[i+2,k] = self.link0*np.cos(theta_rad[i]) - self.link1*np.cos(theta_arr[k]+ theta_rad[i]) + self.link2*np.cos(theta_arr[k] + theta_rad[i] + theta_arr[k])
                y_arr[i+2,k] = self.link0*np.sin(theta_rad[i]) - self.link1*np.sin(theta_arr[k]+ theta_rad[i]) + self.link2*np.sin(theta_arr[k] + theta_rad[i] + theta_arr[k]) 
        plt.plot(x_arr.T, y_arr.T, color='blue')         
        return x_arr, y_arr
       
             
    def main(self):
    
        theta1, theta2 = self.decide_angles()
        theta_arr, theta_rad = self.make_angle_arrays(theta1, theta2)
        val = 0.03
        
        if self.finger_name == "finger_0":
            x_arr, y_arr = self.build_workspace_right(theta_arr, theta_rad)
            #points = np.asarray([[x+self.cube, y] for x in np.linspace(bottom_x, top_x, num_points) for y in np.linspace(bottom_y, top_y, num_points)])   
            inside_indices = self.raycasting(x_arr, y_arr)
        else:
            x_arr, y_arr = self.build_workspace_left(theta_arr, theta_rad)   
            #points = np.asarray([[x, y] for x in np.linspace(bottom_x, top_x, num_points) for y in np.linspace(bottom_y, top_y, num_points)])     #need to determine limits
            inside_indices = self.raycasting(x_arr, y_arr)
           
        return inside_indices, self.points
     
            
    def raycasting(self, x_arr, y_arr):
        
        inside_indices = []
        _eps = 0.00001
        _huge = np.inf
        for idx, i in enumerate(self.points):
            
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
        print(inside_indices)           
        return inside_indices
        
        
     
            
class WorkSpace_Fitness:

    def __init__(self, inside_indices_0, inside_indices_1, points0, points1):
        self.inside_indices_0 = inside_indices_0
        self.inside_indices_1 = inside_indices_1
        self.points0 = np.asarray(points0)
        self.points1 = np.asarray(points1)
    
    def main(self):
    
        idx = [i for i in self.inside_indices_0 if i in self.inside_indices_1]
        fitness = len(idx)/(len(self.points0))
        print(idx)
        for p in idx:
            plt.scatter(self.points0[p][0], self.points0[p][1], color='green')           
            plt.scatter(self.points1[p][0], self.points1[p][1], color = 'yellow')  
        #plt.show()    
        return fitness     
        
def coordinate_array(val):
    finger_z = 0.2
    
    
    total_height = 0.2
    coords0 = []
    coords1 = []
    bottom_x = -abs(total_height)
    bottom_y = -0.2
    row_length = finger_z - bottom_x
    column_length = finger_z - bottom_y
    row_points = 10
    column_points = 10
    n = 4
    rad = 0.0195
    
    center_pt = [[x, y, 0] for x in np.linspace(bottom_x, finger_z, num=row_points) for y in np.linspace(bottom_y, finger_z, num=column_points)]
    
    x1 = [(c[0] + (np.cos(np.pi/n*x + np.pi/2)*rad)) for c in center_pt for x in range(0, n+1)]
    
   
    y1 = [(c[1] + (np.sin(np.pi/n*x + np.pi/2)*rad)) for c in center_pt for x in range(0, n+1)]
    z1 = np.linspace(0, 0, len(x1))
    coords0 = np.asarray(list(zip(x1, y1, z1)))
    x2 = [(c[0] + (np.cos(np.pi/n*x+np.pi + np.pi/2)*rad)) for c in center_pt for x in reversed(range(0, n+1))]
    
    y2 = [((c[1] - (np.sin(np.pi/n*x+np.pi + np.pi/2)*rad))) for c in center_pt for x in reversed(range(0, n+1))]
    
    z2 = np.linspace(0, 0, len(x2))
    coords1 = np.asarray(list(zip(x2, y2, z2)))

    return coords0, coords1     
        
def open_file(name):
    
    rt = f"../output/{name}/hand"
    fittest_file = f"{rt}/{name}.urdf"
    basic_load.load(fittest_file) 
    
    
    
def run_sim(x, y, max_link, loc, name):
    pc = bc.BulletClient(connection_mode=p.GUI)    #or GUI for visual (slower)
    pc.configureDebugVisualizer(pc.COV_ENABLE_RENDERING,0)
    pc.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
    pc.setGravity(0, 0, 0)
        
    cubeStartPos = [0, 0, 1]
    cubeStartOrientation = pc.getQuaternionFromEuler([0, 0, 0])

    gripper = pc.loadURDF(f"{loc}/{name}.urdf", useFixedBase=1, flags=pc.URDF_USE_SELF_COLLISION_INCLUDE_PARENT) 
        
    pc.resetDebugVisualizerCamera(cameraDistance=.2, cameraYaw=180, cameraPitch=-91, cameraTargetPosition=[0, 0.1, 0.1])
    for i in range(len(x)):
            
        p.addUserDebugPoints([[x[i], y[i], 0]], [[1, 0, 0]])
    """
    for i, o in enumerate(x):
        
        for k in range(len(o)):
            
            p.addUserDebugPoints([[x[i][k], y[i][k], 0]], [[1, 0, 0]])
    """
    pc.configureDebugVisualizer(pc.COV_ENABLE_RENDERING,1)        
    #pc.changeDynamics(gripper, 0, jointLowerLimit=((math.pi)/4), jointUpperLimit=((5*math.pi)/4))
    #pc.changeDynamics(gripper, 1, jointLowerLimit=((math.pi)/4), jointUpperLimit=((5*math.pi)/4))
    pc.resetJointState(gripper, 0, targetValue=(-math.pi/4))   
    pc.resetJointState(gripper, 1, targetValue=(-math.pi/4))   
    pc.resetJointState(gripper, 2, targetValue=(-math.pi/4))  
    pc.resetJointState(gripper, 3, targetValue=(math.pi))   
    pc.resetJointState(gripper, 4, targetValue=(math.pi/2))   
    pc.resetJointState(gripper, 5, targetValue=(math.pi/2))   
    """
    for i, o in enumerate(x):
        
        for k in range(len(o)):
            idealJointPoses = p.calculateInverseKinematics(gripper, max_link, [x[i][k], y[i][k], 0], maxNumIterations=3000)   
            for j in range(max_link+1):
                #pc.setJointMotorControl2(gripper, j, controlMode=p.POSITION_CONTROL, targetPosition=idealJointPoses[j])
                pc.resetJointState(gripper, j, targetValue=idealJointPoses[j])    
                time.sleep(0.05)
            #pc.resetJointState(gripper, 0, targetValue=((5*math.pi)/4))
            #pc.resetJointState(gripper, 1, targetValue=(math.pi/2))
    """
    for i in range(len(x)):
        idealJointPoses = p.calculateInverseKinematics(gripper, max_link, [x[i], y[i], 0], maxNumIterations=3000)   
        for j in range(max_link+1):
            pc.resetJointState(gripper, j, targetValue=idealJointPoses[j])    
            time.sleep(0.05)
        pc.stepSimulation()        
            
        time.sleep(1. / 240.)
    
    p.disconnect()    
    
if __name__ == "__main__":

    coords0, coords1 = coordinate_array(0.03)
    links0 = [0.06912, 0.0648, 0.01008]
    #links0 = [f0l1, f0l2, f0l3]
    name0 = "finger_0"

    f1l1 = 0.05#0.0576
    f1l2 = 0.05#0.0864
    f1l3 = 0
    links1 = [0.01296, 0.06768, 0.06336]
    #links1 = [f1l1, f1l2, f1l3]
    name1 = "finger_1"

    width = 0.05386/2
    f = WorkSpace_Test(links0, width, name0, coords0)
    theta1, theta2 = f.decide_angles(0)
    theta_arr, theta_rad = f.make_angle_arrays(theta1, theta2)
    theta1, theta2 = f.decide_angles(1)
    theta_arr2, theta_rad2 = f.make_angle_arrays(theta1, theta2)
    
    x, y = f.build_workspace_right(theta_arr, theta_arr2, theta_arr2)
    l = Dict({'name': 'hand_mut_gen_2_f', 'finger_0': {'num_segs': 4}, 'finger_1': {'num_segs': 4}, 'ratio': {'segs': {'finger_0': [48, 45, 7], 'finger_1': [9, 47, 44]}, 'finger_0': 7, 'finger_1': 7}, 'length': {'palm': 0.05386, 'finger_0': 0.144, 'finger_1': 0.144}})
    
    #b = bh.Build_Json(l)
    #b.build_hand()
    #main.MainScript()
    run_sim(x, y, 3, "../output/hand_mut_gen_2_f/hand", "hand_mut_gen_2_f")
    #open_file("hand_mut_gen_2_f")
    #plt.axis('equal')
    #plt.show()
    print("done")
   
    
"""    
     
 f0l1 = 0.05904
    f0l2 = 0.0576
    f0l3 = 0.02736
    
    
    w = WorkSpace_Test(links0, width, name0, coords0)     
    i0, p0 = w.main()
    
    w2 = WorkSpace_Test(links1, 0, name1, coords1)
    i1, p1 = w2.main()
    rad = 0.0195
    f = WorkSpace_Fitness(i0, i1, p0, p1).main()   
f0l1_theta_2 = 135
f0l2_theta_1 = -45
f0l2_theta_2 = 135
f0l3_theta_1 = -45
f0l3_theta_2  = 135

f1l1_theta_1 = 45
f1l1_theta_2 = 225
f1l2_theta_1 = 45
f1l2_theta_2 = 225
f1l3_theta_1 = 45
f1l3_theta_2 = 225



f0_theta1 = [f0l1_theta_1, f0l1_theta_2]
f0_theta1 = [i * np.pi/180 for i in f0_theta1]

f0_theta2 = [f0l2_theta_1, f0l2_theta_2]
f0_theta2 = [i * np.pi/180 for i in f0_theta2]

f0_theta3 = [f0l3_theta_1, f0l3_theta_2]
f0_theta3 = [i * np.pi/180 for i in f0_theta3]

f1_theta1 = [f1l1_theta_1, f1l1_theta_2]
f1_theta1 = [i * np.pi/180 for i in f1_theta1]

f1_theta2 = [f1l2_theta_1, f1l2_theta_2]
f1_theta2 = [i * np.pi/180 for i in f1_theta2]

f1_theta3 = [f1l3_theta_1, f1l3_theta_2]
f1_theta3 = [i * np.pi/180 for i in f1_theta3]

f0theta_1 = np.linspace(f0l1_theta_1,f0l1_theta_2, N)
f0theta_1 = f0theta_1 * np.pi/180
f0theta_2 = np.linspace(f0l2_theta_1, f0l2_theta_2, N)
f0theta_2 = f0theta_2 * np.pi/180
f0theta_3 = np.linspace(f0l3_theta_1, f0l3_theta_1, N)
f0theta_3 = f0theta_3 * np.pi/180

f1theta_1 = np.linspace(f1l1_theta_1,f1l1_theta_2, N)
f1theta_1 = f1theta_1 * np.pi/180
f1theta_2 = np.linspace(f1l2_theta_1, f1l2_theta_2, N)
f1theta_2 = f1theta_2 * np.pi/180
f1theta_3 = np.linspace(f1l3_theta_1, f1l3_theta_1, N)
f1theta_3 = f1theta_3 * np.pi/180

x0 = np.zeros((2*len(f0theta_1), len(f0theta_2)))
y0 = np.zeros((2*len(f0theta_1), len(f0theta_2)))

x1 = np.zeros((2*len(f0theta_1), len(f0theta_2)))
y1 = np.zeros((2*len(f0theta_1), len(f0theta_2)))

l0 = np.zeros((2*len(f0theta_1), len(f0theta_2)))

for i in range(0,2):
    for j in range(0, len(f0theta_1)):
        x0[i,j] = width + f0l1*np.cos(f0theta_1[j]) + f0l2*np.cos(f0theta_1[j]+ f0_theta2[i]) + f0l3*np.cos(f0theta_1[j]+ f0_theta1[i] + f0_theta1[i])
        y0[i, j] = f0l1*np.sin(f0theta_1[j]) + f0l2*np.sin(f0theta_1[j]+ f0_theta2[i]) + f0l3*np.sin(f0theta_1[j]+ f0_theta1[i] + f0_theta1[i])
    for k in range(0, len(f0theta_1)):
        x0[i+2,k] = width + f0l1*np.cos(f0_theta1[i]) + f0l2*np.cos(f0theta_2[k]+ f0_theta1[i]) + f0l3*np.cos(f0theta_1[k]+ f0_theta1[i] + f0theta_1[k])
        y0[i+2, k] = f0l1*np.sin(f0_theta1[i]) + f0l2*np.sin(f0theta_2[k]+ f0_theta1[i]) + f0l3*np.sin(f0theta_1[k]+ f0_theta1[i] + f0theta_1[k])
    for l in range(0, len(f0theta_1)):
        x1[i,l] = f1l1*np.cos(f1theta_1[l]) - f1l2*np.cos(f1theta_1[l]+ f1_theta2[i]) + f1l3*np.cos(f1theta_1[l]+ f1_theta1[i] + f1_theta1[i])
        y1[i, l] = f1l1*np.sin(f1theta_1[l]) - f1l2*np.sin(f1theta_1[l]+ f1_theta2[i]) + f1l3*np.sin(f1theta_1[l]+ f1_theta1[i] + f1_theta1[i])
    for m in range(0, len(f0theta_1)):
        x1[i+2,m] = f1l1*np.cos(f1_theta1[i]) - f1l2*np.cos(f1theta_2[m]+ f1_theta1[i]) + f1l3*np.cos(f1theta_1[m]+ f1_theta1[i] + f1theta_1[m])
        y1[i+2, m] = f1l1*np.sin(f1_theta1[i]) - f1l2*np.sin(f1theta_2[m]+ f1_theta1[i]) + f1l3*np.sin(f1theta_1[m]+ f1_theta1[i] + f1theta_1[m])

begin = np.asarray([[x, y] for x in np.linspace(-0.1, 0.15, 20) for y in np.linspace(-0.1, 0.15, 20)])
end = np.asarray([[x+0.039, y] for x in np.linspace(-0.1, 0.15, 20) for y in np.linspace(-0.1, 0.15, 20)])
plt.plot(x0.T, y0.T, color='blue')


_eps = 0.00001
_huge = np.inf


for i in end:
    inside = 0
    for k,j in enumerate(x0):
        
        for edge in range(len(j)-1):
        
            A = [x0[k][edge], y0[k][edge]]
            B = [x0[k][edge+1], y0[k][edge+1]]
        
            if A[1] > B[1]:
                A, B = B, A
            if i[1] == A[1]:
                i[1] += _eps
            if i[1] == B[1]:
                i[1] -= _eps
            if i[1] > B[1] or i[1] < A[1] or i[0] > max(A[0], B[0]):
                # The horizontal ray does not intersect with the edge
                continue

            if i[0] < min(A[0], B[0]): # The ray intersects with the edge
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

            if m_point >= m_edge:
                # The ray intersects with the edge
                inside +=1
                continue

    if inside%2 != 0:
        plt.scatter(i[0],i[1], color='green')
              
    else:
        plt.scatter(i[0],i[1], color='red')
  
#for i in begin:
#    plt.scatter(i[0],i[1], color='yellow')
    



#fig, ax = plt.subplots()



#patch = patches.Polygon(a0, facecolor='orange')
#ax.add_patch(patch)
#plt.plot(x1.T, y1.T, color='red')


#x1 = np.array(x1).reshape(-1)
#y1 = np.array(y1).reshape(-1)

#m = np.asarray(list(zip(x0, y0))).reshape(-1, 2)

#ar1 = p.contains_points(begin, radius=1e-9)

#p2 = path.Path()

#ar0 = p2.contains_points(end, radius=1e-9)
iar = []


#for i in range(len(ar0)):
#    if ar0[i] == True:# and ar0[i] == ar1[i]:
#         iar.append(i)
#         print(i)
        
#for i in iar:
#    plt.scatter(begin[i][0], begin[i][1], color='orange')
#    plt.scatter(end[i][0], end[i][1], color='red')
plt.show()
"""
