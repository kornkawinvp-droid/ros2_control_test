import os
from launch import LaunchDescription
from launch.actions import TimerAction
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_path


def generate_launch_description():
    urdf_path = os.path.join(
        get_package_share_path("ros2_control_test"), "urdf", "robot_description.urdf.xacro"
    )

    controller_config = os.path.join(
        get_package_share_path("ros2_control_test"), "config", "controller_config.yaml"
    )

    ekf_config = os.path.join(
        get_package_share_path("ros2_control_test"), "config", "ekf_config.yaml"
    )

    robot_description = ParameterValue(
        Command(["xacro ", urdf_path]), value_type=str
    )


    return LaunchDescription([

        Node(
            package='micro_ros_agent',
            executable='micro_ros_agent',
            name='micro_ros_agent',
            arguments=['serial', '--dev', '/dev/ttyACM0', '-b', '921600'],
            output='screen'
        ),
        # 1. Robot State Publisher — publish /robot_description (latched)
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{"robot_description": robot_description}],
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='imu_tf',
            arguments=[
                '--x', '0', '--y', '0', '--z', '0',
                '--roll', '0', '--pitch', '0', '--yaw', '0',
                '--frame-id', 'base_link',
                '--child-frame-id', 'imu_link'
            ],
        ),

        Node(
            package="controller_manager",
            executable="ros2_control_node",
            parameters=[controller_config],
            output="both",
        ),

        # 3. Spawners
        TimerAction(period=1.0, actions=[
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=["joint_state_broadcaster"],
            )
        ]),
        TimerAction(period=2.0, actions=[
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=["mecanum_drive_controller"],
            )
        ]),

        Node(
            package='ros2_control_test',
            executable='cmd_vel_yflip',
            name='cmd_vel_yflip',
        ),

        Node(
                package='robot_localization',
                executable='ekf_node',
                name='ekf_filter_node',
                output='screen',
                parameters=[ekf_config, {'use_sim_time': False}],
            ),

        Node(
                package='sllidar_ros2',
                executable='sllidar_node',
                name='sllidar_node',
                parameters=[{
                    'serial_port':      '/dev/ttyUSB0',
                    'serial_baudrate':  460800,
                    'frame_id':         'lidar_link',
                    'inverted':         False,
                    'angle_compensate': True,
                }],
                output='screen'
            ),

    ])