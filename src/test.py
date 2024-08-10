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
import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon



class WorkSpace_Test:

    def __init__(self, name, hand_data):

        self.name = name
        self.rad = 0.039/2
        self.hand_data = hand_data
        self.width = 0
        self.fitness_data = Dict()
        self.max_finger_length = max(self.hand_data.length.finger_0, self.hand_data.length.finger_1)
        self.fitness_test = 0
        
    def main(self):
        seg_lengths0, seg_lengths1 = self.get_data()
        right_coords = self.build_coord_space_right(seg_lengths0)
        left_coords = self.build_coord_space_left(seg_lengths1)
        #c_a, r_a, l_a = self.angles_coordinates(right_coords, left_coords)
        #c_s, r_s, l_s = self.straight_coordinates(0.02, right_coords, left_coords)
        c_s = self.area_coordinates(0.02, right_coords, left_coords)
        self.fitness_data.name = self.name
        self.fitness_data.coord_space_right = right_coords.tolist()
        self.fitness_data.coord_space_left = left_coords.tolist()
        self.fitness_data.width = self.width
        area_ans = abs(self.area_test(right_coords, left_coords, c_s))
        print(self.name)
        print(area_ans)
        
        #angles_ans = self.angles_test(right_coords, left_coords, c_a, r_a, l_a)
        #print(angles_ans)
        #straight_ans = self.straight_test(right_coords, left_coords, c_s, r_s, l_s)
        #print(straight_ans)
        self.fitness_data.update()
        self.save_data()
        
        
        
        return area_ans #, angles_ans, straight_ans
        
    def save_data(self):
        with open(f"../points/{self.name}.json", mode="w") as dataFile:
            new_j = json.dumps(self.fitness_data)
            dataFile.write(new_j)
            dataFile.close()
    
    
    def get_data(self):
        segs0 = self.hand_data.finger_0.num_segs
        segs1 = self.hand_data.finger_1.num_segs
        
        
        self.width = self.hand_data.length.palm
        
        finger_0_length = self.hand_data.length.finger_0
        finger_1_length = self.hand_data.length.finger_1

        
           
        
        list_ratios0 = self.hand_data.ratio.segs.finger_0
        list_ratios1 = self.hand_data.ratio.segs.finger_1
        
        seg_lengths0 = [finger_0_length*(x/100) for x in list_ratios0]
        seg_lengths1 = [finger_1_length*(x/100) for x in list_ratios1]
        
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
        
        for i in reversed(range(135-180, 135)):
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
        
        
    def mathy_thing(self, theta1, theta2, theta3, l1, l2, l3):
        theta1 = np.pi * theta1 / 180
        theta2 = np.pi * theta2 / 180
        theta3 = np.pi * theta3 / 180
        val = 90 * np.pi/180
        
        
        x = l1 *np.cos(theta1 + val) + l2*np.cos(theta1+theta2 + val) + l3*np.cos(theta1 + theta2 + theta3 + val) + self.width/2
        y = l1 * np.sin(theta1 + val) + l2*np.sin(theta1 + theta2 + val) + l3*np.sin(theta1 + theta2 + theta3 + val)
        
        
        return [x, y]
        
    def mathy_thing1(self, theta1, theta2, theta3, l4, l5, l6):
        theta1 = np.pi * theta1 / 180
        theta2 = np.pi * theta2 / 180
        theta3 = np.pi * theta3 / 180
        val = 90 * np.pi/180
        
        
        x = l4 *np.cos(theta1 + val) + l5*np.cos(theta1+theta2 + val) + l6*np.cos(theta1 + theta2 + theta3 + val) - self.width/2
        y = l4 * np.sin(theta1 + val) + l5*np.sin(theta1 + theta2 + val) + l6*np.sin(theta1 + theta2 + theta3 + val)
        
        
        return [x, y]

    def area_test(self, r, l, coords):
        insidex = []
        insidey = []
        inside = []
        inside_x_ls = []
        inside_y_ls = []
        iinside = []
        ans = 0
        
        ind = self.straight_raycasting(r, coords)
        
        ind2 = self.straight_raycasting(l, coords)
        
        inside.extend(list(coords[i]) for i in range(len(coords)) if i in ind and i in ind2)

        #inside.extend([list(coords[i]) for i in range(len(coords)) if i in ind])
        #inside.extend([list(r[i]) for i in range(len(r)) if i in ind2])
        
        
        ans = len(inside)
        
        inside_x, inside_y = np.hsplit(np.asarray(inside), 2)
        
        self.fitness_data.area_outline_x = inside_x.tolist()
        self.fitness_data.area_outline_y = inside_y.tolist()
        self.fitness_data.update()
        """
        for i in range(len(l)):
            if i in ind:
                if l[i][1] >= 0:
                    inside.append(l[i])
                    insidex.append(l[i][0])
                    insidey.append(l[i][1])
                
            
        for i in range(len(r)):
            if i in ind2:
                if r[i][1] >= 0:
                    inside.append(r[i])
                    insidex.append(r[i][0])
                    insidey.append(r[i][1])

        try:
            polygon = Polygon(inside)
            
        except:
            ans = 0
        else:
            ans = polygon.area
        
        
        for i in r:
            ri.append([i[0], i[1]])
        for i in l:
            le.append([i[0], i[1]])
        
        
       
        
        ind3 = self.straight_raycasting(inside, coords)    
        
        
        iinside = np.asarray(iinside)
        
        zero_mask = np.all(iinside == 0, axis=(1, 2))
        

        zero_indices = np.where(zero_mask)[0]

        arrs = iinside[~zero_mask]
        
        
        #split_indices = zero_indices - np.arange(len(zero_indices))
        #arrs = np.split(no_zeros, split_indices)
        
        if (len(arrs) <100):
            for a in arrs:
                
                if len(a) != 0:
                    reshaped = a.reshape(-1, 2)
                    no_zeros = reshaped[~np.all(reshaped == [0, 0], axis=1)]
                    inside_pts = np.split(no_zeros, 2, axis=1)

                    

                    area = np.trapz(inside_pts[1], x=inside_pts[0], axis=0)[0]
                    ans = ans + area
                    inside_x_ls.extend(inside_pts[0].tolist())
                    inside_y_ls.extend(inside_pts[1].tolist())
        else:
            reshaped = arrs.reshape(-1, 2)
            no_zeros = reshaped[~np.all(reshaped == [0, 0], axis=1)]
            inside_pts = np.split(no_zeros, 2, axis=1)
            
            ans = np.trapz(inside_pts[1], x=inside_pts[0], axis=0)[0]
            
            inside_x_ls.extend(inside_pts[0].tolist())
            inside_y_ls.extend(inside_pts[1].tolist())
        #outline_points = list(zip(insidex, insidey))
        
        """
        
        
        return ans
       
    def angles_test(self, ri, le, cent, r, l):
        count0 = []
        inside_0 = []
        count1 = []
        inside_1 = []
        angles0 = []
        angles1 = []

      
        for i, ele in enumerate(r):
            
            angles = self.angles_raycasting(ri, ele)
            angles0.append(angles)
            count = len(angles)
            
            if count != 0:
                inside_0.append(i)
                count0.append(count)
                
        for i, ele in enumerate(l):
            angles = self.angles_raycasting(le, ele)
            count = len(angles)
            angles1.append(angles)
         
            if count != 0:
                inside_1.append(i)
                count1.append(count)
                
        
        
        
        ct = 0
        idx = []
        
        
        for i in range(len(inside_0)):
            count = 0
            
            if inside_0[i] in inside_1:
                for a in angles0[inside_0[i]]:
                    if a in angles1[inside_0[i]]:
                         count = count + 1
                if count != 0:
                    
                    idx.append([inside_0[i], count])
                    ct = ct + count
        
        
        
        c = []
        for i in idx:
            j = i[0]
            c.append(cent[j])
        if len(c)!=0:
            fitness = ct
            centersx = np.split(np.asarray(c), 2, 1)[0]
        
            centersy = np.split(np.asarray(c), 2, 1)[1]
            cnt = np.split(np.asarray(idx), 2, 1)[1]
            self.fitness_data.angle_data.centersx = centersx.tolist()
            self.fitness_data.angle_data.centersy = centersy.tolist()
            self.fitness_data.angle_data.count = cnt.tolist()
            self.fitness_data.update()
        else:
            self.fitness_data.angle_data.centersx = []
            self.fitness_data.angle_data.centersy = []
            self.fitness_data.angle_data.count = []
            self.fitness_data.update()
            fitness = 0
        return fitness
    
    def angles_raycasting(self, arr, points):
        angles = []
        for idx, i in enumerate(points):
            if i[0] < self.width/2 and i[0] > -abs(self.width)/2 and i[1] <0:
                continue
            else:
                point = Point(i)
                polygon = Polygon(arr)
                if polygon.contains(point):
                    angles.append(idx)

           
        return angles
        

    def straight_test(self, ri, le, cent, r, l): 

        inside_indicies0 = self.straight_raycasting(ri, r)
        
        inside_indicies1 = self.straight_raycasting(le, l)
        
        idx = [i for i in inside_indicies0 if i in inside_indicies1]
        
        
        if len(idx) != 0:
            fitness = len(idx)
        else:
            fitness = 0
        self.fitness_data.straight_data = idx
        self.fitness_data.update()
              
        return fitness
    
    def straight_raycasting(self, arr, points):
        
        inside_indices = []
        polygon = Polygon(arr)
        for idx, i in enumerate(points):
            if i[0] < self.width/2 and i[0] > -abs(self.width)/2 and i[1] <0:
                continue
            else:
                point = Point(i)
                
            
                if polygon.contains(point):
                    inside_indices.append(idx)
 
        return inside_indices
        
    def angles_coordinates(self, right_coords, left_coords):
        finger_z = 0.288
        val = 0.02
        rad = 0.039/2
        total_height = 0.288
        x_out0, y_out0 = np.split(right_coords, 2, axis=1)
        x_out1, y_out1 = np.split(left_coords, 2, axis=1)
        bottom_x = -abs(total_height + 0.1)
        bottom_y = -abs(total_height + 0.1)
        row_length = finger_z - bottom_x
        column_length = finger_z - bottom_y
        row_points = int(row_length/val)
        column_points = int(column_length/val)
        n = 8
        
        center_pt = [[x, y] for x in np.linspace(bottom_x, finger_z, num=row_points) for y in np.linspace(bottom_y, finger_z, num=column_points)]
        self.fitness_test = len(center_pt)
        for i in center_pt:
            if i[0] < self.width/2 and i[0] > -abs(self.width)/2 and i[1] <0:
                
                center_pt.remove(i)
            elif i[0] <min(x_out0) or i[0] > max(x_out0) or i[0] < min(x_out1) or i[0] > max(x_out1):
                center_pt.remove(i)
            elif i[1] <min(y_out0) or i[1] > max(y_out0) or i[1] < min(y_out1) or i[1] > max(y_out1):
                center_pt.remove(i)
                
        angles = np.linspace(0, 2*np.pi, n, endpoint=False)
        
        x1 = [(c[0] + (np.cos(a)*rad)) for c in center_pt for a in angles]
    
   
        y1 = [(c[1] + (np.sin(a)*rad)) for c in center_pt for a in angles]
        
        coords1 = list(zip(x1, y1))
        angles = [a+np.pi for a in angles]
        x2 = [(c[0] + (np.cos(a)*rad)) for c in center_pt for a in angles]
    
   
        y2 = [(c[1] + (np.sin(a)*rad))for c in center_pt for a in angles]
        
        coords2 = list(zip(x2, y2))
        
        c1 = np.reshape(np.asarray(coords1), (-1, n, 2))
        c2 = np.reshape(np.asarray(coords2), (-1, n, 2))
          
        r = np.asarray(coords1)
        l = np.asarray(coords2)
        
        return center_pt, c1, c2

    def straight_coordinates(self, val, right_coords, left_coords):
        finger_z = 0.288
        
        
        x_out0, y_out0 = np.split(right_coords, 2, axis=1)
        x_out1, y_out1 = np.split(left_coords, 2, axis=1)
        total_height = 0.288
        coords1 = []
        coords2 = []
        bottom_x = -abs(total_height + 0.1)
        bottom_y = -abs(total_height + 0.1)
        row_length = finger_z - bottom_x
        column_length = finger_z - bottom_y
        row_points = int(row_length/val)
        column_points = int(column_length/val)
        n = 8
        rad = 0.039/2
      
        center_pt = [[x, y] for x in np.linspace(bottom_x, finger_z, num=row_points) for y in np.linspace(bottom_y, finger_z, num=column_points)]
        
        for i in center_pt:
            if i[0] < self.width/2 and i[0] > -abs(self.width)/2 and i[1] < 0:
                
                center_pt.remove(i)
            elif i[0] <min(x_out0) or i[0] > max(x_out0) or i[0] < min(x_out1) or i[0] > max(x_out1):
                center_pt.remove(i)
            elif i[1] <min(y_out0) or i[1] > max(y_out0) or i[1] < min(y_out1) or i[1] > max(y_out1):
                center_pt.remove(i)
                
        x1 = [(c[0] + rad) for c in center_pt]
        y1 = [c[1] for c in center_pt]
        
        
        coords1 = list(zip(x1, y1))
        
        x2 = [(c[0] - rad) for c in center_pt]
        y2 = [c[1] for c in center_pt]
        
        coords2 = list(zip(x2, y2))
        
        
        r = np.asarray(coords1)
        l = np.asarray(coords2)
        
        return center_pt, r, l
      
        

    def area_coordinates(self, val, right_coords, left_coords):
        finger_z = 0.288
        
        
        x_out0, y_out0 = np.split(right_coords, 2, axis=1)
        x_out1, y_out1 = np.split(left_coords, 2, axis=1)
        total_height = 0.288
        coords1 = []
        coords2 = []
        bottom_x = -abs(total_height + 0.1)
        bottom_y = -abs(total_height + 0.1)
        row_length = finger_z - bottom_x
        column_length = finger_z - bottom_y
        row_points = int(row_length/val)
        column_points = int(column_length/val)
        n = 8
        rad = 0.039/2
        
        center_pt = [[x, y] for x in np.linspace(bottom_x, finger_z, num=row_points) for y in np.linspace(bottom_y, finger_z, num=column_points)]
        
        for i in center_pt:
            if i[0] < self.width/2 and i[0] > -abs(self.width)/2 and i[1] < 0:
                
                center_pt.remove(i)
            elif i[0] <min(x_out0) or i[0] > max(x_out0) or i[0] < min(x_out1) or i[0] > max(x_out1):
                center_pt.remove(i)
            elif i[1] <min(y_out0) or i[1] > max(y_out0) or i[1] < min(y_out1) or i[1] > max(y_out1):
                center_pt.remove(i)
        
        
        return center_pt
