import rclpy
from rclpy.node import Node
from interfaces.msg import Num

class PyNode(Node):
    def __init__(self):
        super().__init__('py_node')
        self.subscription = self.create_subscription(
            Num,
            'num_topic',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(Num, 'num_topic_py', 10)
        self.current_num = None

    def listener_callback(self, msg):
        self.current_num = msg.num
        self.get_logger().info(f'Received: {self.current_num}')
        if self.current_num < 1:
            self.get_logger().error(f'Error: received non-positive number ({self.current_num}). Stopping.')
            rclpy.shutdown()
            return
        if self.current_num == 1:
            self.get_logger().info('Reached 1. Stopping.')
            rclpy.shutdown()
            return
        # If even, divide by 2 until odd
        while self.current_num % 2 == 0 and self.current_num != 1:
            self.current_num //= 2
            if self.current_num < 1:
                self.get_logger().error(f'Error: number became non-positive ({self.current_num}) during even processing. Stopping.')
                rclpy.shutdown()
                return
        # If odd, send to cpp node
        out_msg = Num()
        out_msg.num = self.current_num
        self.get_logger().info(f'Publishing: {out_msg.num}')
        self.publisher.publish(out_msg)

def main(args=None):
    rclpy.init(args=args)
    node = PyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()