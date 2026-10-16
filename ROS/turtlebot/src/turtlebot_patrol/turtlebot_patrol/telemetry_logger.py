#!/usr/bin/env python3

import rclpy
import csv
import math
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist


class Telemetry(Node):
    def __init__(self):
        super().__init__('telemetry_logger')
        
        ## subscriptions
        self.subscription_1 = self.create_subscription(
            Odometry,
            "/odom",
            self.odom_data,
            10)
        self.subscription_1  # prevent unused variable warning
        
        self.subscription_2 = self.create_subscription(
            Twist,
            "/cmd_vel",
            self.velocity_data,
            10)
        self.subscription_2  # prevent unused variable warning
        
        self.currentrow_CVS = [] # for writing the csv file
        
        self.battery = 100
        self.serial=0
        
        self.distance = 0
        self.time_motion =0
        self.time_total = 0
        self.tempmotiontimestart = 0
        self.tempmotiontimeend = 0
        self.tempstoptimestart = 0
        self.tempstoptimeend = 0
        
    def odom_data(self ,msg):
        odom_pose = msg.pose
        self.displacement = math.sqrt(odom_pose.position.x**2 + odom_pose.position.y**2 )
        self.get_logger().info('Distance travelled: "%d"' % self.displacement)
    
    
    def velocity_data(self,msg): 
        self.linear_speed = msg.Twist.linear
        self.angular_speed = msg.Twist.angular
        
        self.get_logger().info('Linear speed- x:"%d" , y:"%d" ,z:"%d"' % self.linear_speed.x , self.linear_speed.y , self.linear_speed.z) 
        self.get_logger().info('Angular speed- x:"%d" , y:"%d" ,z:"%d"' % self.angular_speed.x , self.angular_speed.y , self.angular_speed.z)
        
        self.calculations()
        
    
        
    
    def calculations(self):
        self.time = self.get_clock().now()
        
        #time calculation
        if self.linear_speed.x != 0:
            if self.tempmotiontimestart = 0:
                self.tempmotiontimestart=self.time
            if self.tempstoptimestart != 0:
                self.tempstoptimeend = self.time
                self.time_total += self.timestoptimeend - self.timestoptimestart
                self.timestoptimestart = 0
        else:
            if self.tempstoptimestart = 0:
                self.tempmotiontimestart=self.time
            if self.tempmotiontimestart != 0:
                self.tempmotiontimeend = self.time
                timeelapsed = self.timemotiontimeend - self.timemotiontimestart
                self.time_motion += timeelapsed
                self.time_total += timeelapsed
                self.timemotiontimestart = 0
                
        #average speed
        self.average_speed = self.linear_speed.x*self.time_motion/self.time_total 

        # battery drain
        self.battery = 100 - self.time_motion/10
        
        #csv writer file
        self.serial += 1
        data = [self.serial , self.time_total , self.displacement , self.battery , self.average_speed]
        self.writer_CVS.writerows(data)

        
        
    #initializes the csv file and writes the header  
    def MakeCSV(self):
        header = ['S.no' , 'Time elapsed' , 'Total distance traveled' ,'Battery' , 'Linear Speed']
        with open('telemetry.csv' , 'w' , newline = '') as csvfile:
            self.writer_CVS = csv.writer(csvfile)
            self.writer_CVS.writerows(header)
        
def main(args=None):
    rclpy.init(args=args)
    node = Telemetry()
    node.MakeCSV()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

