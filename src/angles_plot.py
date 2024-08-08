import numpy as np
import matplotlib.pyplot as plt
from matplotlib import path
from matplotlib.lines import Line2D
import main
import build_hand as bh
import basic_load
from addict import Dict
import time
from scipy.spatial import ConvexHull
import math
from scipy.optimize import curve_fit
from scipy import integrate
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import json


class Plot:

    def __init__(self, name):
        self.name = name
        self.cent = []
        self.center_pts = []
        
    def main(self):
        
        data = self.get_data()
        self.coordinates(0.02, data) #0.02
        self.plot_area(data)  
        #self.plot_straight(data)
        #self.plot_angles(data)
         
    def get_data(self):
        with open(f"../points/{self.name}.json", mode="r") as p:
            data = Dict(json.load(p))
            p.close()
        
        return data
        
    def plot_area(self, data):
        fig, ax = plt.subplots( nrows=1, ncols=1 )
        insidex = data.area_outline_x
        insidey = data.area_outline_y
        width = data.width
        for i in self.cent:
            ax.scatter(i[0], i[1], color="red")
        
        for i in data.coord_space_right:
            ax.scatter(i[0], i[1], color="blue")
        for i in data.coord_space_left:
            ax.scatter(i[0], i[1], color="blue")
        ax.scatter(insidex, insidey, color="purple")
        ax.set_aspect('equal')
        ax.set_title("Outline of Area Measured")
        ax.set_xlabel("X Position (meters)")
        ax.set_ylabel("Y Position (meters)")
        fig.savefig(f'../output/{self.name}_a.png')
        plt.close(fig)
        
        
        
    def plot_straight(self, data):
        
        fig, ax = plt.subplots( nrows=1, ncols=1 )
        width = data.width
        for i in self.cent:
            
                
            ax.scatter(i[0], i[1], color="red")
        for i in data.coord_space_right:
            ax.scatter(i[0], i[1], color="blue")
        for i in data.coord_space_left:
            ax.scatter(i[0], i[1], color="blue")
        idx =  data.straight_data
        
        for p in idx:
             
             ax.scatter(self.center_pts[p][0], self.center_pts[p][1], color='green') 
                
        ax.set_aspect('equal')
        ax.set_title("Center Points of Reached Horizontal Coordinates")
        ax.set_xlabel("X Position (meters)")
        ax.set_ylabel("Y Position (meters)")
        fig.savefig(f'../output/{self.name}_s.png')
        plt.close(fig)
        
        
        
    def plot_angles(self, data):
        
        fig, ax = plt.subplots( nrows=1, ncols=1 )
        width = data.width
        for i in self.cent:
            ax.scatter(i[0], i[1], color="red")
                
        for i in data.coord_space_right:
            ax.scatter(i[0], i[1], color="blue")
        for i in data.coord_space_left:
            ax.scatter(i[0], i[1], color="blue")
        idx =  data.straight_data
        x = data.angle_data.centersx
        y = data.angle_data.centersy
        count = data.angle_data.count
        a = ax.scatter(x, y, c=count, ec='k')
        
        
  
        plt.colorbar(a, label="Amount of Angles Reached") 
        ax.set_title("Center Points of Reached Angles")
        ax.set_xlabel("X Position (meters)")
        ax.set_ylabel("Y Position (meters)")
                
        ax.set_aspect('equal')

        fig.savefig(f'../output/{self.name}_t.png')
        plt.close(fig)
        
        
        
    def coordinates(self, val, data):
        
        finger_z = 0.288
        
        
        x_out0, y_out0 = np.split(np.asarray(data.coord_space_right), 2, axis=1)
        x_out1, y_out1 = np.split(np.asarray(data.coord_space_left), 2, axis=1)
        total_height = 0.288
        coords1 = []
        coords2 = []
        bottom_x = -abs(total_height + 0.1)
        bottom_y = -abs(total_height + 0.1)
        row_length = finger_z - bottom_x
        column_length = finger_z - bottom_y
        row_points = int(row_length/val)
        column_points = int(column_length/val)
        
        rad = 0.039/2
      
        self.center_pts = [[x, y] for x in np.linspace(bottom_x, finger_z, num=row_points) for y in np.linspace(bottom_y, finger_z, num=column_points)]
        self.cent = [[x, y] for x in np.linspace(bottom_x, finger_z, num=row_points) for y in np.linspace(bottom_y, finger_z, num=column_points)]
        for i in self.center_pts:
            if i[0] < data.width/2 and i[0] > -abs(data.width)/2 and i[1] < 0:
                
                self.center_pts.remove(i)
            elif i[0] <min(x_out0) or i[0] > max(x_out0) or i[0] < min(x_out1) or i[0] > max(x_out1):
                self.center_pts.remove(i)
            elif i[1] <min(y_out0) or i[1] > max(y_out0) or i[1] < min(y_out1) or i[1] > max(y_out1):
                self.center_pts.remove(i)
                
    
            
        
      
if __name__ == "__main__":
    p = Plot("child_0_3_3eo")
    p.main()
    print("done")
