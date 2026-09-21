"""Lab 0.1 B: listen to the barometer and the altimeter.

The altimeter gives height (relative to where the box started) and vertical
speed directly; the barometer gives only pressure. The log shows all three.

    ros2 run gz_sensor_lab pressure_listener
"""
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from ros_gz_interfaces.msg import Altimeter
from sensor_msgs.msg import FluidPressure


class PressureListener(Node):
    def __init__(self):
        super().__init__("pressure_listener")
        self.create_subscription(FluidPressure, "/air_pressure", self.on_pressure, 10)
        self.create_subscription(Altimeter, "/altimeter", self.on_altimeter, 10)
        self.pressure = None  # Pa
        self.height = None  # m, relative to the start: 0 -> -1000
        self.speed = None  # m/s, negative while falling
        # Log twice a second, not at 30 Hz.
        self.create_timer(0.5, self.report)

    def on_pressure(self, msg):
        self.pressure = msg.fluid_pressure

        # TODO: processing for height estimation
        # International barometric formula (standard atmosphere):
        #     h = 44330.8 * (1 - (p / 101325) ** 0.190263)
        # Does it agree with the altimeter? (start: 1000.5 m, ground: 0.5 m)
        # Speed from how fast that height changes?

    def on_altimeter(self, msg):
        self.height = msg.vertical_position
        self.speed = msg.vertical_velocity

    def report(self):
        if self.pressure is None or self.height is None:
            self.get_logger().info("waiting for /air_pressure and /altimeter ...")
            return
        self.get_logger().info(
            f"height {self.height:9.2f} m  speed {self.speed:8.2f} m/s  "
            f"pressure {self.pressure:10.1f} Pa"
        )


def main():
    rclpy.init()
    node = PressureListener()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
