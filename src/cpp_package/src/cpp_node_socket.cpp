#include <rclcpp/rclcpp.hpp>
#include <cstdlib>
#include <ctime>
#include <unistd.h>
#include <arpa/inet.h>

class CppNode : public rclcpp::Node {
public:
    CppNode() : Node("cpp_node_socket") {}

    void run() {
        srand(time(NULL));
        int num = rand() % 1000000 + 1;

        int sock = socket(AF_INET, SOCK_STREAM, 0);
        sockaddr_in serv_addr{};
        serv_addr.sin_family = AF_INET;
        serv_addr.sin_port = htons(5000);
        inet_pton(AF_INET, "192.168.1.101", &serv_addr.sin_addr);  // Change to correct IP

        if (connect(sock, (sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
            RCLCPP_ERROR(this->get_logger(), "Connection failed");
            return;
        }

        while (true) {
            while (num % 2 == 1 && num != 1) {
                num = 3 * num + 1;
                RCLCPP_INFO(this->get_logger(), "Tripled to: %d", num);
            }

            std::string msg = std::to_string(num);
            send(sock, msg.c_str(), msg.size(), 0);

            if (num == 1) break;

            char buffer[1024] = {0};
            int valread = recv(sock, buffer, sizeof(buffer), 0);
            if (valread <= 0) break;
            num = std::stoi(buffer);
            RCLCPP_INFO(this->get_logger(), "Received: %d", num);
            if (num == 1) break;
        }

        close(sock);
    }
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<CppNode>();
    node->run();  // manual control, no spin
    rclcpp::shutdown();
    return 0;
}
