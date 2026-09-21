from glob import glob

from setuptools import setup

package_name = "gz_sensor_lab"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", glob("launch/*.launch.py")),
        ("share/" + package_name + "/worlds", glob("worlds/*.sdf")),
        ("share/" + package_name + "/config", glob("config/*.yaml")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Daryna Datsenko",
    maintainer_email="daryna.datsenko@gmail.com",
    description="Lab 0.1: a sensor in a simple Gazebo world, its data in ROS 2.",
    license="MIT",
    entry_points={
        "console_scripts": [
            "rgbd_listener = gz_sensor_lab.rgbd_listener:main",
            "pressure_listener = gz_sensor_lab.pressure_listener:main",
        ],
    },
)
