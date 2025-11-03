#include <memory>
#include <chrono>
#include <functional>
#include <string>
#include <iostream>
#include <cmath>
#include <queue>




#include "rclcpp/rclcpp.hpp"
#include "interfaces/msg/image_processor.hpp"
#include "interfaces/msg/controll_options.hpp"
using std::placeholders::_1;
using namespace std::chrono_literals;


class Controller : public rclcpp::Node
{
    public:

    //float k {0.22 + std::abs(mean_k)};
    //float k_ff {2.8 + std::abs(mean_k)};
    float k_h {1};
    float k_s {0.0001};
    float k {0.24 + (2.5) * std::abs(mean_k)};
    float k_ff {2.8 + (1.5) * std::abs(mean_k)};
    queue <flaot> K_mean_buffer 
    //flaot K_mean_buffer [5] = {};


    Controller()
    : Node("controller")
    {
        subscription_ = this->create_subscription<interfaces::msg::ImageProcessor>(
        "process_data", 10, std::bind(&Controller::get_data, this, _1));

        publisher_ = this->create_publisher<interfaces::msg::ControllOptions>("controll_data", 10);
        timer_ = this->create_wall_timer(
        20ms, std::bind(&Controller::publish_controll, this));
    }

    void calculate_steering_angle(){
        
        
        velocity = 100;
        
        //velocity = 100;
        steering_angle =  k_h * heading_error + atan((k * distance) / (car_velocity)) * (180 / 3.14) +  k_ff * atan(mean_k)  * (180 / 3.14);
        

    } 



    private:
    void get_data(const interfaces::msg::ImageProcessor &msg)
    {
        distance = msg.distance;
        heading_error = msg.heading_error;
        second_derivation = msg.second_derivation;
        mean_k = msg.mean_k;
        car_velocity = msg.velocity;
        // std::cout << distance << " " << heading_error << " " << mean_k << " " << car_velocity << std::endl;
    }

    void publish_controll()
    {
        auto message = interfaces::msg::ControllOptions();
        calculate_steering_angle();
        std::cout << distance << ",,,,," << atan(k * distance / (car_velocity + k_s)) << std::endl;
        message.speed = velocity;
        message.steering = steering_angle;
        publisher_->publish(message);
    }

    rclcpp::Subscription<interfaces::msg::ImageProcessor>::SharedPtr subscription_;
    rclcpp::Publisher<interfaces::msg::ControllOptions>::SharedPtr publisher_;
    double heading_error;
    double distance;
    double second_derivation;
    double mean_k;
    int car_velocity;

    int velocity {0};
    int steering_angle {0};

    rclcpp::TimerBase::SharedPtr timer_;

};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<Controller>());
    rclcpp::shutdown();
    return 0;
}
