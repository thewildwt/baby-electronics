#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from std_srvs.srv import Trigger

class Emergency(Node):
    def __init__(self):
        super().__init__('emergency_stop_server')
        
        ## service call
        self.cli = self.create_client(Trigger, 'Trigger')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        
        req = Trigger.Request()
        future = self.cli.call_async(req)
        response = future.result()
        self.trigger_stop = response.success
        self.trigger_reason = response.message
        
        
        
        ## publisher to esop state
        self.pub= self.create_publisher(
            Bool, 
            '/estop_state', 
            10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.status_publishing)
        
    def status_publishing(self):
        status = Bool()
        status.data = self.trigger_stop
        if status.data:
            self.get_logger().info('Reason stopped: "%s"' % self.trigger_reason)
        self.pub.publish(status)
        



def main(args=None):
    rclpy.init(args=args)
    node = Emergency()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
