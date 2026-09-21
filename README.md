# gazebo_ros2

Gazebo Harmonic + ROS 2 Humble

```bash
./start.sh     # build + start the container
./enter.sh    # open terminal
```

### Run

```bash
colcon build --packages-select gz_sensor_lab && source install/setup.bash
ros2 launch gz_sensor_lab sensor.launch.py sensor:=rgbd      # or sensor:=pressure
ros2 run gz_sensor_lab rgbd_listener                         # second terminal; or pressure_listener
```

Add `extra_args:=-s` to the launch to run without the Gazebo window.

### Run

```bash
gz sim -s -r src/gz_sensor_lab/worlds/pressure.sdf     # 1. run the world
gz topic -l                                            # 2. what Gazebo publishes
ros2 run ros_gz_bridge parameter_bridge --ros-args \
    -p config_file:=src/gz_sensor_lab/config/pressure.yaml   # 3. bridge
ros2 topic list                                        # 4. check in ROS 2
```

Docs: [sensors](https://gazebosim.org/docs/harmonic/sensors) ·
[ros2_launch_gazebo](https://gazebosim.org/docs/harmonic/ros2_launch_gazebo)
