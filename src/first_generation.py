# By Marshall Saltz
import random
import numpy as np
from addict import Dict

class First_Generation:
    """
    Randomly generates initial generation.
    """

    def __init__(self, generation, n):
        """
        Initializes class.
        Parameters:
            generation - generation number
            n - index
        """
        self.upper = 10 # upper finger ratio limit
        self.lower = 1  # lower finger ratio limit
        self.generation = generation
        self.hand_data = Dict() # new Dict() of hand data
        self.n = n

        
    def determine_seg_percents(self, finger, num_segs):
        """
        Randomly determines segments as percentages of the finger length.
        Parameters:
            finger - finger_0 or finger_1
            num_segs - segment amount, 3 or 4 (really 2 or 3, but additional link of no length is added for the sim)
        """
        list_of_ratios = []
        prev_rat = 95
        nm = num_segs- 2
        ct = 0
        for i in range(0, nm):
            rat = np.random.randint(1, prev_rat+1)
            list_of_ratios.append(rat)
            ct += rat
            prev_rat = 100-ct
            
        list_of_ratios.append(100-ct)
        self.hand_data.ratio.segs[finger] = list_of_ratios
        self.hand_data.update()

        
    def build_hand(self):
        """
        Generates random data for an entirely new gripper.
        Returns:
            hand_data - newly generated hand data
        """
          
        file_name = "hand_init" +  '_gen_' + str(self.generation) + "_" + str(self.n)

        self.hand_data.name = file_name
        self.hand_data.finger_0.num_segs = random.randint(3, 4)
        self.hand_data.finger_1.num_segs = random.randint(3, 4)
        
        right = np.random.randint(self.lower, self.upper)
        left = np.random.randint(self.lower, self.upper)
        
        palm_width = round(random.uniform(0.05, 0.09), 5)
        fingers_total_length = 0.288
        finger_0_length = fingers_total_length/(right+left) * right
        finger_1_length = fingers_total_length - finger_0_length

        self.determine_seg_percents("finger_0", self.hand_data.finger_0.num_segs)
        self.determine_seg_percents("finger_1", self.hand_data.finger_1.num_segs)
        self.hand_data.ratio.finger_0 = right
        self.hand_data.ratio.finger_1 = left
        self.hand_data.length.palm = palm_width
        self.hand_data.length.finger_0 = finger_0_length
        self.hand_data.length.finger_1 = finger_1_length
        self.hand_data.update()
    
        return self.hand_data
            
    

