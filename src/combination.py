# By Marshall Saltz
import random
import numpy as np
from addict import Dict
import params


class crossoverFunctions:
    """
    Combines two hands to produce two children.
    Child 0:
        Palm width: decides to either keep old parent 1 or randomly generate new
        Finger 0: random
            Count: Parent 1 segment count
            Percents: Generate new percents
        Finger 1: Parent 0 ratio number
            Count: Parent 0 segment count
            Percents: Keep Parent 0 percents
    Child 1:
        Palm width: decides to either keep old parent 0 or randomly generate new
        Finger 0: Parent 1 ratio number
            Count: Parent 1 segment count
            Percents: Parent 1 percents
        Finger 1: random
            Count: Parent 0 segment count
            Pecents: Generate new percents
    """

    def __init__(self, p0, p1, comb_mode, ind, generation):
        """
        Initializes class.
        Parameters:
            p0 - first parent
            p1 - second parent
            comb_mode - eo or w for naming purposes
            ind - index of outside loop for naming purposes
            generation - generation number
        """
        self.generation = generation
        self.p0 = p0
        self.p1 = p1
        self.comb_mode = comb_mode
        self.ind = ind

    
    def determine_seg_percents(self, num_segs):
        """
        Randomly determines segments as percentages of the finger length.
        Parameters:
            num_segs - segment amount, 3 or 4 (really 2 or 3, but additional link of no length is added for the sim)
        Returns:
            list_of_ratios - list of segment percentages
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

        return list_of_ratios 
    
       	   
    def build_fingers(self, ls, finger, hand_data):
        """
        Generates measurements for a new finger.
        Parameters:
            ls - list of parent segment ratios
            finger - finger_0 or finger_1
            hand_data - child Dict()
        Returns:
            hand_data - child Dict() data
        """
        seg_ratios = []
        num_segs = len(ls)+1
        seg_ratios = self.determine_seg_percents(num_segs)
        hand_data[finger].num_segs = num_segs
        hand_data.ratio.segs[finger] = seg_ratios
        hand_data.update()
        
        return hand_data  
    
    
    def keep_finger(self, ls, finger, hand_data):
        """
        Keeps the old finger percentages and segement numbers.
        Parameters:
            ls - parent list of percentages
            finger - finger_0 or finger_1
            hand_data - child Dict()
        Returns:
            hand_data - updated child Dict()
        """
        seg_ratios = ls
        num_segs = len(ls)+1
        hand_data[finger].num_segs = num_segs
        hand_data.ratio.segs[finger] = seg_ratios
        hand_data.update()
        
        return hand_data
        

    def choose_palm_width(self, p):
        """
        Either keeps the old palm width or randomly generates a new one.
        Parameters:
            p - parent Dict()
        Returns:
            palm_width - either random or parent palmn width
        """
        choice = random.randint(1,3)
        if choice == 1:
            palm_width = p.length.palm
        else:
            palm_width = round(random.uniform(0.05, 0.09), 5)

        return palm_width
        

    def combo(self):
        """
        Combines the grippers.
        Returns:
            hand_data0 - child 0 Dict()
            hand_data1 - child 1 Dict()
        """
        hand_data0 = Dict()
        hand_data1 = Dict()

        
        fn0 = "child_0_" + str(self.generation) + "_" + str(self.ind) + "_" + self.comb_mode
        fn1 = "child_1_" + str(self.generation) + "_" + str(self.ind) + "_" + self.comb_mode
        
        c0f0 = random.randint(1,10) # child 0 finger 0 (random)
        c0f1 = self.p0.ratio.finger_1   # child 0 finger 1 (parent 0 percents)
        
        
        c1f0 = self.p1.ratio.finger_0   # child 1 finger 0 (parent 1 percents)
        c1f1 = random.randint(1,10) # child 1 finger 1 (random)
        
        total_length = 0.288    # combined length of both fingers

        # determine individual finger lengths
        # child 0
        finger_0_0 = (total_length/(c0f0+c0f1))*c0f0
        finger_0_1 = (total_length/(c0f0+c0f1))*c0f1
        # child 1
        finger_1_0 = (total_length/(c1f0+c1f1))*c1f0
        finger_1_1 = (total_length/(c1f0+c1f1))*c1f1

        
        # child 0
        hand_data0 = self.build_fingers(self.p1.ratio.segs.finger_0, "finger_0", hand_data0)    # finger 0 with new ratios and p1 seg count
        hand_data0 = self.keep_finger(self.p0.ratio.segs.finger_1, "finger_1", hand_data0)  # finger 1 with p0 ratios and seg count
        hand_data0.finger_1.num_segs = self.p0.finger_1.num_segs 
        hand_data0.ratio.segs.finger_1 = self.p0.ratio.segs.finger_1

        # child 1
        hand_data1 = self.build_fingers(self.p0.ratio.segs.finger_1, "finger_1", hand_data1)    # finger 1 with new ratios and p0 seg count
        hand_data1 = self.keep_finger(self.p1.ratio.segs.finger_0, "finger_0", hand_data1)  # finger 0 with p1 ratios and seg count
        hand_data1.finger_0.num_segs = self.p1.finger_0.num_segs 
        hand_data1.ratio.segs.finger_0 = self.p1.ratio.segs.finger_0
        
        
        # save data
        hand_data0.ratio.finger_0 = c0f0
        hand_data0.ratio.finger_1 = c0f1
        hand_data0.length.palm = self.choose_palm_width(self.p1)
        hand_data0.length.finger_0 = finger_0_0
        hand_data0.length.finger_1 = finger_0_1
        hand_data1.ratio.finger_0 = c1f0
        hand_data1.ratio.finger_1 = c1f1
        hand_data1.length.palm = self.choose_palm_width(self.p0)
        hand_data1.length.finger_0 = finger_1_0
        hand_data1.length.finger_1 = finger_1_1
        hand_data0.name = fn0
        hand_data1.name = fn1
        hand_data0.update()
        hand_data1.update()

        
        return hand_data0, hand_data1
    
    
