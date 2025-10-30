#include <memory>
#include <chrono>
#include <functional>
#include <string>
#include <iostream>


#include "rclcpp/rclcpp.hpp"
#include "interfaces/msg/image_processor.hpp"
#include "interfaces/msg/controll_options.hpp"
using std::placeholders::_1;
using namespace std::chrono_literals;


class Controller : public rclcpp::Node
{
    public:
    Controller()
    : Node("controller")
    {
        subscription_ = this->create_subscription<interfaces::msg::ImageProcessor>(
        "process_data", 10, std::bind(&Controller::get_data, this, _1));

        publisher_ = this->create_publisher<interfaces::msg::ControllOptions>("controll_data", 10);
        timer_ = this->create_wall_timer(
        500ms, std::bind(&Controller::publish_controll, this));
    }


    private:
    void get_data(const interfaces::msg::ImageProcessor &msg)
    {
        distance = msg.distance;
        heading_error = msg.heading_error;
        second_derivation = msg.second_derivation;
        std::cout << distance << std::endl;
    }

    void publish_controll()
    {
        auto message = interfaces::msg::ControllOptions();
        message.speed = 0;
        message.steering = 0;
    //   publisher_->publish(message);
    }

    rclcpp::Subscription<interfaces::msg::ImageProcessor>::SharedPtr subscription_;
    rclcpp::Publisher<interfaces::msg::ControllOptions>::SharedPtr publisher_;
    double heading_error;
    double distance;
    double second_derivation;

    rclcpp::TimerBase::SharedPtr timer_;

};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<Controller>());
    rclcpp::shutdown();
    return 0;
}
