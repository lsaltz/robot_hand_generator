# By Marshall Saltz
import json
from addict import Dict

class Build_Json:
    """
    Generates json file from hand data for sim purposes.
    """

    def __init__(self, hand_data):
        """
        Initializes class.
        Parameters:
            hand_data - gripper data for generation
        """
        self.robot_gripper = Dict() # json dictionary to be created
        self.hand_data = hand_data
        
        
    def finger_1(self, palm_width, segment_count_1):
        """
        Generate data for finger_1.
        Parameters:
            palm_width - gripper palm width
            segment_count_1 - finger_1 segment count
        """
        self.robot_gripper.hand.palm.palm_joints.finger_1.joint_pose = palm_width/2, 180, -180
        self.robot_gripper.hand.palm.palm_joints.finger_1.joint_style = "pin"
        self.robot_gripper.hand.palm.palm_joints.finger_1.joint_dimensions = 0.0083, 0.006, 0.0108
        self.robot_gripper.hand.finger_1.segment_qty = segment_count_1
        self.robot_gripper.hand.finger_1.finger_pose = palm_width/2, 180, -180
        
       	
    def finger_0(self, palm_width, segment_count_0):
        """
        Generate data for finger_0.
        Parameters:
            palm_width - gripper palm width
            segment_count_1 - finger_0 segment count
        """
        self.robot_gripper.hand.palm.palm_joints.finger_0.joint_pose = palm_width/2, 0, 0
        self.robot_gripper.hand.palm.palm_joints.finger_0.joint_style = "pin"
        self.robot_gripper.hand.palm.palm_joints.finger_0.joint_dimensions = 0.0083, 0.006, 0.0108
        self.robot_gripper.hand.finger_0.segment_qty = segment_count_0
        self.robot_gripper.hand.finger_0.finger_pose = palm_width/2, 0, 0
        
    def build_segment(self, finger, i, link_length):
        """
        Generates data for each segment.
        Parameters:
            finger - finger_1 or finger_0
            i - segment number
            link_length - segment length
        """
        segment = f"segment_{i}"
        self.robot_gripper.hand[finger][segment].segment_profile = [0.0, 0.0, 0], [0, 0.0, 0]
        self.robot_gripper.hand[finger][segment].segment_dimensions = 0.0322, 0.0165, link_length	
        self.robot_gripper.hand[finger][segment].segment_bottom_joint.joint_style = "pin"
        self.robot_gripper.hand[finger][segment].segment_bottom_joint.joint_dimensions = 0.0083, 0.006, 0.0108	
        self.robot_gripper.hand[finger][segment].segment_bottom_joint.joint_range = 0, 180
        self.robot_gripper.hand[finger][segment].segment_bottom_joint.joint_friction = "n/a"
        self.robot_gripper.hand[finger][segment].segment_top_joint.joint_style = "pin"
        self.robot_gripper.hand[finger][segment].segment_top_joint.joint_dimensions = 0.01, 0.0162, 0.00925	
        self.robot_gripper.hand[finger][segment].segment_top_joint.joint_range = 0, 180
        self.robot_gripper.hand[finger][segment].segment_top_joint.joint_friction = "n/a"
        self.robot_gripper.hand[finger][segment].segment_sensors.sensor_qty = 0


    def last_link(self, finger, i):
        """
        Generates data for last link of size 0.
        Parameters:
            finger - finger_0 or finger_1
            i - segment number
        """
        segment = f"segment_{i}"
        self.robot_gripper.hand[finger][segment].segment_profile = [0, 0.0, 0], [0, 0.0, 0],[0, 0.0, 0.01], [0, 0.0, 0.01]
        self.robot_gripper.hand[finger][segment].segment_dimensions = 0, 0, 0    	    
        self.robot_gripper.hand[finger][segment].segment_bottom_joint.joint_style = "pin"
        self.robot_gripper.hand[finger][segment].segment_bottom_joint.joint_dimensions = 0,0,0	#return to this
        self.robot_gripper.hand[finger][segment].segment_bottom_joint.joint_range = 0, 180
        self.robot_gripper.hand[finger][segment].segment_bottom_joint.joint_friction = "n/a"
        self.robot_gripper.hand[finger][segment].segment_sensors.sensor_qty = 0
        
        
    def determine_seg_lengths(self, finger_length, finger, num_segs):
        """
        Gets segment lengths from list of ratios.
        Parameters:
            finger_length - length of finger (mm)
            finger - finger_0 or finger_1
            num_segs - number of segments on finger
        """
        list_of_ratios = self.hand_data.ratio.segs[finger]
        for i in range(len(list_of_ratios)):
            link_length = (finger_length*list_of_ratios[i])/100
            self.build_segment(finger, i, link_length)
        self.last_link(finger, num_segs-1)
        

    def build_hand(self):
        """
        Puts the entire gripper json data together.
        """
        # grab data
        file_name = self.hand_data.name
        
        palmz = 0.053
        palmx = 0.032

        self.hand_data.finger_0.num_segs = len(self.hand_data.ratio.segs.finger_0) + 1
        self.hand_data.finger_1.num_segs = len(self.hand_data.ratio.segs.finger_1) + 1

        right = self.hand_data.ratio.finger_0
        left = self.hand_data.ratio.finger_1
        
        palm_width = self.hand_data.length.palm

        fingers_total_length = 0.288
        finger_0_length = fingers_total_length/(right+left) * right
        finger_1_length = fingers_total_length - finger_0_length
        
        # put data into new Dict()
        self.robot_gripper.hand.hand_name = file_name
        self.robot_gripper.hand.palm.palm_style = "cuboid"
        self.robot_gripper.hand.palm.palm_dimensions = palmx, palm_width, palmz
        
        self.robot_gripper.hand.palm.finger_qty = 2
        self.finger_0(palm_width, self.hand_data.finger_0.num_segs)
        self.determine_seg_lengths(finger_0_length, "finger_0", self.hand_data.finger_0.num_segs)
        self.finger_1(palm_width, self.hand_data.finger_1.num_segs)
        self.determine_seg_lengths(finger_1_length, "finger_1", self.hand_data.finger_1.num_segs)
        self.robot_gripper.objects.object_qty = 0
        
        self.robot_gripper.update()
        
        # Dump it all in a json file which can then be used to generate a urdf for sim purposes
        with open(f'../hand_json_files/hand_queue_json/{file_name}.json', mode="w+") as jfile:        
            new_json = ""
            new_json += json.dumps(self.robot_gripper, indent=4)  
            jfile.write(new_json)
        jfile.close()       

        self.robot_gripper.clear()        
        
            
    

