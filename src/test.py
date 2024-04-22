import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib import path
from matplotlib.lines import Line2D
import main
import build_hand as bh
import basic_load
from addict import Dict
import time
import math
from scipy.optimize import curve_fit
from scipy import integrate
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
from addict import Dict


class WorkSpace_Test:

    def __init__(self, loc, name, hand_data):

        self.name = name
        self.rad = 0.039/2
        self.hand_data = hand_data
        self.width = 0
        self.fitness_data = Dict()
        
    def main(self, c_a, r_a, l_a, c_s, r_s, l_s):
        seg_lengths0, seg_lengths1 = self.get_data()
        right_coords = self.build_coord_space_right(seg_lengths0)
        left_coords = self.build_coord_space_left(seg_lengths1)
        self.fitness_data.name = self.name
        self.fitness_data.coord_space_right = right_coords
        self.fitness_data.coord_space_left = left_coords
        area_ans = self.area_test(right_coords, left_coords, c_a, r_a, l_a)
        angles_ans = self.angles_test(right_coords, left_coords, c_s, r_s, l_s)
        straight_ans = self.straight_test(right_coords, left_coords)
        
        return area_ans, angles_ans, straight_ans
        
    def save_data(self):
        with open(f"../output/{self.name}", mode="w") as dataFile:
            
    
    def get_data(self):
        segs0 = self.hand_data.finger_0.num_segs
        segs1 = self.hand_data.finger_1.num_segs
        
        
        self.width = self.hand_data.length.palm
        
        finger_0_length = self.hand_data.length.finger_0
        finger_1_length = self.hand_data.length.finger_1

        
           
        
        list_ratios0 = self.hand_data.ratio.segs.finger_0
        list_ratios1 = self.hand_data.ratio.segs.finger_1
        
        seg_lengths0 = [x * finger_0_length for x in list_ratios0]
        seg_lengths1 = [x * finger_1_length for x in list_ratios1]
        
        if len(seg_lengths0) == 2:
            seg_lengths0.append(0)
        if len(seg_lengths1) == 2:
            seg_lengths1.append(0)
            
        return seg_lengths0, seg_lengths1
    
    def build_coord_space_right(self, seg_lengths0):
        
        right_coords = []
        
        for i in range(-135, -135+180):
            right_coords.append(self.mathy_thing(i, 0, 0, seg_lengths0[0], seg_lengths0[1], seg_lengths0[2]))
        for i in range(0, 90):
            right_coords.append(self.mathy_thing(-135+180, i, 0, seg_lengths0[0], seg_lengths0[1], seg_lengths0[2]))
        for i in range(0, 90):
            right_coords.append(self.mathy_thing(-135+180, 90, i, seg_lengths0[0], seg_lengths0[1], seg_lengths0[2]))
        for i in reversed(range(-135, -135+180)):
            right_coords.append(self.mathy_thing(i, 90, 90, seg_lengths0[0], seg_lengths0[1], seg_lengths0[2]))
        for i in reversed(range(0, 90)):
            right_coords.append(self.mathy_thing(-135, i, 90, seg_lengths0[0], seg_lengths0[1], seg_lengths0[2]))
        for i in reversed(range(0, 90)):
            right_coords.append(self.mathy_thing(-135, 0, i, seg_lengths0[0], seg_lengths0[1], seg_lengths0[2]))
        
        
        return np.asarray(right_coords)
        
    def build_coord_space_left(self, seg_lengths1):
        left_coords = []
        
        for i in reversed(range(135-180, 135, seg_lengths1[0], seg_lengths1[1], seg_lengths1[2])):
            left_coords.append(self.mathy_thing1(i, 0, 0, seg_lengths1[0], seg_lengths1[1], seg_lengths1[2]))
        for i in reversed(range(-90, 0)):
            left_coords.append(self.mathy_thing1(135-180, i, 0, seg_lengths1[0], seg_lengths1[1], seg_lengths1[2]))
        for i in reversed(range(-90, 0)):
            left_coords.append(self.mathy_thing1(135-180, -90, i, seg_lengths1[0], seg_lengths1[1], seg_lengths1[2]))
        for i in range(135-180, 135):
            left_coords.append(self.mathy_thing1(i, -90, -90, seg_lengths1[0], seg_lengths1[1], seg_lengths1[2]))
        for i in range(-90, 0):
            left_coords.append(self.mathy_thing1(135, i, -90, seg_lengths1[0], seg_lengths1[1], seg_lengths1[2]))
        for i in range(-90, 0):
            left_coords.append(self.mathy_thing1(135, 0, i, seg_lengths1[0], seg_lengths1[1], seg_lengths1[2]))
        
        return np.asarray(left_coords)    
        
        
    def mathy_thing(self, theta1, theta2, theta, seg_lengths0, seg_lengths0, seg_lengths0):
        theta1 = np.pi * theta1 / 180
        theta2 = np.pi * theta2 / 180
        theta3 = np.pi * theta3 / 180
        val = 90 * np.pi/180
        
        
        x = self.l1 *np.cos(theta1 + val) + self.l2*np.cos(theta1+theta2 + val) + self.l3*np.cos(theta1 + theta2 + theta3 + val) + self.width/2
        y = self.l1 * np.sin(theta1 + val) + self.l2*np.sin(theta1 + theta2 + val) + self.l3*np.sin(theta1 + theta2 + theta3 + val)
        
        
        return [x, y]
        
    def mathy_thing1(self, theta1, theta2, theta3, seg_lengths1, seg_lengths1, seg_lengths1):
        theta1 = np.pi * theta1 / 180
        theta2 = np.pi * theta2 / 180
        theta3 = np.pi * theta3 / 180
        val = 90 * np.pi/180
        
        
        x = self.l4 *np.cos(theta1 + val) + self.l5*np.cos(theta1+theta2 + val) + self.l6*np.cos(theta1 + theta2 + theta3 + val) - self.width/2
        y = self.l4 * np.sin(theta1 + val) + self.l5*np.sin(theta1 + theta2 + val) + self.l6*np.sin(theta1 + theta2 + theta3 + val)
        
        
        return [x, y]
        

    

    def area_test(self, r, l):
        x = []
        y = []
        x2 = []
        y2 = []
        insidex = []
        insidey = []
        for i in r:
            x.append(i[0])
            y.append(i[1])
        for i in l:
            x2.append(i[0])
            y2.append(i[1])
        ind = self.raycasting(x, y, l)
        ind2 = self.raycasting(x2, y2, r)
        for i in ind:
            insidex.append(l[i][0])
            insidey.append(l[i][1])
            
        for i in ind2:
            insidex.append(r[i][0])
            insidey.append(r[i][1])
            
        ans = integrate.trapezoid(insidey, x=insidex, axis=0)
        self.fitness_data.area_outline = [insidex, insidey]
        self.fitness_data.update()
        return ans
        
    def angles_test(self, ri, le, cent, r, l):
        
        x_arr0 = np.split(ri, 2, 1)[0]
        
        y_arr0 =  np.split(ri, 2, 1)[1]
        
        x_arr1 = np.split(le, 2, 1)[0]
        y_arr1 =  np.split(le, 2, 1)[1]
        
        for i, ele in enumerate(r):
            
            angles = self.angles_raycasting(x_arr0, y_arr0, ele)
            angles0.append(angles)
            count = len(angles)
            
            if count != 0:
                inside_0.append(i)
                count0.append(count)
                
        for i, ele in enumerate(l):
            angles = self.angles_raycasting(x_arr1, y_arr1, ele)
            count = len(angles)
            angles1.append(angles)
         
            if count != 0:
                inside_1.append(i)
                count1.append(count)
                
        
        
        
        ct = []
        idx = []
        
        for i in range(len(inside_indicies_0)):
            count = 0
            if inside_indicies_0[i] in inside_indicies_1:
                for a in angles0[inside_indicies_0[i]]:
                    if a in angles1[inside_indicies_0[i]]:
                         count = count + 1
                if count != 0:
                    
                    idx.append([inside_indicies_0[i], count])
                    ct.append(count)
        
        
        
        c = []
        for i in idx:
            j = i[0]
            c.append(cent[j])
        
        fitness = sum(ct)/(len(cent)*8)
        centersx = np.split(np.asarray(c), 2, 1)[0]
        
        centersy = np.split(np.asarray(c), 2, 1)[1]
        cnt = np.split(np.asarray(idx), 2, 1)[1]
        self.fitness_data.angle_data.centersx = centersx
        self.fitness_data.angle_data.centersy = centersy
        self.fitness_data.angle_data.count = cnt
        self.fitness_data.update()
        
        return fitness
    
    def angles_raycasting(self, x_arr, y_arr, points):
        
        inside_indices = []
        outside_points = []
        _eps = 0.00001
        _huge = np.inf
        inside = False
        count = 0
        angles = []
        for idx, i in enumerate(points):
            
            inside = 0
            for j in range(len(x_arr)-1):
        
                
                    
                A = [x_arr[j], y_arr[j]]
                B = [x_arr[j+1], y_arr[j+1]]
        
                if A[1] > B[1]:
                    A, B = B, A
                if i[1] == A[1] or i[1] == B[1]:
                    i[1] += _eps
                
                  
                if i[1] > B[1] or i[1] < A[1] or i[0] > max(A[0], B[0]):
                    continue

                if i[0] < min(A[0], B[0]):
                    inside = not inside
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
                    inside = not inside
                    continue

            if inside:
               
                
                angles.append(idx)

                  
        return angles
        

    def straight_test(self, ri, le, cent, r, l): 
        
        
        
        
        
        x_arr0 = np.split(ri, 2, 1)[0]
        
        y_arr0 =  np.split(ri, 2, 1)[1]
        
        x_arr1 = np.split(le, 2, 1)[0]
        y_arr1 =  np.split(le, 2, 1)[1]
        
        
        inside_indicies0 = self.straight_raycasting(x_arr0, y_arr0, r)
        
        inside_indicies1 = self.straight_raycasting(x_arr1, y_arr1, l)
        
        idx = [i for i in inside_indicies_0 if i in inside_indicies_1]
        fitness = len(idx)/len(cent)       
        return fitness
    
    def straight_raycasting(self, x_arr, y_arr, points):
        
        inside_indices = []
        
        _eps = 0.00001
        _huge = np.inf
        inside = False
        for idx, i in enumerate(points):
            
            inside = 0
            for j in range(len(x_arr)-1):
        
                
                    
                A = [x_arr[j], y_arr[j]]
                B = [x_arr[j+1], y_arr[j+1]]
        
                if A[1] > B[1]:
                    A, B = B, A
                if i[1] == A[1] or i[1] == B[1]:
                    i[1] += _eps
                
                  
                if i[1] > B[1] or i[1] < A[1] or i[0] > max(A[0], B[0]):
                    continue

                if i[0] < min(A[0], B[0]):
                    inside = not inside
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
                    inside = not inside
                    continue

            if inside:
                
                inside_indices.append(idx)
                
            
        return inside_indices
        
        
        
        
        
#source:http://www.philliplemons.com/posts/ray-casting-algorithm 
