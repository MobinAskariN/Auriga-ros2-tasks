from launch import LaunchDescription
from launch.actions import TimerAction
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='py_package',
            executable='py_node',
            name='py_node',
            output='screen',
        ),
        TimerAction(
            period=2.0,  # Wait 2 seconds before starting cpp_node
            actions=[
                Node(
                    package='cpp_package',
                    executable='cpp_node',
                    name='cpp_node',
                    output='screen',
                )
            ]
        )
    ])
