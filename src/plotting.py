# By Marshall Saltz
import numpy as np
import matplotlib.pyplot as plt
from addict import Dict
import json
import params
import test as nt


class Plot:
    """
    Takes care of plotting data.
    """

    def __init__(self, name, precision):
        """
        Initializes class.
        Parameters:
            name - name of gripper to plot data of.
            precision - precision testing was run at for coordinate generation
        """
        self.name = name
        self.precision = precision
        self.center_pts = []    # workspace points
        
    def main(self):
        """
        Main function for plotting, generates plot based on flag set in params.
        """
        data = self.get_data()
        self.coordinates(data)
        if params.flag == "angle":
            self.plot_angles(data)
        elif params.flag == "area":
            self.plot_area(data)  
        else:
            self.plot_straight(data)

         
    def get_data(self):
        """
        Gets points data of gripper.
        Returns:
            data - Dict() of received data
        """
        with open(f"../points/{self.name}.json", mode="r") as p:
            data = Dict(json.load(p))
            p.close()

        return data
    
        
    def plot_area(self, data):
        """
        Plots area test.
        Parameters:
            data - data to plot
        """
        fig, ax = plt.subplots( nrows=1, ncols=1 )
        insidex = data.area_outline_x
        insidey = data.area_outline_y
        width = data.width
        for pt in self.center_pts:
            ax.scatter(pt[0], pt[1], color="red")
        # outline of each finger's reachable space
        for pt in data.coord_space_right:
            ax.scatter(pt[0], pt[1], color="blue")
        for pt in data.coord_space_left:
            ax.scatter(pt[0], pt[1], color="blue")
        # plot reached center points
        ax.scatter(insidex, insidey, color="purple")
        ax.set_aspect('equal')
        ax.set_title("Area Test")
        ax.set_xlabel("X Position (meters)")
        ax.set_ylabel("Y Position (meters)")
        fig.savefig(f'../output/{self.name}_{self.precision}_a.png')
        plt.close(fig)
        
        
        
    def plot_straight(self, data):
        """
        Plots straight line test.
        Parameters:
            data - data to plot
        """
        fig, ax = plt.subplots( nrows=1, ncols=1 )
        width = data.width
        # scatter all points
        for pt in self.center_pts:
            ax.scatter(pt[0], pt[1], color="red")
        # plot outline
        for pt in data.coord_space_right:
            ax.scatter(pt[0], pt[1], color="blue")
        for pt in data.coord_space_left:
            ax.scatter(pt[0], pt[1], color="blue")
        idx =  data.straight_data
        # scatter reached straight center points
        for p in idx:
             ax.scatter(self.center_pts[p][0], self.center_pts[p][1], color='green')        
        ax.set_aspect('equal')
        ax.set_title("Center Points of Reached Horizontal Coordinates")
        ax.set_xlabel("X Position (meters)")
        ax.set_ylabel("Y Position (meters)")
        fig.savefig(f'../output/{self.name}_{self.precision}_s.png')
        plt.close(fig)
        
        
    def plot_angles(self, data):
        """
        Plots angles test.
        Parameters:
            data - data to plot
        """
        fig, ax = plt.subplots( nrows=1, ncols=1 )
        width = data.width
        # plot workspace
        for pt in self.center_pts:
            ax.scatter(pt[0], pt[1], color="red")
        # plot outline
        for pt in data.coord_space_right:
            ax.scatter(pt[0], pt[1], color="blue")
        for pt in data.coord_space_left:
            ax.scatter(pt[0], pt[1], color="blue")
        # plot reached angles
        x = data.angle_data.centersx
        y = data.angle_data.centersy
        count = data.angle_data.count
        a = ax.scatter(x, y, c=count, cmap='viridis', edgecolors='none')
        plt.colorbar(a, label="Amount of Angles Reached") 
        ax.set_title("Center Points of Reached Angles")
        ax.set_xlabel("X Position (meters)")
        ax.set_ylabel("Y Position (meters)")
        ax.set_aspect('equal')
        fig.savefig(f'../output/{self.name}_{self.precision}_t.png')
        plt.close(fig)
        

    def coordinates(self, data):
        """
        Generates background coordinates for plotting.
        Parameters:
            data - gripper data
        """
        val = self.precision
        x_out0, y_out0 = np.split(np.asarray(data.coord_space_right), 2, axis=1)
        x_out1, y_out1 = np.split(np.asarray(data.coord_space_left), 2, axis=1)
        top_x = max(max(data.coord_space_left, key=lambda point:point[0])[0], max(data.coord_space_right, key=lambda point:point[0])[0]) + params.trim_val
        bottom_x = min(min(data.coord_space_left, key=lambda point:point[0])[0], min(data.coord_space_right, key=lambda point:point[0])[0]) - params.trim_val
        top_y = max(max(data.coord_space_left, key=lambda point:point[1])[1], max(data.coord_space_right, key=lambda point:point[1])[1]) + params.trim_val
        bottom_y = min(min(data.coord_space_left, key=lambda point:point[1])[1], min(data.coord_space_right, key=lambda point:point[1])[1]) - params.trim_val
        row_length = top_x - bottom_x
        column_length = top_y - bottom_y
        row_points = int(row_length/val)
        column_points = int(column_length/val)
        width = data.width
        
        self.center_pts = [[x, y] for x in np.linspace(bottom_x, top_x, num=row_points) for y in np.linspace(bottom_y, top_y, num=column_points)]
        for pt in self.center_pts:
            if pt[0] < width/2 and pt[0] > -abs(width)/2 and pt[1] <0:
                self.center_pts.remove(pt)
            elif (pt[0] < min(x_out0) or pt[0] > max(x_out0)) and (pt[0] < min(x_out1) or pt[0] > max(x_out1)):
                self.center_pts.remove(pt)
            elif (pt[1] < min(y_out0) or pt[1] > max(y_out0)) and (pt[1] < min(y_out1) or pt[1] > max(y_out1)):
                self.center_pts.remove(pt)
    

