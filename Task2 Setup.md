# Collatz Distributed System

This document describes how to set up and run the distributed Collatz collaboration system across two machines (physical or virtual). Follow these steps carefully to build, configure, and execute the Python (server) and C++ (client) nodes communicating over sockets.

---

## Prerequisites

- **ROS 2** installed and sourced (e.g., Humble or later).
- **Colcon** build tool.
- Two machines (physical or one physical + one VirtualBox VM) on the **same Wi‑Fi** network.
- Python and C++ toolchains configured for your ROS 2 environment.

---

## 1. Clone, Build, and Source Your Workspace

First, clone the repository:

```bash
git clone https://github.com/MobinAskariN/Auriga-ros2-tasks.git
cd Auriga-ros2-tasks
```

Then build the workspace:

```bash
colcon build
```

Finally, source ROS 2 and workspace environments on **both machines**:

```bash
source /opt/ros/<distro>/setup.bash
source ~/Auriga-ros2-tasks/install/setup.bash
```

> Replace `<distro>` with your ROS 2 distribution name (e.g., `humble`).

1. Build the workspace:

```bash
cd ~/Auriga-ros2-tasks
colcon build
```

2. Source ROS 2 and workspace environments on **both machines**:

```bash
source /opt/ros/<distro>/setup.bash
source ~/Auriga-ros2-tasks/install/setup.bash
```

> Replace `<distro>` with your ROS 2 distribution name (e.g., `humble`).

---

## 2. Verify Network Connectivity

1. Ensure both machines are connected to the **same Wi‑Fi**.
2. On each machine, find its IP address:

```bash
hostname -I
```

3. Test connectivity by pinging the other machine’s IP:

```bash
ping <other-machine-IP>
```

---

## 3. (VirtualBox Only) Bridged Networking

If using a VirtualBox VM, configure Bridged Adapter:

1. Shut down the VM.
2. In VirtualBox Manager, select the VM → **Settings** → **Network**.
3. For **Adapter 1**:
   - **Enable Network Adapter**: 
   - **Attached to**: `Bridged Adapter`
   - **Name**: your host Wi‑Fi interface (e.g., `wlan0` or `enp3s0`).
4. Restart the VM and confirm it appears on the same network.

---

## 4. Open Firewall Port (Python Server)

On the machine running the Python server (e.g., VM):

```bash
sudo ufw allow 5000/tcp
```

---

## 5. Configure Server IP in C++ Client

Edit `socket_cpp_node.cpp` in the `cpp_package`:

```cpp
// Locate this line and replace with the server machine’s IP:
inet_pton(AF_INET, "192.168.X.X", &serv_addr.sin_addr);
```

Save and rebuild if you change this file:

```bash
colcon build --packages-select cpp_package
source install/setup.bash
```

---

## 6. Running the System

All commands should be executed in separate terminals :

1. **Python Server (on Machine 1)**

   ```bash
   ros2 run py_package socket_py_node
   ```

   You should see:

   ```text
   Waiting for connection...
   ```

2. **C++ Client (on Machine 2)**

   ```bash
   ros2 run cpp_package socket_cpp_node
   ```

   Expected output on client side:

   ```text
   Tripled to: ...
   Received: ...
   ```

   And on Python server:

   ```text
   Connected by ('192.168.1.5', ...)
   Received: ...
   ```

---

## 7. Troubleshooting

- **Ping fails:** Check Wi‑Fi connection and Bridged Adapter settings (if VM).
- **Firewall issues:** Ensure port 5000 is open on the server machine.
- **Code changes not applied:** Always rebuild and source the workspace after modifications.
- **Incorrect IP:** Double-check `hostname -I` output and update the client code.

---

Congratulations! Your two ROS 2 nodes should now communicate over sockets and collaborate to compute the Collatz sequence across machines.

---

## 8. Running Both Nodes with a Single Command (Multi‑Machine)

Because your Python node is the **server** (listening) and your C++ node is the **client** (connecting), we must start the server first.

You can automate both starts using SSH from the client machine:

Make start_collatz.sh executable:

```bash
chmod +x start_collatz.sh
```

Run it from the **client** machine:

```bash
./start_collatz.sh
```

> Ensure you have password‑less SSH set up between the client and server machines (`ssh-copy-id`).

---
