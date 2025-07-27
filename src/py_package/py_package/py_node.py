import rclpy
from rclpy.node import Node
from interfaces.srv import NumSrv
import time


class PyNode(Node):
    def __init__(self):
        super().__init__('py_node')
        self.srv = self.create_service(NumSrv, 'num_srv', self.handle_num_srv)
        self.processing_done = False

    def handle_num_srv(self, request, response):
        current_num = request.num
        self.get_logger().info(f'Received: {current_num}')

        if current_num < 1:
            self.get_logger().error(f'Error: received non-positive number ({current_num}). Stopping.')
            response.result = current_num
            response.finished = True
            self.processing_done = True
            return response

        if current_num == 1:
            self.get_logger().info('Reached 1. Stopping.')
            response.result = 1
            response.finished = True
            self.processing_done = True
            return response

        # If even, divide by 2 until odd
        while current_num % 2 == 0:
            current_num //= 2
            if current_num < 1:
                self.get_logger().error(f'Error: number became non-positive ({current_num}) during even processing. Stopping.')
                response.result = current_num
                response.finished = True
                self.processing_done = True
                return response

        # Still odd and > 1 → send to C++ node
        response.result = current_num
        response.finished = False
        self.get_logger().info(f'Returning: {current_num}')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = PyNode()

    try:
        while rclpy.ok() and not node.processing_done:
            time.sleep(0.1)  # allow background threads to process service requests
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
