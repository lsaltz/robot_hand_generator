# By Marshall Saltz

import random
import numpy as np
import os
import json
from addict import Dict

"""
This file mutates the segment amount and size, creating mutated files.
"""

def mutate(mutationsNum, max_segments, generation):
    robot_gripper = Dict()
    
    list_of_dics = []
    i = 0
    while (i < mutationsNum):
        hand_data = Dict()
        upper = 10
        lower = 1
        total_size = 0.36
        ratio_palm = np.random.randint(lower, upper)
        ratio_fingers = np.random.randint(lower, upper)
        ratio_proximal = np.random.randint(lower, upper)
        ratio_distal = np.random.randint(lower, upper)
        palm_width = (total_size / (ratio_palm + ratio_fingers)) * ratio_palm
        finger_length = (total_size / (ratio_palm + ratio_fingers)) * ratio_fingers
        proximal_length = (finger_length / (ratio_proximal + ratio_distal)) * ratio_proximal
        distal_length = (finger_length / (ratio_proximal + ratio_distal)) * ratio_distal
        palmz = 0.053
        palmx = 0.032
        file_name = "hand_mut_" + str(i) + '_gen_' + str(generation)
        
        hand_data.name = file_name
        hand_data.palm = ratio_palm
        hand_data.fingers = ratio_fingers
        hand_data.proximal = ratio_proximal
        hand_data.distal = ratio_distal
        hand_data.total_height = palmz + finger_length
        hand_data.palm_z = palmz
        hand_data.finger_z = finger_length
        hand_data.update()
        list_of_dics.append(hand_data)
        
        print("Ratios used for: {} are(palm to fingers): {}:{} and(proximal to distal): {}:{}".format(file_name, ratio_palm, ratio_fingers, ratio_proximal, ratio_distal))
        segment_count_0 = max_segments	#np.random.randint(1, max_segments)
        segment_count_1 = max_segments	#np.random.randint(1, max_segments)

        robot_gripper.hand.hand_name = file_name
        robot_gripper.hand.palm.palm_style = "cuboid"
        robot_gripper.hand.palm.palm_dimensions = palmx, palm_width, palmz
        robot_gripper.hand.palm.finger_qty = 2


        robot_gripper.hand.palm.palm_joints.finger_0.joint_pose = palm_width/2, 0, 0
        robot_gripper.hand.palm.palm_joints.finger_0.joint_style = "pin"
        robot_gripper.hand.palm.palm_joints.finger_0.joint_dimensions = 0.0083, 0.006, 0.0108	#return to this

        robot_gripper.hand.palm.palm_joints.finger_1.joint_pose = palm_width/2, 180, -180
        robot_gripper.hand.palm.palm_joints.finger_1.joint_style = "pin"
        robot_gripper.hand.palm.palm_joints.finger_1.joint_dimensions = 0.0083, 0.006, 0.0108	#return to this WDL
            
        robot_gripper.hand.finger_0.segment_qty = segment_count_0
        robot_gripper.hand.finger_0.finger_pose = palm_width/2, 0, 0
       
        robot_gripper.hand.finger_0.segment_0.segment_profile = [0.0, 0.0, 0], [0, 0.0, 0]
        robot_gripper.hand.finger_0.segment_0.segment_dimensions = 0.0322, 0.0165, proximal_length	#return to this
        robot_gripper.hand.finger_0.segment_0.segment_bottom_joint.joint_style = "pin"
        robot_gripper.hand.finger_0.segment_0.segment_bottom_joint.joint_dimensions = 0.0083, 0.006, 0.0108	
       	robot_gripper.hand.finger_0.segment_0.segment_bottom_joint.joint_range = 0, 180
       	robot_gripper.hand.finger_0.segment_0.segment_bottom_joint.joint_friction = "n/a"
        robot_gripper.hand.finger_0.segment_0.segment_top_joint.joint_style = "pin"
       	robot_gripper.hand.finger_0.segment_0.segment_top_joint.joint_dimensions = 0.01, 0.0162, 0.00925	
       	robot_gripper.hand.finger_0.segment_0.segment_top_joint.joint_range = 0, 180
       	robot_gripper.hand.finger_0.segment_0.segment_top_joint.joint_friction = "n/a"
       	robot_gripper.hand.finger_0.segment_0.segment_sensors.sensor_qty = 0

        robot_gripper.hand.finger_0.segment_1.segment_profile = [0, 0.0, 0], [0, 0.0, 0]
       	robot_gripper.hand.finger_0.segment_1.segment_dimensions = 0.0322, 0.0213, distal_length	
        robot_gripper.hand.finger_0.segment_1.segment_bottom_joint.joint_style = "pin"
        robot_gripper.hand.finger_0.segment_1.segment_bottom_joint.joint_dimensions = 0.01, 0.0162, 0.00925	
        robot_gripper.hand.finger_0.segment_1.segment_bottom_joint.joint_range = 0, 180
       	robot_gripper.hand.finger_0.segment_1.segment_bottom_joint.joint_friction = "n/a"
       	robot_gripper.hand.finger_0.segment_1.segment_top_joint.joint_style = "pin"
        robot_gripper.hand.finger_0.segment_1.segment_top_joint.joint_dimensions = 0,0,0	#return to this
        robot_gripper.hand.finger_0.segment_1.segment_top_joint.joint_range = 0, 180
       	robot_gripper.hand.finger_0.segment_1.segment_top_joint.joint_friction = "n/a"
        robot_gripper.hand.finger_0.segment_1.segment_sensors.sensor_qty = 0
        
        robot_gripper.hand.finger_0.segment_2.segment_profile = [0, 0.0, 0], [0, 0.0, 0],[0, 0.0, 0.01], [0, 0.0, 0.01]
       	robot_gripper.hand.finger_0.segment_2.segment_dimensions = 0, 0, 0    	
       	robot_gripper.hand.finger_0.segment_2.segment_bottom_joint.joint_style = "pin"
        robot_gripper.hand.finger_0.segment_2.segment_bottom_joint.joint_dimensions = 0,0,0	#return to this
        robot_gripper.hand.finger_0.segment_2.segment_bottom_joint.joint_range = 0, 180
       	robot_gripper.hand.finger_0.segment_2.segment_bottom_joint.joint_friction = "n/a"
       	
       	robot_gripper.hand.finger_0.segment_2.segment_sensors.sensor_qty = 0
       	
       	
        robot_gripper.hand.finger_1.segment_qty = segment_count_1
        robot_gripper.hand.finger_1.finger_pose = palm_width/2, 180, -180

        robot_gripper.hand.finger_1.segment_0.segment_profile = [0, 0, 0], [0, 0, 0]
       	robot_gripper.hand.finger_1.segment_0.segment_dimensions = 0.0322, 0.0165, proximal_length	
        robot_gripper.hand.finger_1.segment_0.segment_bottom_joint.joint_style = "pin"
       	robot_gripper.hand.finger_1.segment_0.segment_bottom_joint.joint_dimensions = 0.008, 0.006, 0.01083	
       	robot_gripper.hand.finger_1.segment_0.segment_bottom_joint.joint_range = 0, 180
       	robot_gripper.hand.finger_1.segment_0.segment_bottom_joint.joint_friction = "n/a"
        robot_gripper.hand.finger_1.segment_0.segment_top_joint.joint_style = "pin"
       	robot_gripper.hand.finger_1.segment_0.segment_top_joint.joint_dimensions = 0.01, 0.0162, 0.00925	
       	robot_gripper.hand.finger_1.segment_0.segment_top_joint.joint_range = 0, 180
       	robot_gripper.hand.finger_1.segment_0.segment_top_joint.joint_friction = "n/a"
       	robot_gripper.hand.finger_1.segment_0.segment_sensors.sensor_qty = 0

        robot_gripper.hand.finger_1.segment_1.segment_profile = [0, 0.0, 0], [0, 0.0, 0]
       	robot_gripper.hand.finger_1.segment_1.segment_dimensions = 0.0322, 0.0213, distal_length	
        robot_gripper.hand.finger_1.segment_1.segment_bottom_joint.joint_style = "pin"
       	robot_gripper.hand.finger_1.segment_1.segment_bottom_joint.joint_dimensions = 0.01, 0.0162, 0.00925	
       	robot_gripper.hand.finger_1.segment_1.segment_bottom_joint.joint_range = 0, 180
       	robot_gripper.hand.finger_1.segment_1.segment_bottom_joint.joint_friction = "n/a"
       	robot_gripper.hand.finger_1.segment_1.segment_top_joint.joint_style = "pin"
        robot_gripper.hand.finger_1.segment_1.segment_top_joint.joint_dimensions = 0, 0, 0	#return to this
        robot_gripper.hand.finger_1.segment_1.segment_top_joint.joint_range = 0, 180
       	robot_gripper.hand.finger_1.segment_1.segment_top_joint.joint_friction = "n/a"
        robot_gripper.hand.finger_1.segment_1.segment_sensors.sensor_qty = 0
        
        robot_gripper.hand.finger_1.segment_2.segment_profile = [0, 0.0, 0], [0, 0.0, 0],[0, 0.0, 0.01], [0, 0.0, 0.01]
       	robot_gripper.hand.finger_1.segment_2.segment_dimensions = 0, 0, 0    	
       	robot_gripper.hand.finger_1.segment_2.segment_bottom_joint.joint_style = "pin"
        robot_gripper.hand.finger_1.segment_2.segment_bottom_joint.joint_dimensions = 0,0,0	#return to this
        robot_gripper.hand.finger_1.segment_2.segment_bottom_joint.joint_range = 0, 180
       	robot_gripper.hand.finger_1.segment_2.segment_bottom_joint.joint_friction = "n/a"
       	
       	robot_gripper.hand.finger_1.segment_2.segment_sensors.sensor_qty = 0
        
        robot_gripper.objects.object_qty = 0

        robot_gripper.update()
        
        with open('../hand_json_files/hand_queue_json/' + file_name + '.json', mode="w") as jfile:        
            new_json = ""
            new_json += json.dumps(robot_gripper, indent=4)
                
            jfile.write(new_json)
            jfile.close()       
        i += 1
        
        robot_gripper.clear()
        
        
        print("A new hand has been mutated.")
    return list_of_dics
