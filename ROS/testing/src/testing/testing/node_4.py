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
        self.linear_speed_long = 5.5
        self.linear_speed_half_short = 1.3
        
        
        self.angular_speed = 1.0 #initial angular speed
        
        
        #initialization 
        self.switch_case = "oval" 
        self.orientation = "half_short"
        self.line_status = "rotation_circle"
        self.orientation_count = 0
        self.line_status_count = 0
        
        self.elapsed = 0.0
        self.dt = 0.1

        # constants 
        self.duration_half_line = 2.0 #determines how long the line is
        self.duration_half_short = 1.3
        self.duration_long = 0.6
        self.duration_rotation_short = 0.9
        self.duration_rotation_direction_1 = 1.4
        self.duration_rotation_direction_2 = math.pi

        self.timer = self.create_timer(self.dt, self.move)
        
        
    def move(self):
        twist = Twist()

        match self.switch_case:
            case "oval":         # drawing the spiral
                
                match self.orientation_count:
                    case 1:
                        self.orientation = "long"
                    case 2:
                        self.orientation = "half_short"
                    case 3:
                        self.orientation = "half_short"
                    case 4:
                        self.orientation = "long"
                    case 5:
                        self.orientation = "half_short"
                    case 6:
                        self.orientation = "stop"
                        self.switch_case = "line"
                
                match self.orientation:
                    case "long":
                        if self.elapsed < self.duration_long:
                            twist.linear.x = self.linear_speed_long
                            twist.angular.z = self.angular_speed
                            self.elapsed += self.dt
                        else:
                            twist.linear.x = 0.0
                            twist.angular.z = 0.0
                            self.get_logger().info("long complete")
                            self.orientation_count += 1
                            self.elapsed = 0
                    
                    case "half_short":
                        if self.elapsed < self.duration_half_short:
                            twist.linear.x = self.linear_speed_half_short
                            twist.angular.z = self.angular_speed
                            self.elapsed += self.dt
                        else:
                            twist.linear.x = 0.0
                            twist.angular.z = 0.0
                            self.get_logger().info("half_short complete")
                            self.orientation_count += 1
                            self.elapsed = 0
                    
                    case "stop":
                        pass
            
            case "line":                         #drawing of line
                match self.line_status_count:
                    case 1:
                        self.line_status = "rotation_direction_1"
                    case 2:
                        self.line_status = "half_line"
                    case 3:
                        self.line_status = "rotation_direction_2"
                    case 4:
                        self.line_status = "half_line"
                    case 5:
                        self.line_status = "half_line"
                    case 6:
                        self.line_status = "stop"
                
                match self.line_status:
                    case "half_line":
                        if self.elapsed < self.duration_half_line: 
                            twist.linear.x = self.linear_speed 
                            self.elapsed += self.dt
                        else:
                            twist.linear.x = 0.0
                            self.get_logger().info("Line complete!")
                            self.line_status_count += 1
                            self.elapsed = 0
                    
                    case "rotation_circle":
                        if self.elapsed < self.duration_rotation_short:
                            twist.linear.x = self.linear_speed_half_short
                            twist.angular.z = self.angular_speed
                            self.elapsed += self.dt
                        else:
                            twist.linear.x = 0.0
                            twist.angular.z = 0.0
                            self.get_logger().info("rotation_circle complete")
                            self.line_status_count += 1
                            self.elapsed = 0
                            
                    case "rotation_direction_1":
                        if self.elapsed < self.duration_rotation_direction_1: #overshoots due to program running on 0.1 secs
                            twist.angular.z = self.angular_speed
                            self.elapsed += self.dt
                        else:
                            twist.angular.z = 0.0
                            self.get_logger().info("rotation_direction_1 Complete!")
                            self.line_status_count += 1
                            self.elapsed = 0
                    
                    case "rotation_direction_2":
                        if self.elapsed < self.duration_rotation_direction_2: #overshoots due to program running on 0.1 secs
                            twist.angular.z = self.angular_speed
                            self.elapsed += self.dt
                        else:
                            twist.angular.z = 0.0
                            self.get_logger().info("rotation_direction_2 Complete!")
                            self.line_status_count += 1
                            self.elapsed = 0
                    
                    case "stop":
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

