# By Marshall Saltz
import random
import numpy as np
from addict import Dict
import params

class Mutate:
    """
    Mutates gripper files.
    """

    def __init__(self, data, generation, number):
        """
        Initializes class.
        Parameters:
            data - gripper data
            generation - current generation
            number - mutation index
        """
        self.hand_data = Dict() # for storing new data
        self.upper = 10 # upper bounds of mutation finger ratios
        self.lower = 1  # lower bounds
        self.data = data 
        self.generation = generation
        self.number = number


    def determine_seg_percents(self, finger, num_segs):
        """
        Randomly determines segments as percentages of the finger length.
        Parameters:
            finger - finger_0 or finger_1
            num_segs - segment amount, 3 or 4 (really 2 or 3, but additional link of no length is added for the sim)
        """
        list_of_ratios = []
        prev_rat = params.percent_threshold   # link can't be < 100 - threshold
        num = num_segs - 2  # -2 for extra link and just determine the remaining percent of last link via subtraction
        ct = 0  # count of accumulated link percentages
        for i in range(0, num):
            rat = np.random.randint(1, prev_rat+1)
            list_of_ratios.append(rat)
            ct += rat
            prev_rat = 100-ct
        list_of_ratios.append(100-ct)
           
        self.hand_data.ratio.segs[finger] = list_of_ratios
        self.hand_data.update()


    def build_hand(self):
        """
        Mutates the hand. Randomly determines number of segments, pams width, segment percentages, while keeping
        original R:L ratio intact.
        Returns:
            hand_data - Dict() containing muatated hand data
        """
        file_name = "hand_mut_gen_" + str(self.generation) + "_" + str(self.number)
        self.hand_data.name = file_name
        
        self.hand_data.finger_0.num_segs = random.randint(3, 4)
        self.hand_data.finger_1.num_segs = random.randint(3, 4)
        right = self.data.ratio.finger_0
        left = self.data.ratio.finger_1
        
        palm_width = round(random.uniform(0.05, 0.09), 5)
        
        fingers_total_length = 0.288
        finger_0_length = fingers_total_length/(right+left) * right
        finger_1_length = fingers_total_length - finger_0_length

        self.determine_seg_percents("finger_0", int(self.hand_data.finger_0.num_segs))
        self.determine_seg_percents("finger_1", int(self.hand_data.finger_1.num_segs))
        
        self.hand_data.ratio.finger_0 = right
        self.hand_data.ratio.finger_1 = left
        self.hand_data.length.palm = palm_width
        self.hand_data.length.finger_0 = finger_0_length
        self.hand_data.length.finger_1 = finger_1_length
        self.hand_data.update()
 
        return self.hand_data
            
    
        
    
    