def plot_fitness(generational_fitness, generations):
        """
        Plots maximum overall fitnesses with each generation.
        Parameters:
            generational_fitness - list of maximum fitnesses
            generations - total amount of generations
        """
        epochs = []
        plt.figure()
        generational_fitness = list(generational_fitness)
        plt.xlim(0, generations)
        plt.ylim(0, max(generational_fitness) + max(generational_fitness)/2)
        for i in range(generations):
            epochs.append(i)
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.title("Max fitness of each generation")
        plt.plot(epochs, generational_fitness, color='blue', linestyle='solid')
        plt.savefig(f"../output/fitness_trend_{params.flag}")
        with open(f"../output/generational_{params.flag}.json", mode="w") as resultsFile:
            new_j = json.dumps(list(zip(epochs, generational_fitness)))
            resultsFile.write(new_j)
        resultsFile.close()

def test(dicList, precision):
    """
    Runs test on grippers.
    Parameters:
        dicList - list of dictionaries to test
        precision - space in between points (mm)
    Returns:
        fitnesses - list of test results
    """
    fitnesses = []
    for l in dicList:    
        gripper_name = l['name']    
        w = nt.WorkSpace_Test(gripper_name, l, precision)     
        fit = w.main()
        fitnesses.append([fit, f"{gripper_name}.json"])
    
    return fitnesses


