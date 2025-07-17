#include <rclcpp/rclcpp.hpp>
#include <interfaces/msg/num.hpp>
#include <random>

using std::placeholders::_1;

class CppNode : public rclcpp::Node {
public:
    CppNode() : Node("cpp_node") {
        publisher_ = this->create_publisher<interfaces::msg::Num>("num_topic", 10);
        subscription_ = this->create_subscription<interfaces::msg::Num>(
            "num_topic_py", 10, std::bind(&CppNode::topic_callback, this, _1));
        // Initialize random number
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<int64_t> dis(1, 1000000);
        current_num_ = dis(gen);
        RCLCPP_INFO(this->get_logger(), "Starting number: %ld", current_num_);
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(500),
            std::bind(&CppNode::process_number, this));
    }

private:
    void process_number() {
        if (current_num_ < 1) {
            RCLCPP_ERROR(this->get_logger(), "Error: number became non-positive (%ld). Stopping.", current_num_);
            rclcpp::shutdown();
            return;
        } else if (current_num_ == 1) {
            RCLCPP_INFO(this->get_logger(), "Reached 1. Stopping.");
            rclcpp::shutdown();
            return;
        }
        // Odd: triple and add 1 until even
        while (current_num_ % 2 != 0) {
            current_num_ = current_num_ * 3 + 1;
            if (current_num_ < 1) {
                RCLCPP_ERROR(this->get_logger(), "Error: number became non-positive (%ld) during odd processing. Stopping.", current_num_);
                rclcpp::shutdown();
                return;
            }
        }
        // Publish even number
        auto msg = interfaces::msg::Num();
        msg.num = current_num_;
        RCLCPP_INFO(this->get_logger(), "Publishing: %ld", msg.num);
        publisher_->publish(msg);
        timer_->cancel(); // Wait for Python node response
    }

    void topic_callback(const interfaces::msg::Num::SharedPtr msg) {
        current_num_ = msg->num;
        RCLCPP_INFO(this->get_logger(), "Received: %ld", current_num_);
        if (current_num_ < 1) {
            RCLCPP_ERROR(this->get_logger(), "Error: received non-positive number (%ld). Stopping.", current_num_);
            rclcpp::shutdown();
            return;
        }
        if (current_num_ == 1) {
            RCLCPP_INFO(this->get_logger(), "Python node reached 1. Stopping.");
            rclcpp::shutdown();
            return;
        }
        timer_->reset();
    }

    rclcpp::Publisher<interfaces::msg::Num>::SharedPtr publisher_;
    rclcpp::Subscription<interfaces::msg::Num>::SharedPtr subscription_;
    rclcpp::TimerBase::SharedPtr timer_;
    int64_t current_num_;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<CppNode>());
    rclcpp::shutdown();
    return 0;
}
