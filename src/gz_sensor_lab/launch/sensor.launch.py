"""Gazebo + the ros_gz bridge for one lab sensor, in one command.

    ros2 launch gz_sensor_lab sensor.launch.py sensor:=rgbd
    ros2 launch gz_sensor_lab sensor.launch.py sensor:=pressure
    ros2 launch gz_sensor_lab sensor.launch.py sensor:=rgbd extra_args:=-s   # no GUI

sensor:=<name> picks worlds/<name>.sdf and config/<name>.yaml. 
The listeners are started separately with 'ros2 run', so they can be restarted on their own
while the simulation keeps running.
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory("gz_sensor_lab")
    pkg_ros_gz_sim = get_package_share_directory("ros_gz_sim")

    sensor = LaunchConfiguration("sensor")
    world = PathJoinSubstitution([pkg_share, "worlds", [sensor, ".sdf"]])
    bridge_config = PathJoinSubstitution([pkg_share, "config", [sensor, ".yaml"]])

    # -r starts the simulation running rather than paused.
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, "launch", "gz_sim.launch.py")
        ),
        launch_arguments={
            "gz_args": [LaunchConfiguration("extra_args"), " -r ", world],
        }.items(),
    )

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        parameters=[{"config_file": bridge_config}],
        output="screen",
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "sensor",
                default_value="rgbd",
                description="Which lab sensor: rgbd | pressure.",
            ),
            DeclareLaunchArgument(
                "extra_args",
                default_value="",
                description="Extra `gz sim` arguments, e.g. -s for no GUI.",
            ),
            gazebo,
            bridge,
        ]
    )