#######################Currently generating new plots for angle_5000_2
if __name__ == "__main__":
    fitnesses = []
    precision = params.precision2
    ls = [
        Dict({'finger_1': {'num_segs': 4}, 'ratio': {'segs': {'finger_1': [42, 13, 45], 'finger_0': [53, 1, 46]}, 'finger_0': 7, 'finger_1': 7}, 'finger_0': {'num_segs': 4}, 'length': {'palm': 0.05237, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_1_1522_1w_s'}),
        Dict({'finger_0': {'num_segs': 4}, 'ratio': {'segs': {'finger_0': [55, 2, 43], 'finger_1': [45, 13, 42]}, 'finger_0': 7, 'finger_1': 7}, 'finger_1': {'num_segs': 4}, 'length': {'palm': 0.05135, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_0_1683_0eo_eo'}),
        Dict({'name': 'hand_mut_gen_2170_8', 'finger_0': {'num_segs': 4}, 'finger_1': {'num_segs': 4}, 'ratio': {'segs': {'finger_0': [47, 8, 45], 'finger_1': [47, 13, 40]}, 'finger_0': 7, 'finger_1': 7}, 'length': {'palm': 0.05069, 'finger_0': 0.144, 'finger_1': 0.144}}),
        Dict({'finger_1': {'num_segs': 4}, 'ratio': {'segs': {'finger_1': [45, 7, 48], 'finger_0': [45, 15, 40]}, 'finger_0': 7, 'finger_1': 7}, 'finger_0': {'num_segs': 4}, 'length': {'palm': 0.05069, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_1_2247_4w_s'}),
        Dict({'finger_0': {'num_segs': 4}, 'ratio': {'segs': {'finger_0': [46, 17, 37], 'finger_1': [47, 13, 40]}, 'finger_0': 7, 'finger_1': 7}, 'finger_1': {'num_segs': 4}, 'length': {'palm': 0.05189, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_0_2520_3w_s'}),
        Dict({'finger_0': {'num_segs': 4}, 'ratio': {'segs': {'finger_0': [51, 11, 38], 'finger_1': [45, 13, 42]}, 'finger_0': 7, 'finger_1': 7}, 'finger_1': {'num_segs': 4}, 'length': {'palm': 0.05135, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_0_2577_2eo_eo'}),
        Dict({'finger_0': {'num_segs': 4}, 'ratio': {'segs': {'finger_0': [53, 4, 43], 'finger_1': [42, 13, 45]}, 'finger_0': 7, 'finger_1': 7}, 'finger_1': {'num_segs': 4}, 'length': {'palm': 0.05177, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_0_2828_3eo_eo'}),
        Dict({'finger_0': {'num_segs': 4}, 'ratio': {'segs': {'finger_0': [43, 14, 43], 'finger_1': [46, 10, 44]}, 'finger_0': 7, 'finger_1': 7}, 'finger_1': {'num_segs': 4}, 'length': {'palm': 0.05177, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_0_2865_1eo_eo'}),
        Dict({'finger_1': {'num_segs': 4}, 'ratio': {'segs': {'finger_1': [47, 9, 44], 'finger_0': [51, 8, 41]}, 'finger_0': 7, 'finger_1': 7}, 'finger_0': {'num_segs': 4}, 'length': {'palm': 0.05177, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_1_3028_0w_s'}),
        Dict({'finger_0': {'num_segs': 4}, 'ratio': {'segs': {'finger_0': [50, 4, 46], 'finger_1': [47, 13, 40]}, 'finger_0': 7, 'finger_1': 7}, 'finger_1': {'num_segs': 4}, 'length': {'palm': 0.05019, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_0_3264_2w_s'}),
        Dict({'finger_0': {'num_segs': 4}, 'ratio': {'segs': {'finger_0': [52, 1, 47], 'finger_1': [44, 12, 44]}, 'finger_0': 7, 'finger_1': 7}, 'finger_1': {'num_segs': 4}, 'length': {'palm': 0.05176, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_0_3286_1eo_eo'}),
        Dict({'finger_1': {'num_segs': 4}, 'ratio': {'segs': {'finger_1': [44, 16, 40], 'finger_0': [50, 4, 46]}, 'finger_0': 7, 'finger_1': 7}, 'finger_0': {'num_segs': 4}, 'length': {'palm': 0.05227, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_1_3301_1w_s'}),
        Dict({'finger_0': {'num_segs': 4}, 'ratio': {'segs': {'finger_0': [50, 6, 44], 'finger_1': [47, 13, 40]}, 'finger_0': 7, 'finger_1': 7}, 'finger_1': {'num_segs': 4}, 'length': {'palm': 0.05019, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_0_3502_0w_s'}),
        Dict({'finger_0': {'num_segs': 4}, 'ratio': {'segs': {'finger_0': [46, 11, 43], 'finger_1': [47, 13, 40]}, 'finger_0': 7, 'finger_1': 7}, 'finger_1': {'num_segs': 4}, 'length': {'palm': 0.05071, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_0_3594_3w_s'}),
        Dict({'finger_1': {'num_segs': 4}, 'ratio': {'segs': {'finger_1': [49, 3, 48], 'finger_0': [51, 8, 41]}, 'finger_0': 7, 'finger_1': 7}, 'finger_0': {'num_segs': 4}, 'length': {'palm': 0.05019, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_1_3647_3w_s'}),
        Dict({'finger_0': {'num_segs': 4}, 'ratio': {'segs': {'finger_0': [56, 2, 42], 'finger_1': [47, 13, 40]}, 'finger_0': 7, 'finger_1': 7}, 'finger_1': {'num_segs': 4}, 'length': {'palm': 0.05069, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_0_3775_1w_s'}),
        Dict({'finger_0': {'num_segs': 4}, 'ratio': {'segs': {'finger_0': [43, 11, 46], 'finger_1': [47, 13, 40]}, 'finger_0': 7, 'finger_1': 7}, 'finger_1': {'num_segs': 4}, 'length': {'palm': 0.05152, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_0_4400_2w_s'}),
        Dict({'finger_1': {'num_segs': 4}, 'ratio': {'segs': {'finger_1': [43, 9, 48], 'finger_0': [55, 2, 43]}, 'finger_0': 7, 'finger_1': 7}, 'finger_0': {'num_segs': 4}, 'length': {'palm': 0.05019, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_1_4609_3w_s'}),
        Dict({'finger_0': {'num_segs': 4}, 'ratio': {'segs': {'finger_0': [51, 10, 39], 'finger_1': [47, 13, 40]}, 'finger_0': 7, 'finger_1': 7}, 'finger_1': {'num_segs': 4}, 'length': {'palm': 0.0505, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_0_4624_2w_s'}),
        Dict({'finger_0': {'num_segs': 4}, 'ratio': {'segs': {'finger_0': [51, 10, 39], 'finger_1': [47, 13, 40]}, 'finger_0': 7, 'finger_1': 7}, 'finger_1': {'num_segs': 4}, 'length': {'palm': 0.05205, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_0_4841_1w_s'}),
        Dict({'finger_0': {'num_segs': 4}, 'ratio': {'segs': {'finger_0': [46, 9, 45], 'finger_1': [47, 13, 40]}, 'finger_0': 7, 'finger_1': 7}, 'finger_1': {'num_segs': 4}, 'length': {'palm': 0.05019, 'finger_0': 0.144, 'finger_1': 0.144}, 'name': 'child_0_4862_1w_s'})
    ]
    fitnesses = test(ls, 5001, precision)
    for l in ls:
        p = Plot(l["name"], precision)
        p.main()
