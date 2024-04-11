#!/usr/bin/env python3
import argparse
import rclpy
from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

def main(args=None):
    rclpy.init(args=args)

    parser = argparse.ArgumentParser(description='Send joint trajectory action goal')
    parser.add_argument('table1_joint', type=float, help='Position for table1_joint')
    parser.add_argument('tbone_joint', type=float, help='Position for tbone_joint')
    parser.add_argument('table3_joint', type=float, help='Position for table3_joint')
    parser.add_argument('table4_joint', type=float, help='Position for table4_joint')
    parser.add_argument('table5_joint', type=float, help='Position for table5_joint')
    parser.add_argument('--time_to_reach', type=int, default=1, help='Time to reach the desired position in seconds')
    parser.add_argument('--time_to_reach_ns', type=int, default=0, help='Time to reach the desired position in nanoseconds')
    args = parser.parse_args()

    # Create a ROS 2 node
    node = rclpy.create_node('trajectory_sender_node')

    # Create an Action Client for the FollowJointTrajectory action
    name_action_traj_base = "/joint_trajectory_controller/follow_joint_trajectory"
    action_client = ActionClient(node, FollowJointTrajectory, name_action_traj_base)

    # Wait for the action server to be available
    if not action_client.wait_for_server(timeout_sec=5.0):
        node.get_logger().error('Action server not available. Exiting...')
        return

    # Create a FollowJointTrajectory goal
    goal_msg = FollowJointTrajectory.Goal()
    goal_msg.trajectory = JointTrajectory()
    goal_msg.trajectory.joint_names = [ "table1_joint",
                                        "tbone_joint",
                                        "table3_joint",
                                        "table4_joint",
                                        "table5_joint"]

    # Create a trajectory point
    point = JointTrajectoryPoint()
     # Use the provided joint positions
    point.positions = [args.table1_joint,
                       args.tbone_joint,
                       args.table3_joint,
                       args.table4_joint,
                       args.table5_joint]
    point.time_from_start.sec = args.time_to_reach  # Use the provided time
    point.time_from_start.nanosec = args.time_to_reach_ns  # Use the provided time in nanoseconds

    # Add the trajectory point to the goal
    goal_msg.trajectory.points.append(point)

    # Send the goal to the action server
    future = action_client.send_goal_async(goal_msg)

    rclpy.spin_until_future_complete(node, future)

    if future.result() is not None:
        node.get_logger().info('Goal successfully completed.')
    else:
        node.get_logger().error('Goal failed to complete')

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
