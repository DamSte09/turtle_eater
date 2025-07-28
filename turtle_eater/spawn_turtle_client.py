#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
import numpy as np
from functools import partial

class SpawnTurtleClientNode(Node):
    def __init__(self):
        super().__init__("spawn_turtle_client")

        self.spawn_turtle_client_ = self.create_client(Spawn, "spawn")

        self.timer_ = self.create_timer(2.0, self.spawn_turtle_delay)
        
    def spawn_turtle_delay(self):
        self.call_spawn_turtle(np.random.uniform(0, 10), np.random.uniform(0, 10), 0.0)

    def call_spawn_turtle(self, x, y, theta):
        while not self.spawn_turtle_client_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for the server...")
        
        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = theta

        future = self.spawn_turtle_client_.call_async(request)
        future.add_done_callback(partial(self.callback_call_spawn_turtle, request = request))

    def callback_call_spawn_turtle(self, future, request):
        response = future.result()
        self.get_logger().info("Spawned " + str(response.name))
        


        
def main(args=None):
    rclpy.init(args=args)
    node = SpawnTurtleClientNode()
    rclpy.spin(node) #keeping node alive
    rclpy.shutdown()

if __name__== "__main__":
    main()