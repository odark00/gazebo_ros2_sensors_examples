"""Lab 0.1 A: listen to the RGBD camera.

Subscribes to the colour image and the depth image and turns each into a
numpy array. The log shows the image size and the depth at the centre pixel;

    ros2 run gz_sensor_lab rgbd_listener
"""
import numpy as np
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import Image


def image_to_array(msg):
    """sensor_msgs/Image -> numpy array, for the two encodings Gazebo sends."""
    if msg.encoding == "rgb8":
        return np.frombuffer(msg.data, np.uint8).reshape(msg.height, msg.width, 3)
    if msg.encoding == "32FC1":
        return np.frombuffer(msg.data, np.float32).reshape(msg.height, msg.width)
    raise ValueError(f"unhandled encoding {msg.encoding}")


class RgbdListener(Node):
    def __init__(self):
        super().__init__("rgbd_listener")
        self.create_subscription(Image, "/rgbd_camera/image", self.on_image, 10)
        self.create_subscription(Image, "/rgbd_camera/depth_image", self.on_depth, 10)
        self.rgb = None
        self.depth = None
        # Log once a second, not at 30 Hz.
        self.create_timer(1.0, self.report)

    def on_image(self, msg):
        self.rgb = image_to_array(msg)

        # TODO: processing on the colour image (H x W x 3, RGB, uint8).
        # e.g. threshold on colour to find the red box, cv2.Canny for edges ...

    def on_depth(self, msg):
        # Metres. Pixels with nothing in range are +inf (sky) - mask them.
        self.depth = image_to_array(msg)

        # TODO: processing on the depth image (H x W, float32 metres).
        # e.g. distance to the nearest object, the depth of the red pixels ...

    def report(self):
        if self.rgb is None or self.depth is None:
            self.get_logger().info("waiting for /rgbd_camera/image and depth_image ...")
            return
        h, w = self.depth.shape
        self.get_logger().info(
            f"image {w}x{h}  mean rgb {self.rgb.reshape(-1, 3).mean(axis=0).round(1)}  "
            f"centre depth {self.depth[h // 2, w // 2]:.2f} m"
        )


def main():
    rclpy.init()
    node = RgbdListener()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
