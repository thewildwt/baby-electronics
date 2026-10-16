#!/usr/bin/env python3

import rclpy
import math
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from turtlebot_patrol_interfaces.msg import obstacle_status

class LiDAR(Node):
    def __init__(self):
        super().__init__('lidar_obstacle_detector')
        
        ## subscriber to scan
        self.subscription = self.create_subscription(
            LaserScan,
            "/scan",
            self.laser_scan_process,
            10)
        self.subscription  # prevent unused variable warning
        
        ## publisher to obstacle status
        self.pub= self.create_publisher(
            obstacle_status, 
            '/obstacle_status', 
            10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.status_publishing)
        
    
    def laser_scan_progress(self , msg):
        laser_orignal_range = msg.ranges
        laser_range = []
        
        for i in laser_orignal_range: ## to get rid of inf values
            if math.isnan(i):
                laser_range.append(8.0)  ## setting default distance for infinity values
            else:
                laser_range.append(i)
      
        self.laser_front = laser_range[30:-1:-1] + laser_range[359:330:-1]
        self.laser_right = laser_range[90:30:-1]
        self.laser_front = laser_range[330:270:-1]
        
        if(min(laser_front + laser_right + laser_left) <= 0.5):
            self.laser_obstacle = True
        else
            self.laser_obstacle = False
        
        front_min = min(laser_front)
        right_min = min(laser_right)
        left_min = min(laser_left)
        
        
    def status_publishing(self):
        status = obstacle_status()
        status.front_scan = self.laser_front
        status.right_scan = self.laser_right
        status.left_scan = self.laser_left
        status.obstacle_detected = self.laser_obstacle
        self.pub.publish(status)
        


def main(args=None):
    rclpy.init(args=args)
    node = LiDAR()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
