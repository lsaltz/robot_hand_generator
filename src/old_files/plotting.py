import matplotlib.pyplot as plt
import numpy as np
import json
from addict import Dict

class Plotting:

    def __init__(self, all_coordinates, jfile, right_coords, left_coords, c_coords):
        self.ac = all_coordinates
        self.jfile = jfile
        self.rco = right_coords
        self.lco = left_coords
        self.name = jfile.split(".")[0]
        self.c_coords = c_coords
        
    def plot_center(self):
        coordsR, coordsL, nr_R, nr_L = self.open_file()
        right_reached = self.get_count(1, coordsR)
        left_reached = self.get_count(2, coordsL)
        all_pts = []
        for i in range(len(right_reached)):
            all_pts.append(right_reached[i] + left_reached[i])
        fig, ax = plt.subplots(3)
        x = []
        y = []
        for i in range(len(self.c_coords)):
            x.append(self.c_coords[i][0])
            y.append(self.c_coords[i][1])
        a1=ax[0].scatter(x, y, c=right_reached, cmap=plt.cm.jet)
        a2=ax[1].scatter(x, y, c=left_reached, cmap=plt.cm.jet)
        a3=ax[2].scatter(x, y, c=all_pts, cmap=plt.cm.jet)
        fig.colorbar(a1, orientation='horizontal')
        fig.colorbar(a2, orientation='horizontal')
        fig.colorbar(a3, orientation='horizontal')
        ax[0].set_title('Right')
        ax[0].set_aspect('equal', 'box')
        ax[1].set_title('Left')
        ax[1].set_aspect('equal', 'box')
        ax[2].set_title('Total')
        ax[2].set_aspect('equal', 'box')
        plt.show()
        
    def get_count(self, ind, coords):    
        counting_arr = []
        co = self.format_lists(coords)
        for i in range(len(self.ac)):
            counting_arr.append(0)
            
            for c in co:
                
                if list(c) in self.ac[i][ind]:
                   counting_arr[i] += 1
                   
        
        return counting_arr
                 
    def format_lists(self, ls):
        x = [i[0] for i in ls]
        y = [i[1] for i in ls]
        returned_ls = list(zip(x, y, np.zeros(len(ls))))
        return returned_ls
    
    def plot_seperate_thetas_bar_chart(self):
        coordsR, coordsL, nr_R, nr_L = self.open_file()
        coordR = self.format_lists(coordsR)
        coordL = self.format_lists(coordsL)
        nrR = self.format_lists(nr_R)
        nrL = self.format_lists(nr_L)
        rc = self.rco
        lc = self.lco
        
        height_right_reached = []
        height_left_reached = []
        height_right_not = []
        height_left_not = []
        total_reached = []
        total_not = []
        
        for i in range(8):
            hrr = self.get_height(i, coordR, rc)
            hlr = self.get_height(i, coordL, lc)
            hrn = self.get_height(i, nrR, rc)
            hln = self.get_height(i, nrL, lc)
            height_right_reached.append(hrr)
            
            height_left_reached.append(hlr)
            
            height_right_not.append(hrn)
            height_left_not.append(hln)
            total_reached.append(hrr+hlr)
            total_not.append(hln+hrn)
           
        right_heights = {
            'Reached': np.asarray(height_right_reached),
            'Not Reached': np.asarray(height_right_not)
        }  
        left_heights = {
            'Reached': np.asarray(height_left_reached),
            'Not Reached': np.asarray(height_left_not)
        }
        total_heights = {
            'Reached': np.asarray(total_reached),
            'Not Reached': np.asarray(total_not)
        }
        fig, ax = plt.subplots(3, layout='constrained')
        ax = self.plot_bar(0, ax, right_heights)
        ax = self.plot_bar(1, ax, left_heights)
        ax = self.plot_bar(2, ax, total_heights)
        ax[0].set_title('Right')
        
        ax[1].set_title('Left')
        ax[2].set_title('Total')
        #ax.set_title(f"{self.name}")
        #ax.legend(loc="upper right")
        plt.show()
        
    def plot_bar(self, index, ax, dictionary_to_plot):
        i = np.arange(8)
        multiplier = 0
        width = 0.5
        for labels, measurements in dictionary_to_plot.items():
            offset=width*multiplier
            p = ax[index].bar(i, measurements, width, label=labels)
            ax[index].bar_label(p, padding=3)  
            
            multiplier+=1
        ax[index].set_xlim(-1,8)
        #ax[index].axis('equal')
        
        ax[index].legend(loc='upper left', ncols=2)
        return ax       
           
        
    def get_height(self, i, coords, full_coords):
        
        theta = full_coords[i::8]
        height = self.get_t(coords, theta)
        
        return height
                    
    def get_t(self, coords, theta):
        count = 0
        
        for r in coords:
            
            if r in theta:
                count += 1
                
        return count        
    """    
    def get_thetas(self, coordinates):
        ind = []
        center_pts = []
        for r in coordinates:
            for a in self.ac:
                if list(r) in a[1]:
                    ind.append(self.ac.index(list(r)))
                    
        for i in ind:
            center_pts.append(self.ac[i][0])            
        
    """    
    def open_file(self): 
        coordsR=[]
        coordsL=[]
        nr_R=[]
        nr_L=[]
        with open(f"../points/{self.jfile}", mode="r") as f:
            fi = json.load(f)
            dictionary = Dict(fi)
            coordsR.extend(list(dictionary.finger_0.reached))
            coordsL.extend(list(dictionary.finger_1.reached))
            nr_R.extend(list(dictionary.finger_0.not_reached))
            nr_L.extend(list(dictionary.finger_1.not_reached))
            
        return coordsR, coordsL, nr_R, nr_L



def coordinate_array(val):
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
    rad = 0.019
    
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
     
    return coords1, coords2, center_pt, c
    
if __name__ == "__main__":
    jfile = "child_0_257_9w.json"
    coords1, coords2, ccoords, all_coords = coordinate_array(0.03)
    p = Plotting(all_coords, jfile, coords1, coords2, ccoords)
    #print(ccoords)
    #p.plot_seperate_thetas_bar_chart()
    p.plot_center()
