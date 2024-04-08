# robot_arm
Raw model design 

To use it, you have to install ros-humble-ros2-control and ros-humble-ros2-controllers packages.
see : https://control.ros.org/master/doc/getting_started/getting_started.html#installation for more info 

a complete install of moveit2 
https://moveit.picknik.ai/main/doc/tutorials/getting_started/getting_started.html
for install instructions.

download and unpack or clone repo into a clean workspace (src) directory 


To build it, go to workspace:

rosdep update --rosdistro=$ROS_DISTRO
sudo apt-get update
rosdep install --from-paths src --ignore-src -r -y

. /opt/ros/${ROS_DISTRO}/setup.sh
colcon build --symlink-install



To run it:
. install/setup.bash

before running place the .setup_assistant fire in the arm_moveit directory or run the setup assistant to generate the robot arm 


ros2 launch moveit demo.launch.py 



