#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class DrawCircle(Node):
    def __init__(self):
        super().__init__('draw_circle')
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10) 

        self.linear_speed = 2.5  #initial linear speed
        self.angular_speed = 1.0 #initial angular speed
        self.rotations = 0   #to count number of revolutions

        # time to complete one full circle: (2*pi) / angular_speed
        self.duration_circle = (2 * math.pi) / self.angular_speed
        self.elapsed = 0.0
        self.dt = 0.1

        # time to complete line 
        self.duration_line = 5 #determines how long the line is

        self.timer = self.create_timer(self.dt, self.move)
        
        
    def move(self):
        twist = Twist()

        if self.rotations < 6 :         # drawing the 6 circles
            
            if self.elapsed < self.duration_circle:
                twist.linear.x = self.linear_speed
                twist.angular.z = self.angular_speed
                self.elapsed += self.dt
            else:
                twist.linear.x = 0.0
                twist.angular.z = 0.0
                self.get_logger().info("Circle complete!")
                self.rotations += 1
                self.elapsed = 0
                self.linear_speed -= 0.3 
            
        elif self.rotations < 7:   #rotation of turtle - no linear velocity
            
            if self.elapsed < self.duration_circle * 3.0/4.0 : #overshoots due to program running on 0.1 secs
                twist.angular.z = self.angular_speed
                self.elapsed += self.dt
            else:
                twist.angular.z = 0.0
                self.get_logger().info("Rotation Complete!")
                self.rotations += 1
                self.elapsed = 0
        else:                          #drawing of line - no angular component

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

