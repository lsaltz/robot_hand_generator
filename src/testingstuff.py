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





def area_test():
    iinside = [[[0, 1],[2, 3],[4,5]],
                [[0,0],[0,0],[0,0]],
                [[2,3],[4,5],[7,8]]]
    iinside = np.asarray(iinside)
        
    zero_mask = np.all(iinside == 0, axis=(1, 2))
    

    zero_indices = np.where(zero_mask)[0]
    print(zero_indices)
    no_zeros = iinside[~zero_mask]
    

    split_indices = zero_indices - np.arange(len(zero_indices))
    arrs = np.split(no_zeros, split_indices)
        
    print(arrs)
    
area_test()