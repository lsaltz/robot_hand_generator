# By Marshall Saltz
import numpy as np
from addict import Dict
from addict import Dict
import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import params


class WorkSpace_Test:
    """
    Runs testing on grippers.
    """

    def __init__(self, name, hand_data, precision):
        """
        Initializes class.
        Parameters:
            name - gripper to test
            hand_data - dictionary of gripper measurements and ratios
            precision - coarse or fine, set in parameters
        """
        self.name = name
        self.rad = params.radius  # radius of distance
        self.hand_data = hand_data
        self.width = self.hand_data.length.palm # width of palm
        self.fitness_data = Dict()  # Dict() to store fitness data in
        self.precision = precision

        
    def main(self):
        """
        Runs testing methods.
        Returns:
            ans - fitness score
        """
        seg_lengths0, seg_lengths1 = self.get_data()
        right_coords = self.build_coord_space_right(seg_lengths0)
        left_coords = self.build_coord_space_left(seg_lengths1)

        if params.flag == "area":
            c_s = self.area_coordinates(self.precision, right_coords, left_coords)
            ans = abs(self.area_test(right_coords, left_coords, c_s))
        elif params.flag == "angle":
            c_a, r_a, l_a = self.angles_coordinates(right_coords, left_coords)
            ans = self.angles_test(right_coords, left_coords, c_a, r_a, l_a)
        else:
            r_s, l_s = self.straight_coordinates(self.precision, right_coords, left_coords)
            ans = self.straight_test(right_coords, left_coords, r_s, l_s)

        self.fitness_data.name = self.name
        self.fitness_data.coord_space_right = right_coords.tolist()
        self.fitness_data.coord_space_left = left_coords.tolist()
        self.fitness_data.width = self.width
        self.fitness_data.update()
        self.save_data()

        print(self.name)
        print(ans)

        return ans
    
        
    def save_data(self):
        """
        Saves fitness data in a json file.
        """
        with open(f"../points/{self.name}.json", mode="w") as dataFile:
            new_j = json.dumps(self.fitness_data)
            dataFile.write(new_j)
            dataFile.close()
    
    
    def get_data(self):
        """
        Retrieves segment measurements.
        Returns:
            seg_lengths0 - list of finger 0 segment lengths (right)
            seg_lengths1 - list of finger 1 segment lengths (left)
        """
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
        """
        Builds right finger outline of reachable space.
        Parameters:
            seg_lengths0 - list of segment lengths
        Returns:
            right_coords as a numpy array - list of outline points
        """
        right_coords = []
        for i in range(-135, -135+180):
            right_coords.append(self.build_outline(i, 0, 0, seg_lengths0[0], seg_lengths0[1], seg_lengths0[2], "right"))
        for i in range(0, 90):
            right_coords.append(self.build_outline(-135+180, i, 0, seg_lengths0[0], seg_lengths0[1], seg_lengths0[2], "right"))
        for i in range(0, 90):
            right_coords.append(self.build_outline(-135+180, 90, i, seg_lengths0[0], seg_lengths0[1], seg_lengths0[2], "right"))
        for i in reversed(range(-135, -135+180)):
            right_coords.append(self.build_outline(i, 90, 90, seg_lengths0[0], seg_lengths0[1], seg_lengths0[2], "right"))
        for i in reversed(range(0, 90)):
            right_coords.append(self.build_outline(-135, i, 90, seg_lengths0[0], seg_lengths0[1], seg_lengths0[2], "right"))
        for i in reversed(range(0, 90)):
            right_coords.append(self.build_outline(-135, 0, i, seg_lengths0[0], seg_lengths0[1], seg_lengths0[2], "right"))
        
        return np.asarray(right_coords)
    
        
    def build_coord_space_left(self, seg_lengths1):
        """
        Builds left finger outline of reachable space.
        Parameters:
            seg_lengths1 - list of segment lengths
        Returns:
            left_coords as a numpy array - list of outline points
        """
        left_coords = []
        for i in reversed(range(135-180, 135)):
            left_coords.append(self.build_outline(i, 0, 0, seg_lengths1[0], seg_lengths1[1], seg_lengths1[2], "left"))
        for i in reversed(range(-90, 0)):
            left_coords.append(self.build_outline(135-180, i, 0, seg_lengths1[0], seg_lengths1[1], seg_lengths1[2], "left"))
        for i in reversed(range(-90, 0)):
            left_coords.append(self.build_outline(135-180, -90, i, seg_lengths1[0], seg_lengths1[1], seg_lengths1[2], "left"))
        for i in range(135-180, 135):
            left_coords.append(self.build_outline(i, -90, -90, seg_lengths1[0], seg_lengths1[1], seg_lengths1[2], "left"))
        for i in range(-90, 0):
            left_coords.append(self.build_outline(135, i, -90, seg_lengths1[0], seg_lengths1[1], seg_lengths1[2], "left"))
        for i in range(-90, 0):
            left_coords.append(self.build_outline(135, 0, i, seg_lengths1[0], seg_lengths1[1], seg_lengths1[2], "left"))
        
        return np.asarray(left_coords)    
        
        
    def build_outline(self, theta1, theta2, theta3, l1, l2, l3, finger):
        """
        Adapted from: https://hades.mech.northwestern.edu/index.php/Modern_Robotics
        To find the original formulas, go to the Forward Kinematics section in the textbook.
        Also see: 
        https://mecharithm.com/learning/lesson/task-space-and-workspace-for-robots-102
        https://journals.sagepub.com/doi/10.5772/45686
        Uses Denavit-Hartenberg parameters to calculate reachable space based on joint limits set in build_coord_space methods.
        Parameters:
            (from palm up)
            theta1 - joint 1 angle 
            theta2 - joint 2 angle
            theta3 - joint 3 angle
            l1 - link1 length
            l2 - link2 length
            l3 - link3 length
            finger - right or left
        Returns:
            [x, y] - list of x and y coordinates of calculated point
        """
        # convert to radians
        theta1 = np.pi * theta1 / 180
        theta2 = np.pi * theta2 / 180
        theta3 = np.pi * theta3 / 180

        # rotation offset
        val = 90 * np.pi/180
        
        if finger == "right":
            x = l1 *np.cos(theta1 + val) + l2*np.cos(theta1+theta2 + val) + l3*np.cos(theta1 + theta2 + theta3 + val) + self.width/2
        else:
            x = l1 *np.cos(theta1 + val) + l2*np.cos(theta1+theta2 + val) + l3*np.cos(theta1 + theta2 + theta3 + val) - self.width/2
        y = l1 * np.sin(theta1 + val) + l2*np.sin(theta1 + theta2 + val) + l3*np.sin(theta1 + theta2 + theta3 + val)
        
        return [x, y]
    

    def area_test(self, r, l, coords):
        """
        Runs area test, in which it counts the amount of center points inside the overlapping workspaces.
        Parameters:
            r - right outline
            l - left outline
            coords - center points
        Returns:
            ans - fitness score (number of points inside both outlines)
        """
        inside = []
        ans = 0
        ind = self.check_inside(r, coords)
        ind2 = self.check_inside(l, coords)
        inside.extend(list(coords[i]) for i in range(len(coords)) if i in ind and i in ind2)
        ans = len(inside)
        inside_x, inside_y = np.hsplit(np.asarray(inside), 2)
        self.fitness_data.area_outline_x = inside_x.tolist()
        self.fitness_data.area_outline_y = inside_y.tolist()
        self.fitness_data.update()
        
        return ans
    
       
    def angles_test(self, right_outline, left_outline, cent, r_points, l_points):
        """
        Runs angles test, in which it checks if points distance radius from center point at n different 
        angles 180 degrees apart are inside their respective right and left workspaces and match up with each other.
        Parameters:
            right_outline - shape of right finger reachable space
            left_outline - shape of left finger reachable space
            cent - center coordinates
            r_points - right finger coords at n angles to check [[[x1, y1],...,[xn, yn]]]
            l_points - left finger coords at n angles to check [[[x1, y1],...,[xn, yn]]]
        Returns:
            fitness - fitness score (amount of point pairs reached)
        """
        count0 = [] # list of angle counts for right finger
        inside_0 = []   # list of inside l_points coordinate indices for right finger
        count1 = [] # list of angle counts for left finger
        inside_1 = []   # list of inside l_points coordinate indices for left finger
        angles0 = []    # list of coordinates reached out of n tested right
        angles1 = []    # list of coordinates reached out of n tested left
      
        # enumerate index, point list of n points through coordinates to test
        for i, ele in enumerate(r_points):
            angles = self.check_inside(right_outline, ele)
            angles0.append(angles)
            count = len(angles)
            if count != 0:
                inside_0.append(i)
                count0.append(count)
                
        for i, ele in enumerate(l_points):
            angles = self.check_inside(left_outline, ele)
            count = len(angles)
            angles1.append(angles)
            if count != 0:
                inside_1.append(i)
                count1.append(count)
        
        ct = 0  # total count of number of points reached
        idx = []    # [index of reached angle point [0->n], count of angle]

        # check if it is in the overlapping area
        for i in range(len(inside_0)):
            count = 0   # angle count
            if inside_0[i] in inside_1:
                for a in angles0[inside_0[i]]:
                    if a in angles1[inside_0[i]]:
                         count = count + 1
                if count != 0:
                    idx.append([inside_0[i], count])
                    ct = ct + count

        c = []  # list of reached center points
        for i in idx:
            j = i[0]
            c.append(cent[j])

        # if any inside points are found, save the data
        if len(c)!=0:
            fitness = ct
            centersx = np.split(np.asarray(c), 2, 1)[0]
            centersy = np.split(np.asarray(c), 2, 1)[1]
            cnt = np.split(np.asarray(idx), 2, 1)[1]
            self.fitness_data.angle_data.centersx = centersx.tolist()
            self.fitness_data.angle_data.centersy = centersy.tolist()
            self.fitness_data.angle_data.count = cnt.tolist()
            self.fitness_data.update()

        # otherwise data is blank
        else:
            self.fitness_data.angle_data.centersx = []
            self.fitness_data.angle_data.centersy = []
            self.fitness_data.angle_data.count = []
            self.fitness_data.update()
            fitness = 0

        return fitness
    
    
    def check_inside(self, outline, points):
        """
        Checks if angles test points are inside the outline.
        Parameters:
            outline - outline of workspace
            points - list of n points to check
        Returns:
            inside_indices - list of inside point indices
        """
        inside_indices = []
        polygon = Polygon(outline)
        for idx, i in enumerate(points):
            if i[0] < self.width/2 and i[0] > -abs(self.width)/2 and i[1] < 0:
                continue
            else:
                point = Point(i)
                if polygon.contains(point):
                    inside_indices.append(idx)
   
        return inside_indices
        

    def straight_test(self, right_outline, left_outline, r_points, l_points): 
        """
        Conducts straight test, in which it tests if a pair of right and left points around a center point
        at 180 degrees apart are inside their respective outlines and match up with each other.
        Parameters:
            right_outline - right outline coordinates
            left_outline - left outline coordinates
            r_points - right coordinates to test
            l_points - left coordinates to test
        Returns:
            fitness - fitness score from straight test (amount of point pairs which fall within parameters)
        """
        inside_indicies0 = self.check_inside(right_outline, r_points)
        inside_indicies1 = self.check_inside(left_outline, l_points)
        idx = [i for i in inside_indicies0 if i in inside_indicies1]

        if len(idx) != 0:
            fitness = len(idx)
        else:
            fitness = 0

        self.fitness_data.straight_data = idx
        self.fitness_data.update()
              
        return fitness
    
        
    def angles_coordinates(self, right_coords, left_coords):
        """
        Builds an array of coordinates to test for angles test.
        Parameters:
            right_coords - right workspace outline
            left_coords - left workspace outline
        Returns:
            center_pt - center coordinates [[x, y],..]
            right_angles - right coordinates at n angles to check [[[x1, y1],...,[xn, yn]]]
            left_angles - left coordinates at n angles to check [[[x1, y1],...,[xn, yn]]]
        """
        val = self.precision    # precision at which to test (mm) distance between each coordinate 
        rad = params.radius  # radius of imaginary cube to reach
        # separated lists of outline coords
        x_out0, y_out0 = np.split(right_coords, 2, axis=1)  
        x_out1, y_out1 = np.split(left_coords, 2, axis=1)
        top_x = max(max(left_coords, key=lambda point:point[0])[0], max(right_coords, key=lambda point:point[0])[0]) + params.trim_val
        bottom_x = min(min(left_coords, key=lambda point:point[0])[0], min(right_coords, key=lambda point:point[0])[0]) - params.trim_val
        top_y = max(max(left_coords, key=lambda point:point[1])[1], max(right_coords, key=lambda point:point[1])[1]) + params.trim_val
        bottom_y = min(min(left_coords, key=lambda point:point[1])[1], min(right_coords, key=lambda point:point[1])[1]) - params.trim_val
        row_length = top_x - bottom_x
        column_length = top_y - bottom_y
        row_points = int(row_length/val)
        column_points = int(column_length/val)
        n = params.angles_count   # angles around the center point to check
        
        center_pt = [[x, y] for x in np.linspace(bottom_x, top_x, num=row_points) for y in np.linspace(bottom_y, top_y, num=column_points)]
        
        # check if points are valid
        center_pt = [pt for pt in center_pt if not ( pt[0] < self.width/2 and pt[0] > -abs(self.width/2) and pt[1] <0) or (pt[0] < min(x_out0) or pt[0] > max(x_out0)) and (pt[0] < min(x_out1) or pt[0] > max(x_out1))
                           or (pt[1] < min(y_out0) or pt[1] > max(y_out0)) and (pt[1] < min(y_out1) or pt[1] > max(y_out1))]
                
        # generate coords around center_pt for right finger
        angles = np.linspace(0, 2*np.pi, n, endpoint=False) # angles list
        x0 = [(c[0] + (np.cos(a)*rad)) for c in center_pt for a in angles] 
        y0 = [(c[1] + (np.sin(a)*rad)) for c in center_pt for a in angles]
        coords0 = list(zip(x0, y0))

        # generate coords for left finger (shifted by 180 degrees)
        angles = [a+np.pi for a in angles]
        x1 = [(c[0] + (np.cos(a)*rad)) for c in center_pt for a in angles]
        y1 = [(c[1] + (np.sin(a)*rad))for c in center_pt for a in angles]
        coords1 = list(zip(x1, y1))
        
        right_angles = np.reshape(np.asarray(coords0), (-1, n, 2))
        left_angles = np.reshape(np.asarray(coords1), (-1, n, 2))

        return center_pt, right_angles, left_angles

      
    def straight_coordinates(self, val, right_coords, left_coords):
        """
        Builds an array of coordinates to test for straight test.
        Parameters:
            right_coords - right workspace outline
            left_coords - left workspace outline
        Returns:
            r - right coordinates [[x,y],...]
            l - left coordinates [[x,y],...]
        """
        val = self.precision
        x_out0, y_out0 = np.split(np.asarray(right_coords), 2, axis=1)
        x_out1, y_out1 = np.split(np.asarray(left_coords), 2, axis=1)
        top_x = max(max(left_coords, key=lambda point:point[0])[0], max(right_coords, key=lambda point:point[0])[0]) + params.trim_val
        bottom_x = min(min(left_coords, key=lambda point:point[0])[0], min(right_coords, key=lambda point:point[0])[0]) - params.trim_val
        top_y = max(max(left_coords, key=lambda point:point[1])[1], max(right_coords, key=lambda point:point[1])[1]) + params.trim_val
        bottom_y = min(min(left_coords, key=lambda point:point[1])[1], min(right_coords, key=lambda point:point[1])[1]) - params.trim_val
        row_length = top_x - bottom_x
        column_length = top_y - bottom_y
        row_points = int(row_length/val)
        column_points = int(column_length/val)
        rad = params.radius
      
        center_pt = [[x, y] for x in np.linspace(bottom_x, top_x, num=row_points) for y in np.linspace(bottom_y, top_y, num=column_points)]
        center_pt = [pt for pt in center_pt if not ( pt[0] < self.width/2 and pt[0] > -abs(self.width/2) and pt[1] <0) or (pt[0] < min(x_out0) or pt[0] > max(x_out0)) and (pt[0] < min(x_out1) or pt[0] > max(x_out1))
                           or (pt[1] < min(y_out0) or pt[1] > max(y_out0)) and (pt[1] < min(y_out1) or pt[1] > max(y_out1))]
        

        x0 = [(c[0] + rad) for c in center_pt]
        y0 = [c[1] for c in center_pt]
        coords0 = list(zip(x0, y0))
        
        x1 = [(c[0] - rad) for c in center_pt]
        y1 = [c[1] for c in center_pt]
        coords1 = list(zip(x1, y1))
        
        r = np.asarray(coords0)
        l = np.asarray(coords1)
        
        return r, l
       

    def area_coordinates(self, val, right_coords, left_coords):
        """
        Builds an array of coordinates to test for area test.
        Parameters:
            right_coords - right workspace outline
            left_coords - left workspace outline
        Returns:
            center_pt - coordinates to test
        """
        val = self.precision
        x_out0, y_out0 = np.split(np.asarray(right_coords), 2, axis=1)
        x_out1, y_out1 = np.split(np.asarray(left_coords), 2, axis=1)
        top_x = max(max(left_coords, key=lambda point:point[0])[0], max(right_coords, key=lambda point:point[0])[0]) + params.trim_val
        bottom_x = min(min(left_coords, key=lambda point:point[0])[0], min(right_coords, key=lambda point:point[0])[0]) - params.trim_val
        top_y = max(max(left_coords, key=lambda point:point[1])[1], max(right_coords, key=lambda point:point[1])[1]) + params.trim_val
        bottom_y = min(min(left_coords, key=lambda point:point[1])[1], min(right_coords, key=lambda point:point[1])[1]) - params.trim_val
        row_length = top_x - bottom_x
        column_length = top_y - bottom_y
        row_points = int(row_length/val)
        column_points = int(column_length/val)
        rad = params.radius
        center_pt = [[x, y] for x in np.linspace(bottom_x, top_x, num=row_points) for y in np.linspace(bottom_y, top_y, num=column_points)]
        
        center_pt = [pt for pt in center_pt if not ( pt[0] < self.width/2 and pt[0] > -abs(self.width/2) and pt[1] <0) or (pt[0] < min(x_out0) or pt[0] > max(x_out0)) and (pt[0] < min(x_out1) or pt[0] > max(x_out1))
                           or (pt[1] < min(y_out0) or pt[1] > max(y_out0)) and (pt[1] < min(y_out1) or pt[1] > max(y_out1))]
        
        return center_pt
