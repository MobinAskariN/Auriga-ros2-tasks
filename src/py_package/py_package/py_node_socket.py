# py_node_no_spin.py
import rclpy
from rclpy.node import Node
import socket

class PythonNode(Node):
    def __init__(self):
        super().__init__('python_node_socket')

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', 5000))
        s.listen(1)
        self.get_logger().info("Waiting for connection...")
        conn, addr = s.accept()
        self.get_logger().info(f"Connected by {addr}")

        while True:
            data = conn.recv(1024)
            if not data:
                break
            num = int(data.decode())
            self.get_logger().info(f"Received: {num}")
            while num % 2 == 0 and num != 1:
                num //= 2
                self.get_logger().info(f"Divided to: {num}")
            conn.sendall(str(num).encode())
            if num == 1:
                break

        conn.close()
        s.close()

def main(args=None):
    rclpy.init(args=args)
    node = PythonNode()
    node.run()
    node.destroy_node()
    rclpy.shutdown()
