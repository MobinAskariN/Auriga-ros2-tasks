import os

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import TimerAction

def generate_launch_description():
    return LaunchDescription([
        # Launch controll.cpp node
        Node(
            
            package='py_package',
            executable='main',
            name='runner',
            output='screen',
            respawn=True

        ),
        TimerAction(
        # Launch vision.py node
            period=1.0,
            actions=[Node(
            package='cpp_package',       # replace with your package name
            executable='controller',     # name of compiled cpp executable
            name='controller',
            output='screen',
            respawn=True
            # optionally pass arguments
            # arguments=['--ros-args', '--log-level', 'info']
            )]
        ),
    ])