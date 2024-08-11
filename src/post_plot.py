import random
import numpy as np
import os
import json
import mutations
from addict import Dict
import matplotlib.pyplot as plt
import time
import main
from pathlib import Path
import basic_load
import combination
import first_generation
import copy
import build_hand as bh
import angles_plot

def plot_fitness(generational_fitness, letter):
    with open(generational_fitness, mode="r") as f:
        data = json.load(f)
        

    f.close()
    
    epochs = []
    plt.figure()
    plt.xlim(0, 5001)
    print(data)
    generational_fitness = np.split(np.asarray(data), len(data[0]), axis=1)[1]
    print(generational_fitness)
    plt.ylim(0, (max(generational_fitness) + max(generational_fitness)/2))
    for i in range(5000+1):
        epochs.append(i)
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    #plt.ylabel("Area")
    plt.title("Max Fitness of Each Generation")
    plt.plot(epochs, generational_fitness, color='blue', linestyle='solid')
    
    #plt.savefig(f"../output/fitness_{letter}")
    plt.savefig(f"../output/fitness_{letter}")
plot_fitness("../output/generational_a.json", "a")

#plot_fitness("../output/generational_s.json", "s")
#plot_fitness("../output/generational_t.json", "t")