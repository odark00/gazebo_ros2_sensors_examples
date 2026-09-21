#!/bin/bash
# Opens a shell in the running container (ROS 2 + ros_gz already sourced).
exec docker exec -it gazebo_ros2 bash "$@"
