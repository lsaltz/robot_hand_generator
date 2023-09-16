[![DOI](https://zenodo.org/badge/449414021.svg)](https://zenodo.org/badge/latestdoi/449414021)
# robot_hand_generator_MLS: evolutionary algorithm edition
A tool used to generate the best symmetrical two-fingered hand design to pick up and hold onto a cube. Currently tests the hand's range of motion while maintaining x distance between distal links.

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
    
    Currently, I have it set to run only in the terminal. If you wish to view the visual testing process(slower), navigate to:
    
    ```console
    cd ~/robot_hand_generator_MLS/src/
    ```
    Open the file with nano or your editor of choice:
    
    ```console
    nano testing.py
    ```
    And change:
     ```console
     physicsClient = p.connect(p.DIRECT)
    ```
    To:
     ```console
     physicsClient = p.connect(p.GUI)
    ```
   
## What the outputs mean:

After ea.py finishes running, it will send all the data it gathered to a text file called "results.txt" located in ~/robot_hand_generator_MLS/output.
It lists the winning hand and its location as well as its length ratios of palm to fingers and proximal to distal links. 
It also lists the runner up hand and the results of the other hands. 
In the output folder, you can also find a graph of the overall fitness trend, an overall graph of all the points from the top 10%, and graphs of the top and bottom 10% of grippers generated. 

Some examples of what this looks like are:
![alt text](https://github.com/lsaltz/robot_hand_generator_MLS/blob/main/imgs/results.png?raw=true)
![alt text](https://github.com/lsaltz/robot_hand_generator_MLS/blob/main/imgs/fitness_trend.png?raw=true)
<p align="left">Winning hand: </p>

![alt text](https://github.com/lsaltz/robot_hand_generator_MLS/blob/main/imgs/child_0_5_2m.png?raw=true)

<p align="left">Overall points of top 10%: </p>

![alt text](https://github.com/lsaltz/robot_hand_generator_MLS/blob/main/imgs/overall_graph.png?raw=true)

Currently the maximum amount of times this code has been run is 25. I plan to run it 500 times once I return to my desktop.

## Todo:
- Optimize
- Run 500+ times


## Additional Notes:
If you wish to run this software more than once, clear your outputs and points folders. If you run into issues with MESA and OpenGL, add the following to ~/.bashrc:
```
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
```
This project was originally created by Josh Campbell, and has been adjusted by me. The original repository can be found at:
https://github.com/OSUrobotics/robot_hand_generator

