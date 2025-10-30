import rclpy
from rclpy.node import Node
from interfaces.msg import ImageProcessor
from interfaces.msg import ControllOptions
from py_package.yekta_the_processor import calculation
from py_package.avis.avisengine import Car
import cv2
import time

autonomous_mode = True


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
        speed = 0
        steering = 0
        try:
            while True:
                car.getData()
                sensors = car.getSensors() 
                image = car.getImage()
                carSpeed = car.getSpeed()
                # car.setSpeed(10)


                # if image is not None and image.any():
                #    q cv2.imshow('frames', image)

                # get data from processor and publish it to the controller
                distance_in_moment, degree_in_moment, second_derivative, mean_k = calculation(image)

                if not autonomous_mode:
                    key = cv2.waitKey(50) & 0xFF        
                    if key == ord('w'):        # جلو
                        speed = min(speed + 10, 100)
                    elif key == ord('s'):      # عقب
                        speed = max(speed - 10, -100)
                    elif key == ord('a'):      # چپ
                        steering = max(steering - 5, -30)
                    elif key == ord('d'):      # راست
                        steering = min(steering + 5, 30)
                    elif key == ord(' '):      # اسپیس = توقف
                        speed = 0
                        steering = 0
                    elif key == ord('q'):      # خروج
                        break

                    # اعمال تنظیمات
                    car.setSpeed(speed)
                    car.setSteering(steering)


                    # if cv2.waitKey(10) == ord('q'):
                    #     break
                
                else:
                    process_data = ImageProcessor()
                    process_data.heading_error = degree_in_moment
                    process_data.distance = distance_in_moment
                    process_data.second_derivation = second_derivative
                    process_data.mean_k = mean_k

                    self.publisher_.publish(process_data)

        finally:
            car.stop()



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
