import rclpy
from rclpy.node import Node
from interfaces.msg import ImageProcessor
from interfaces.msg import ControllOptions
from avis.avisengine import Car
import cv2
import time


class Processor(Node):
    def __init__(self):
        super().__init__('runner')
        self.car = Car()
        self.car.connect(server="127.0.0.1", port=25001)
        self.publisher_ = self.create_publisher(ImageProcessor, 'process_data', 10)

        self.subscription = self.create_subscription(
            ControllOptions,
            'controll_data',
            self.controll,
            10)


    def process_image(self):
        car = self.car
        while True:
            car.getData()
            sensors = car.getSensors() 
            image = car.getImage()
            carSpeed = car.getSpeed()


            if image is not None and image.any():
                cv2.imshow('frames', image)

            # get data from processor and publish it to the controller


    def controll(self, msg:ControllOptions):
        # self.get_logger().info('I heard: "%s"' % msg.data)
        self.car.setSpeed(msg.speed)
        self.car.setSteering(msg.steering)





def main(args=None):
    rclpy.init(args=args)
    node = Processor()
    node.process_image()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
