import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib import path
from matplotlib.lines import Line2D

import matplotlib.patches as patches


"""
TODO:
3. integrate, loop through dictionaries of fingers, etc.
"""




class WorkSpace_Test:

    def __init__(self, link0, link1, link2, width, finger_name):
        self.link0 = link0
        self.link1 = link1
        self.link2 = link2
        self.finger_name = finger_name
        self.width = width
        self.N = 100
        self.cube = 0.039

        theta1 = -45
        theta2 = 135
        
        
    def decide_angles(self):
    
        if self.finger_name == "finger_0":
            theta1 = -45
            theta2 = 135
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
    
    def build_workspace_right(self, theta_arr, theta_rad):
    
        x_arr = np.zeros((2*len(theta_arr), len(theta_arr)))
        y_arr = np.zeros((2*len(theta_arr), len(theta_arr)))
        
        for i in range(0,2):
            for j in range(0, len(theta_arr)):
                x_arr[i,j] = self.width + self.link0*np.cos(theta_arr[j]) + self.link1*np.cos(theta_arr[j] + theta_rad[i]) + self.link2*np.cos(theta_arr[j] + theta_rad[i] + theta_rad[i])
                y_arr[i,j] = self.link0*np.sin(theta_arr[j]) + self.link1*np.sin(theta_arr[j] + theta_rad[i]) + self.link2*np.sin(theta_arr[j] + theta_rad[i] + theta_rad[i])
            for k in range(0, len(theta_arr)):
                x_arr[i+2,k] = self.width + self.link0*np.cos(theta_rad[i]) + self.link1*np.cos(theta_arr[k] + theta_rad[i]) + self.link2*np.cos(theta_arr[k] + theta_rad[i] + theta_arr[k])
                y_arr[i+2,k] = self.link0*np.sin(theta_rad[i]) + self.link1*np.sin(theta_arr[k] + theta_rad[i]) + self.link2*np.sin(theta_arr[k] + theta_rad[i] + theta_arr[k])
        
        return x_arr, y_arr         
    
    
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
                
        return x_arr, y_arr
       
               
    def main(self):
    
        theta1, theta2 = self.decide_angles()
        theta_arr, theta_rad = self.make_angle_arrays(theta1, theta2)
        
        if self.finger_name == "finger_0":
            x_arr, y_arr = self.build_workspace_right(theta_arr, theta_rad)
            points = np.asarray([[x+self.cube, y] for x in np.linspace(-0.1, 0.15, 20) for y in np.linspace(-0.1, 0.15, 20)])   
            inside_indices = self.raycasting(x_arr, y_arr, points)
        else:
            x_arr, y_arr = self.build_workspace_left(theta_arr, theta_rad)   
            points = np.asarray([[x, y] for x in np.linspace(-0.1, 0.15, 20) for y in np.linspace(-0.1, 0.15, 20)])    #need to determine limits
            inside_indices = self.raycasting(x_arr, y_arr, points)
            
        return inside_indices, points
     
            
    def raycasting(self, x_arr, y_arr, points):
        plt.plot(x_arr.T, y_arr.T, color='blue')
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
                inside_indices.append(idx)
              
            else:
                plt.scatter(i[0],i[1], color='red')   
                       
        return inside_indices
        
        
class WorkSpace_Fitness:

    def __init__(self, inside_indices_0, inside_indices_1, points0, points1):
        self.inside_indices_0 = inside_indices_0
        self.inside_indices_1 = inside_indices_1
        self.points0 = np.asarray(points0)
        self.points1 = np.asarray(points1)
    
    def main(self):
    
        idx = [i for i in self.inside_indices_0 if i in self.inside_indices_1]
        fitness = len(idx)/(len(self.points0)+len(self.points1))
        
        for p in idx:
            plt.scatter(self.points0[p][0], self.points0[p][1], color='green')           
            plt.scatter(self.points1[p][0], self.points1[p][1], color = 'yellow')  
            
        return fitness         

if __name__ == "__main__":
    
    f0l1 = 0.05904
    f0l2 = 0.0576
    f0l3 = 0.02736
    name0 = "finger_0"

    f1l1 = 0.0576
    f1l2 = 0.0864
    f1l3 = 0
    name1 = "finger_1"

    width = 0.05326 
    
    w = WorkSpace_Test(f0l1, f0l2, f0l3, width, name0)     
    i0, p0 = w.main()
    
    w2 = WorkSpace_Test(f1l1, f1l2, f1l3, 0, name1)
    i1, p1 = w2.main()
    f = WorkSpace_Fitness(i0, i1, p0, p1).main()
    print(f)
    plt.show()
    
    
    
     
"""         
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
