# robot_arm
Raw model design 

To use it, you have to install ros-humble-ros2-control and ros-humble-ros2-controllers packages.
see : https://control.ros.org/master/doc/getting_started/getting_started.html#installation for more info 

To download it,
download and unpack or clone repo into a clean workspace (src) directory 


To build it, go to workspace:

rosdep update --rosdistro=$ROS_DISTRO
sudo apt-get update
rosdep install --from-paths src --ignore-src -r -y

. /opt/ros/${ROS_DISTRO}/setup.sh
colcon build --symlink-install

To run it:
. install/setup.bash

ros2 launch moveit demo.launch.py 



