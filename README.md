[![DOI](https://zenodo.org/badge/449414021.svg)](https://zenodo.org/badge/latestdoi/449414021)
# robot_hand_generator_MLS: evolutionary algorithm edition
A tool used to generate the best symmetrical two-fingered hand design to pick up and hold onto a cube. Currently tests the hand's range of motion while maintaining x distance between distal links.
This tool runs three different tests and generates the best two-fingered gripper as found by each of those tests. The tests consist of:
- the number of reachable center points as separated by a horizontal line of a fixed width
- the number of reachable center points as separated by lines of fixed widths at different angles
- the area of overlap between both fingers' reachable space, found using inverse kinematics
  
## Requirements:
- Linux OS or WSL with ubuntu


## Install and Setup:
Ubuntu is currently the only tested method for executing this program.


1. Run the following commands:

    First, update your machine:
    
    ```console
    sudo apt update
    sudo apt upgrade
    ```
    Next, copy the following lines into the terminal:
    ```
    cd ~/
    ```
    ```
    git clone https://github.com/lsaltz/robot_hand_generator_MLS.git
    ```
    ```
    cd ~/robot_hand_generator_MLS/
    ```
    ```
    chmod u+x setup.sh
    ```
    ```
    ./setup.sh
    ```

    * This will set up the environment.
    
2. After the environment has finished setting up (this will take some time), run the evolutionary algorithm, open:

    ```console
    cd ~/robot_hand_generator_MLS/src/
    ```
   
   And run:
    
    ```console
    python3 ea.py
    ```
    and specify for how many generations you would like to run it for. The more you enter, the longer it will take. 
    
   
## What the outputs mean:

After ea.py finishes running, it will send all the data it gathered from each test to three separate results text files located in ~/robot_hand_generator_MLS/output.

In the output folder you can also find a graph of the overall fitness trend and charts of the tests conducted on the top 10 hands.

Some examples of what this looks like are:

<p align="left">Winning hand: </p>

![alt text](https://github.com/lsaltz/robot_hand_generator_MLS/blob/main/imgs/child_496_0w_t_s.png?raw=true)
![alt text](https://github.com/lsaltz/robot_hand_generator_MLS/blob/main/imgs/child_496_0w_t_t.png?raw=true)
![alt text](https://github.com/lsaltz/robot_hand_generator_MLS/blob/main/imgs/child_520_0w_s_a.png?raw=true)


## Todo:


## Additional Notes:
If you wish to run this software more than once, clear your outputs and points folders. If you run into issues with MESA and OpenGL, add the following to ~/.bashrc:
```
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
```
This project was originally created by Josh Campbell, and has been adjusted by me. The original repository can be found at:
https://github.com/OSUrobotics/robot_hand_generator
