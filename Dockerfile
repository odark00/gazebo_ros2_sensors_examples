# Gazebo Harmonic + ROS 2 Humble sandbox for the sensor labs
#
# Built on the visual-odometry image, which already ships Gazebo 8, the
# Harmonic-built ros_gz (in /root/ardu_ws), RViz, OpenCV and cv_bridge 
FROM ardupilot-visual-odom:latest

# colcon build there
ENV VO_WS=/root/gazebo_ros2

WORKDIR /root/gazebo_ros2
CMD ["bash"]
