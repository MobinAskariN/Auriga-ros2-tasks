#!/bin/bash

REMOTE_USER="user"              # second machine user
REMOTE_HOST="192.168.1.102"     # second machine IP


# 1. starting python node(the server)
echo "Starting Python server node on $REMOTE_HOST..."
ssh $REMOTE_USER@$REMOTE_HOST "
    source /opt/ros/humble/setup.bash &&
    source ~/ros2_ws/install/setup.bash &&
    ros2 run py_package python_node_socket
" &
sleep 2  # sleep for 2 seconds until server is up

# 2. starting cpp node(the client)
echo "Starting C++ client node locally..."
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run cpp_package cpp_node_socket

