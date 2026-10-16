#!/usr/bin/env python3

import rclpy
import math
from rclpy.node import Node
from std_msgs.msg import Bool
from nav_msgs.msg import Odometry
from turtlebot_patrol_interfaces.msg import obstacle_status
from geometry_msgs.msg import Twist

class Controller(Node):
    def __init__(self):
        super().__init__('patrol_controller')
        
        ## subscribers
        self.subscription_1 = self.create_subscription(
            obstacle_status,
            "/obstacle_status",
            self.obstacle_data,
            10)
        self.subscription_1  # prevent unused variable warning
        
        self.subscription_2 = self.create_subscription(
            Odometry,
            "/odom",
            self.odom_data,
            10)
        self.subscription_2  # prevent unused variable warning
        
        self.subscription_3 = self.create_subscription(
            Bool,
            "/esop_state",
            self.stop_data,
            10)
        self.subscription_1  # prevent unused variable warning
        
        
        
        
        ## publisher to obstacle status
        self.pub= self.create_publisher(
            Twist, 
            '/cmd_vel', 
            10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.MovementLogic)
        
        
        ## patrol route
        self.patrol_route= [10,10,10,10] # rectangular patrol path with specified distances
        self.patrol_angle = (math.pi/2)
        self.patrol_current = 0
        
        ## speed
        self.linearspeed = 0.5:
        self.angularspeed = 0.174 
        
        ## course correction
        self.linear_steps = 0 
        self.front_minimumdistanceofaction = 5.0
        self.old_left_distance = 0
        self.old_right_distance = 0
        
         
        
        
    ## getting information from the subscriptions
    def obstacle_data(self , msg):
        self.front_scan = msg.front_scan
        self.right_scan = msg.right_scan
        self.left_scan = msg.left_scan
        self.obstacle_detected = msg.obstacle_detected
    
    def odom_data(self , msg):
        self.odom_header = msg.header
        self.odom_child_frame = msg.child_frame_id
        self.odom_pose = msg.pose
        self.odom_twist = msg.twist
    
    def stop_data(self , msg):
        self.trigger_stop = msg.data

    
    ##main controller
    
    def MovementLogic(self): ##ignore this spaghetti mess of if loops
        twist = Twist()
        if not self.trigger_stop:  ## checks if emergency stop is implemented
            if not obstacle_detected:  ##checks if any object is close
                    
                if self.patrol_route[self.patrol_current]/self.linearspeed > # goes straight self.linear_steps:
                    twist.linear.x = self.linearspeed
                    self.linear_steps += 1
                    
                else:  #rotates
                    twist.linear.x = 0.0 
                    twist.angular.z = self.patrol_angle
                    self.linear_steps = 0
                    
            else:  ## obstacle detected
                if min(self.front_scan) <= 0.5: #object at front
                    twist.linear.x = 0.0
                    twist.angular.z = copysign(self.angularspeed , (self.left_scan + self.front_scan[30::]) - sum(self.right_scan + self.front_scan[:30:] ) #rotates towards the clearer side
                    
                else: #object closer to the side
                    if min(self.left_scan) <= 0.5
                        if self.old_left_distance == 0:
                            self.old_left_distance = min(self.left_scan)
                        if min(self.left_scan) < self.old_left_distance:
                            twist.angular_z = -self.angularspeed
                            self.old_left_distance = min(self.left_scan)
                    else:
                        if self.old_right_distance == 0:
                            self.old_right_distance = min(self.right_scan)
                        if min(self.right_scan) < self.old_right_distance:
                            twist.angular_z = self.angularspeed
                            self.old_side_distance = min(self.right_scan) 
              
        else:
            twist.linear.x = 0.0
            twist.angular.z = 0.0
        
        
        self.pub.publish(twist)



def main(args=None):
    rclpy.init(args=args)
    node = Controller()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

