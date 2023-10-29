import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
from launch_ros.actions import Node
import os
from launch_ros.descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
from launch.actions import ExecuteProcess

def generate_launch_description():
    pkg_share = launch_ros.substitutions.FindPackageShare(package='robot_arm_description').find('robot_arm_description')
    default_model_path = os.path.join(pkg_share, 'urdf/robot_arm.xacro')
    use_sim_time = LaunchConfiguration('use_sim_time')

    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'use_sim_time': use_sim_time},{'robot_description': ParameterValue(Command(['xacro ', LaunchConfiguration('model')]),value_type=str)}]
    )
    spawn_entity_node = launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'test_robot', '-topic', 'robot_description'],
        parameters= [{'use_sim_time': use_sim_time}],
        output='screen'
    )
    
    world_file_name = 'empty_world.world'
    world = os.path.join(get_package_share_directory('robot_arm_description'), 'worlds', world_file_name)
    gazebo_node = ExecuteProcess(cmd=['gazebo', '--verbose', world,'-s', 'libgazebo_ros_factory.so'], output='screen')

    # load and START the controllers in launch file
    load_joint_state_broadcaster = ExecuteProcess(
										cmd=['ros2', 'control', 'load_controller', '--set-state', 'start','joint_state_broadcaster'],
										output='screen')
    load_joint_trajectory_controller = ExecuteProcess( 
										cmd=['ros2', 'control', 'load_controller', '--set-state', 'start', 'joint_trajectory_controller'], 
										output='screen')

    return launch.LaunchDescription([
        launch.actions.ExecuteProcess(cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'], 
                                           output='screen'),
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='True',
                                description='Flag to enable use_sim_time'),
        launch.actions.DeclareLaunchArgument(name='model', default_value=default_model_path,
                                            description='Absolute path to robot urdf file'),
        robot_state_publisher_node,
        spawn_entity_node,
    ])