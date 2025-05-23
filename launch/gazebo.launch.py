from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
import os
import xacro
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    pkg_path = get_package_share_directory('gazebo_visualization')
    urdf_file = os.path.join(pkg_path, 'urdf', 'robot.urdf')

    # Set the URDF as a launch configuration so it can be passed to nodes
    robot_description = Command(['xacro ', urdf_file])

    doc = xacro.parse(open(urdf_file))
    xacro.process_doc(doc)
    params={'robot_description':doc.toxml()}

    robot_state_publisher = Node(
    package='robot_state_publisher',
    executable='robot_state_publisher',
    output='screen',
    parameters=[params]
    )
    
    # Launch Gazebo and spawn the robot
    gazebo = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
        [os.path.join(get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py'])
    )

    # Spawn the robot in Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', '/robot_description', '-entity', 'robot'],
        output='screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument(name='headless', default_value='true', description='Set to "false" to run headless.'),
        gazebo,
        robot_state_publisher,
        spawn_entity,
    ])
