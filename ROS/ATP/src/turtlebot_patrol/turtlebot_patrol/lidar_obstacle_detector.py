#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, LaserScan
from std_msgs.msg import String

class LiDAR(Node):
    def __init__(self):
        super().__init__('lidar_obstacle_detector')
        self.subscription = self.create_subscription(
            LaserScan,
            "/scan",
            self.laser_scan_process,
            10)
        self.subscription  # prevent unused variable warning
    
    def laser_scan_progress(self):
        
        


def main(args=None):
    rclpy.init(args=args)
    node = LiDAR()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
