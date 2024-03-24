from launch import LaunchDescription
from launch.actions import ExecuteProcess


def generate_launch_description():

    # load and START the controllers in launch file

    load_joint_state_broadcaster = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller',
             '--set-state', 'active', 'joint_state_broadcaster'],
        output='screen')

    load_robot_arm_system_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state',
             'active', 'robot_arm_system_controller'],
        output='screen')
    
    

    return LaunchDescription([load_joint_state_broadcaster, load_robot_arm_system_controller])
