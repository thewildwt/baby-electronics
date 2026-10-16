from setuptools import find_packages, setup

package_name = 'turtlebot_patrol'

setup(
    name=package_name,
    version='0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    package_data={'': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='thewildwt',
    maintainer_email='cybervt2007@gmail.com',
    description='A modular ROS 2 software stack for a TurtleBot3 operating in a simulated Gazebo environment. The robot must autonomously patrol a predefined route, detect and avoid obstacles using LiDAR, respond to an emergency-stop service, and publish/log basic telemetry',
    license=':p',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'lidar_obstacle_detector = turtlebot_patrol.lidar_obstacle_detector:main',
            'emergency_stop_server = turtlebot_patrol.emergency_stop_server:main',
            'patrol_controller = turtlebot_patrol.patrol_controller:main',
            'telemetry_logger = turtlebot_patrol.telemetry_logger:main'
        ],
    },
)
