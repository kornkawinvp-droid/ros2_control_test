import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_path

def generate_launch_description():

    joy_config = os.path.join(get_package_share_path("ros2_control_test"),"config","joy_config.yaml")

    return LaunchDescription([
        Node(
            package="joy",
            executable="joy_node",
        ),
        Node(
            package="teleop_twist_joy",
            executable="teleop_node",
            parameters=[joy_config]
        ),
    ])