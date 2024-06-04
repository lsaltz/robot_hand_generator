import numpy as np    
# By Marshall Saltz
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
import test as nt
import build_hand as bh
import angles_plot
import json

def get_data(filename, gen):
    data = []
    for i in range(gen):
        if i % 2 == 0 and i != 0: ################################change to 50!!!!!!!!!!!!!!!!
            with open(f"../output/{filename}{i}.json", mode="r") as p:
                data.extend(json.load(p))
    return data    
   

data = get_data("sortedScoring", 5)
print(data)