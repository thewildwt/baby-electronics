#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class DrawCircle(Node):
    def __init__(self):
        super().__init__('draw_circle')
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10) 

        self.linear_speed = 0.5  #initial linear speed
        self.angular_speed = 1.0 #initial angular speed
        self.switch_case = "spiral"  #for checking what part of code to execute

        # time to complete the spiral
        self.duration_circle = 4 * (2 * math.pi) / self.angular_speed
        self.elapsed = 0.0
        self.dt = 0.1

        # time to complete line 
        self.duration_line = 2 #determines how long the line is
        
        # speed by which to increase the circle
        self.linear_increase_constant = 0.15
        self.linear_increase = self.linear_increase_constant/self.duration_circle

        self.timer = self.create_timer(self.dt, self.move)
        
        
    def move(self):
        twist = Twist()

        match self.switch_case:
            case "spiral":         # drawing the spiral
                
                if self.elapsed < self.duration_circle:
                    twist.linear.x = self.linear_speed
                    self.linear_speed += self.linear_increase
                    twist.angular.z = self.angular_speed
                    self.elapsed += self.dt
                else:
                    twist.linear.x = 0.0
                    twist.angular.z = 0.0
                    self.get_logger().info("Spiral complete!")
                    self.switch_case = "rotation"
                    self.elapsed = 0

            case "rotation":   #rotation of turtle - no linear velocity
                
                if self.elapsed < self.duration_circle/4.0 * 3.0/4.0 : #overshoots due to program running on 0.1 secs
                    twist.angular.z = self.angular_speed
                    self.elapsed += self.dt
                else:
                    twist.angular.z = 0.0
                    self.get_logger().info("Rotation Complete!")
                    self.switch_case = "line"
                    self.elapsed = 0                
            case "line":                         #drawing of line

                if self.elapsed < self.duration_line: 
                    twist.linear.x = self.linear_speed 
                    self.elapsed += self.dt
                else:
                    twist.linear.x = 0.0
                    self.get_logger().info("Line complete!")
                    self.timer.cancel()  # cancels timer

        self.cmd_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = DrawCircle()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main() 

