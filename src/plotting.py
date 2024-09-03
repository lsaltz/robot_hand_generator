# By Marshall Saltz
from matplotlib.patches import Rectangle
import numpy as np
import matplotlib.pyplot as plt
from addict import Dict
import json
import params
import test as nt
import collections


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
            ax.scatter(pt[0], pt[1], color="gray")
        # plot reached center points
        ax.scatter(insidex, insidey, color="green")
        # outline of each finger's reachable space
        for pt in data.coord_space_right:
            ax.scatter(pt[0], pt[1], color="white", alpha=0.2)
        for pt in data.coord_space_left:
            ax.scatter(pt[0], pt[1], color="white", alpha=0.2)
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
            ax.scatter(pt[0], pt[1], color="gray")
        idx =  data.straight_data
        # scatter reached straight center points
        for p in idx:
             ax.scatter(self.center_pts[p][0], self.center_pts[p][1], color='green')      
        # plot outline
        for pt in data.coord_space_right:
            ax.scatter(pt[0], pt[1], color="white", alpha=0.2)
        for pt in data.coord_space_left:
            ax.scatter(pt[0], pt[1], color="white", alpha=0.2)  
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
        # plot workspace
        for pt in self.center_pts:
            ax.scatter(pt[0], pt[1], color="gray")
        # plot reached angles
        x = data.angle_data.centersx
        y = data.angle_data.centersy
        count = data.angle_data.count
        a = ax.scatter(x, y, c=count, cmap='viridis', edgecolors='none')
        # plot outline
        for pt in data.coord_space_right:
            ax.scatter(pt[0], pt[1], color="white", alpha = 0.2)
        for pt in data.coord_space_left:
            ax.scatter(pt[0], pt[1], color="white", alpha = 0.2)

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
        self.center_pts = [pt for pt in self.center_pts if not ( pt[0] < width/2 and pt[0] > -abs(width)/2 and pt[1] <0) or (pt[0] < min(x_out0) or pt[0] > max(x_out0)) and (pt[0] < min(x_out1) or pt[0] > max(x_out1))
                           or (pt[1] < min(y_out0) or pt[1] > max(y_out0)) and (pt[1] < min(y_out1) or pt[1] > max(y_out1))]



def get_data(filename, gen):
    """
    Gets data from a json. Since it saves every interval, it uses that info to get the file.
    Parameters:
        filename - file from which to retreive data
        gen - generation number
    Returns:
        data - data from file (list form)
    """
    data = []
    for i in range(gen):
        if i % params.interval == 0 and i != 0:
            with open(f"../output/{filename}{i}.json", mode="r") as p:
                data.extend(json.load(p))
    return data    


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
        plt.ylabel("Fitness Score")
        plt.title("Maximum Coarse Fitness Score of Each Generation")
        plt.plot(epochs, generational_fitness, color='blue', linestyle='solid')
        plt.text(50, max(generational_fitness) + max(generational_fitness)/3, f'Overall Maximum Fitness Score: {max(generational_fitness)}', bbox={'facecolor': 'blue', 'alpha': 0.5, 'pad': 10})
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
        precision - space in between points
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


def plot_palm_widths(gen):
    """
    Plots palm widths versus scoring.
    Parameters:
        gen - number of generations
    """
    ls =[]
    sortedScoring = []
    sortedScoring.extend(get_data("sortedScoring", gen))
    with open("../output/totallistfile.json") as f:
        ls.extend(json.load(f))
    newlist = sorted(ls, key=lambda d:d['length']['palm'])
    palm_scores_dict = Dict()
    palm_max_score = []
    palm_avg_score = []
    width_list = []
    count = 0
    
    for pair in reversed(sortedScoring):
        for element in newlist:
            if count >= 20:
                break
            if element['name'] +".json" == pair[1]:
                width = element['length']['palm']
                if width not in palm_scores_dict:
                    palm_scores_dict[width] = []
                    count += 1
                palm_scores_dict[width].append(pair[0])
    od = collections.OrderedDict(sorted(palm_scores_dict.items()))
    for width, score, in od.items():
        palm_max_score.append(max(score))
        palm_avg_score.append(sum(score) / len(score))
        width_list.append(width)
    fig, ax = plt.subplots()
    w = 0.25
    bar_len_1 = np.arange(len(palm_avg_score))
    bar2 = [n + w for n in bar_len_1]
    plt.bar(bar_len_1, palm_avg_score, color ='green', width = w, edgecolor ='none', label ='Average Score') 
    plt.bar(bar2, palm_max_score, color ='blue', width = w, edgecolor ='none', label ='Maximum Score') 
    ax.set_ylabel('Fitness Score')
    ax.set_xlabel('Palm Width (m)')
    ax.set_title(f'Palm Widths in Comparison to Fitness Scores')
    plt.xticks((bar2 + bar_len_1)/2, width_list)
    ax.legend()
    ax.set_ylim(0, max(max(palm_avg_score), max(palm_max_score))+10)
    fig.set_size_inches(18.5, 10.5)
    plt.savefig(f"../output/palm_widths_{params.flag}")

def get_top(sortedScoring):
    """
    Returns top grippers.
    Parameters:
        sortedScoring - list of grippers and their scores sorted by score in ascending order
    Returns:
        top - list of top grippers and their scores
        top_names - just the grippers' names
    """
    top = []
    count = 0
    for d in reversed(range(len(sortedScoring))):
        if sortedScoring[d] not in top:
            top.append(sortedScoring[d])
            count += 1
        if count > params.winner_count:
            break
    top_names = list(map(lambda x:x[1].split('.')[0], top))
    return top, top_names

def plot_seg_percents(gen, finger):
    """
    Plots segment percentages versus scores. finger_1
    is separate from finger_0.
    Parameters:
        gen - generations run
        finger - which finger to plot
    """
    ls =[]
    sortedScoring = []
    sortedScoring.extend(get_data("sortedScoring", gen))
    sortedScoring = sorted(sortedScoring, key = lambda x: float(x[0]))
    top_scores, top_names = get_top(sortedScoring)
    with open("../output/totallistfile.json") as f:
        ls.extend(json.load(f))
    segs_0 = []
    segs_1 = []
    segs_2 = []
    for name in top_names:
        for element in ls:    
            if element['name'] == name:
                percents = element['ratio']['segs'][finger]
                segs_0.append(percents[0])
                segs_1.append(percents[1])
                if len(percents) < 3:
                    segs_2.append(0)
                else:
                    segs_2.append(percents[2])
                break
    fig, ax = plt.subplots()
    w = 0.25
    bar_len_1 = np.arange(len(segs_0))
    bar2 = [n + w for n in bar_len_1]
    bar3 = [n + w for n in bar2]
    plt.bar(bar_len_1, segs_0, color ='green', width = w, edgecolor ='none', label ='Segment 0') 
    plt.bar(bar2, segs_1, color ='blue', width = w, edgecolor ='none', label ='Segment 1') 
    plt.bar(bar3, segs_2, color ='indigo', width = w, edgecolor ='none', label ='Segment 2') 
    ax.set_ylabel('Segment Percentage')
    ax.set_xlabel('Fitness Score')
    ax.set_title(f'{finger} Segment Percentages in Comparison to Fitness Scores')
    plt.xticks(bar2, [x[0] for x in top_scores])
    ax.legend()
    ax.set_ylim(0, 100)
    fig.set_size_inches(18.5, 10.5)
    plt.savefig(f"../output/{finger}_Segments_{params.flag}")
