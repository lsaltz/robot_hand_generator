# Apapted from Josh Campbell by Marshall Saltz

import random
import copy
import numpy as np
import os
import json
from addict import Dict

class crossoverFunctions:

    def __init__(self, generation):
        self.dictionary = Dict()
        self.generation = generation
        
    """
    This converts the json files to dictionaries, and takes in an argument
    of the json file.
    """
    def json_to_dictionaries(self, jfile):
        with open(jfile, mode="r") as parentfile:
            dictionary = json.load(parentfile)
            parent = Dict(dictionary)
            parentfile.close()
        print("parent dictionaries created")
        return parent

    """
    This counts the segments and takes a dictionary as an argument It returns two segments counts: one for each finger.
    """
    def segment_counter(self, parent):
        segment_countF0 = parent.hand.finger_0.segment_qty
        segment_countF1 = parent.hand.finger_1.segment_qty
        print("segments counted...")
        return segment_countF0, segment_countF1
    
    """
    This sets up a new dictionary for the children.
    """
    def new_dictionary(self, num):
        dictionary = Dict()
        dictionary.hand.hand_name = "child_hand_" + str(num) + "_gen_" + str(self.generation)
        dictionary.hand.palm.palm_style = "cuboid"
        dictionary.hand.palm.palm_dimensions = 0.032, 0.075, 0.053
        dictionary.hand.palm.finger_qty = 2

        random1 = random.random()
        random2 = random.random()
        random3 = random.random()

        dictionary.hand.palm.palm_joints.finger_0.joint_pose = 0.02675, 0, 0
        dictionary.hand.palm.palm_joints.finger_0.joint_style = "pin"
        dictionary.hand.palm.palm_joints.finger_0.joint_dimensions = random1, random2, random3

        dictionary.hand.palm.palm_joints.finger_1.joint_pose = 0.02675, 180, -180
        dictionary.hand.palm.palm_joints.finger_1.joint_style = "pin"
        dictionary.hand.palm.palm_joints.finger_1.joint_dimensions = random1, random2, random3
            
        dictionary.hand.finger_0.finger_pose = 0.02675, 0, 0  
        dictionary.update()
        print("new dictionary created")
        return dictionary
        
    """
    If the two segments have an equal count, then one child has 0 segments on one finger, 
    and on the other the segments are swapped.
    """
    def equivalent_fingers(self, parent1, parent2, finger, segment_count):
    #if a==b c1 = 0 segments and c0 = swapped segments
        c0 = Dict()
        c1 = self.new_dictionary(1)
        c1.hand[finger].segment_qty = 0
        c0 = copy.deepcopy(parent1)
        
        for i in range(0, segment_count, 2):
            segment_name = "segment_" + str(i)
            c0.hand[finger][segment_name] = parent2.hand[finger][segment_name]
        return c0, c1

    """
    If one finger has more segments, this takes the difference from the finger with more segments.
    """
    def difference(self, lesser_parent, greater_parent, lesser_segments, greater_segments, finger):
        difference_child = self.new_dictionary(1)
        difference_child = copy.deepcopy(greater_parent)
        difference = greater_segments - lesser_segments
        
        difference_child.hand[finger].segment_qty = difference
        print("difference: " + str(difference))
        for i in range(lesser_segments):
            segment_name = "segment_" + str(difference + i)
            difference_child.hand[finger].pop(segment_name)
        return difference_child
        
    """
    This combines the leftovers after the difference is taken from the greater finger.
    """        
    def leftovers(self, lesser_parent, greater_parent, lesser_segments, greater_segments, finger):
        
        leftovers_child = self.new_dictionary(0)
        leftovers_child = copy.deepcopy(lesser_parent)
        dif = greater_segments - lesser_segments
        new_count = lesser_segments * 2
        leftovers_child.hand[finger].segment_qty = new_count
        for i in range(lesser_segments):
            segment_name = "segment_" + str(i)
            segment_name2 = "segment_" + str(lesser_segments + i)
            leftovers_child.hand[finger][segment_name2].update(greater_parent.hand[finger][segment_name])
        return leftovers_child
    
           
    """
    This compares the segments on each finger, and runs the above functions based on those comparisons.
    """                
    def segment_count_comparator(self, a, b, a_segments, b_segments, finger):
        
        if a_segments > b_segments:
            child1 = self.difference(b, a, b_segments, a_segments, finger)
            child0 = self.leftovers(b, a, b_segments, a_segments, finger)
        elif a_segments < b_segments:
            child1 = self.difference(a, b, a_segments, b_segments, finger)
            child0 = self.leftovers(a, b, a_segments, b_segments, finger)
        else:
            child0, child1 = self.equivalent_fingers(a, b, finger, a_segments)
        print("segments compared and new dictionary for each finger is created.")
        return child0, child1

    """
    This updates the dictionaries with the new information.
    """                
    def update_dictionaries(self, finger0, finger1, num):
        new = self.new_dictionary(num)
        finger0.hand.finger_1 = copy.deepcopy(finger1.hand.finger_1)
        new = copy.deepcopy(finger0)
        print("digits finger 0: "+ str(new.hand.finger_0.segment_qty))
        print("digits finger 1:" + str(new.hand.finger_1.segment_qty))
        print("dictionary updated")
        return new
        
        
    """
    This converts the dictionaries to json files.
    """  
    def write_to_json(self, finger0, finger1, num):
        child = self.update_dictionaries(finger0, finger1, num)
        child.objects.object_qty = 0
        print("child_" + child.hand.hand_name)
        with open('../hand_json_files/hand_queue_json/{0}.json'.format("child_"+str(child.hand.hand_name)), mode = "w") as f:
            new_json = json.dumps(child, indent=4)
            f.write(new_json)
            f.close()