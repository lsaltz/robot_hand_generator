#Adapted from its original by Marshall Saltz

import pybullet as p
import pybullet_data
import pathlib
import time

def load(file_path):
    # Resource paths
    #current_path = str(pathlib.Path().resolve())

    #hand_path = current_path + "INSERT PATH TO FILE HERE EX: /data/hand.urdf"

    hand_path = file_path

    #hand_path = current_path + "INSERT PATH TO FILE HERE EX: /data/hand.urdf"

    # Setup simulator

    physics_client = p.connect(p.GUI, options="--opengl2")

    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    p.setGravity(0, 0, -10)

    p.resetDebugVisualizerCamera(cameraDistance=.02, cameraYaw=0, cameraPitch=-89.9999, cameraTargetPosition=[0, 0.1, 0.5])



    # load plane object

    plane_id = p.loadURDF("plane.urdf")

    # load hand object, you can also chang the base orientation if you would like
    # Make sure that the z is high enough so it does not clip the ground plane
    LinkId = []
    hand_id = p.loadURDF(hand_path, useFixedBase=True, basePosition=[0.0, 0.0, 0.05])
    for i in range(0, p.getNumJoints(hand_id)):
            
        p.setJointMotorControl2(hand_id, i, p.POSITION_CONTROL, targetPosition=0, force=0)
        linkName = p.getJointInfo(hand_id, i)[12].decode("ascii")
        if "sensor" in linkName:
            LinkId.append("skip")
        else:
            LinkId.append(p.addUserDebugParameter(linkName, -3.14, 3.14, 0))

    # Keeps sim window open until you exit
    while p.isConnected():
        p.stepSimulation()
        time.sleep(1./240.)

        for i in range(0, len(LinkId)):
            if LinkId[i] != "skip":
                linkPos = p.readUserDebugParameter(LinkId[i])
                p.setJointMotorControl2(hand_id, i, p.POSITION_CONTROL, targetPosition=linkPos)


if __name__ == "__main__":
    load("../output/child_1_52_1w_a/hand/child_1_52_1w_a.urdf")
