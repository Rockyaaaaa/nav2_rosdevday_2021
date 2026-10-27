# Copyright (c) 2021 Samsung Research America
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import xacro
from ament_index_python.packages import get_package_share_directory

from launch import LaunchContext, LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Get the launch directory
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    bringup_dir = get_package_share_directory('nav2_rosdevday_2021')
    robot_model_dir = get_package_share_directory('neo_simulation2')
    warehouse_dir = get_package_share_directory('aws_robomaker_small_warehouse_world')

    nav2_launch_dir = os.path.join(nav2_bringup_dir, 'launch')
    launch_dir = os.path.join(bringup_dir, 'launch')
    warehouse_launch_file = os.path.join(
        warehouse_dir, 'launch', 'small_warehouse.launch.py')
    rviz_config_file = os.path.join(nav2_bringup_dir, 'rviz', 'nav2_default_view.rviz')

    # Create the launch configuration variables
    slam = LaunchConfiguration('slam')
    map_yaml_file = LaunchConfiguration('map')
    use_sim_time = LaunchConfiguration('use_sim_time')
    params_file = LaunchConfiguration('params_file')

    # Launch configuration variables specific to simulation
    use_simulator = LaunchConfiguration('use_simulator')
    use_rviz = LaunchConfiguration('use_rviz')
    headless = LaunchConfiguration('headless')
    world = LaunchConfiguration('world')
    my_robot = LaunchConfiguration('my_robot')
    arm_type = LaunchConfiguration('arm_type')
    use_docking_adapter = LaunchConfiguration('use_docking_adapter')

    # Declare the launch arguments
    declare_slam_cmd = DeclareLaunchArgument(
        'slam',
        default_value='False',
        description='Whether run a SLAM')

    declare_map_yaml_cmd = DeclareLaunchArgument(
        'map',
        default_value=os.path.join(
            warehouse_dir, 'maps', '005', 'map.yaml'),
        description='Full path to map file to load')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true')

    declare_params_file_cmd = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(bringup_dir, 'params', 'basic_params.yaml'),
        description='Full path to the ROS2 parameters file to use for all launched nodes')

    declare_use_simulator_cmd = DeclareLaunchArgument(
        'use_simulator',
        default_value='True',
        description='Whether to start the simulator')

    declare_use_rviz_cmd = DeclareLaunchArgument(
        'use_rviz',
        default_value='True',
        description='Whether to start RVIZ')

    declare_simulator_cmd = DeclareLaunchArgument(
        'headless',
        default_value='False',
        description='Whether to execute gzclient for the simulation frontend')

    declare_world_cmd = DeclareLaunchArgument(
        'world',
        default_value=os.path.join(
            bringup_dir, 'worlds', 'industrial_sim.world'),
        description='Full path to world model file to load')

    declare_my_robot_cmd = DeclareLaunchArgument(
        'my_robot',
        default_value='mpo_700',
        description='Robot types: "mpo_700", "mpo_500", "mp_400", "mp_500"')

    declare_arm_type_cmd = DeclareLaunchArgument(
        'arm_type',
        default_value='',
        description='Arm type (mpo_700/mpo_500 only): ec66, cs66, ur5, ur10, ur5e, ur10e')

    declare_docking_adapter_cmd = DeclareLaunchArgument(
        'use_docking_adapter',
        default_value='False',
        description='Enable the docking adapter (mpo_700 only)')

    # Let the warehouse package start and configure Gazebo.
    warehouse_gazebo_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(warehouse_launch_file),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'headless': headless,
        }.items())

    rviz_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_launch_dir, 'rviz_launch.py')),
        condition=IfCondition(use_rviz),
        launch_arguments={'namespace': '',
                          'use_namespace': 'False',
                          'use_sim_time': use_sim_time,
                          'rviz_config': rviz_config_file}.items())

    bringup_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_launch_dir, 'bringup_launch.py')),
        launch_arguments={'slam': slam,
                          'map': map_yaml_file,
                          'use_sim_time': use_sim_time,
                          'params_file': params_file,
                          'autostart': 'True'}.items())

    # UNCOMMENT HERE FOR KEEPOUT DEMO
    # start_lifecycle_manager_cmd = Node(
    #         package='nav2_lifecycle_manager',
    #         executable='lifecycle_manager',
    #         name='lifecycle_manager_costmap_filters',
    #         output='screen',
    #         emulate_tty=True,
    #         parameters=[{'use_sim_time': use_sim_time},
    #                     {'autostart': True},
    #                     {'node_names': ['filter_mask_server', 'costmap_filter_info_server']}])

    # start_map_server_cmd = Node(
    #         package='nav2_map_server',
    #         executable='map_server',
    #         name='filter_mask_server',
    #         output='screen',
    #         emulate_tty=True,
    #         parameters=[params_file])

    # start_costmap_filter_info_server_cmd = Node(
    #         package='nav2_map_server',
    #         executable='costmap_filter_info_server',
    #         name='costmap_filter_info_server',
    #         output='screen',
    #         emulate_tty=True,
    #         parameters=[params_file])

    # Create the launch description and populate
    ld = LaunchDescription()

    # Declare the launch options
    ld.add_action(declare_slam_cmd)
    ld.add_action(declare_map_yaml_cmd)
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_params_file_cmd)
    ld.add_action(declare_use_simulator_cmd)
    ld.add_action(declare_use_rviz_cmd)
    ld.add_action(declare_simulator_cmd)
    ld.add_action(declare_world_cmd)
    ld.add_action(declare_my_robot_cmd)
    ld.add_action(declare_arm_type_cmd)
    ld.add_action(declare_docking_adapter_cmd)
    ld.add_action(warehouse_gazebo_cmd)
    ld.add_action(OpaqueFunction(
        function=launch_robot_setup,
        args=[my_robot, arm_type, use_docking_adapter, use_sim_time, robot_model_dir]))
    ld.add_action(rviz_cmd)
    ld.add_action(bringup_cmd)
    # UNCOMMENT HERE FOR KEEPOUT DEMO
    # ld.add_action(start_lifecycle_manager_cmd)
    # ld.add_action(start_map_server_cmd)
    # ld.add_action(start_costmap_filter_info_server_cmd)

    return ld


def launch_robot_setup(
        context: LaunchContext, my_robot_arg, arm_type_arg,
        docking_adapter_arg, use_sim_time_arg, robot_model_dir):
    """Expand the selected Neo Xacro and spawn that exact description in Gazebo."""
    robot_name = my_robot_arg.perform(context)
    arm_type = arm_type_arg.perform(context)
    use_docking_adapter = docking_adapter_arg.perform(context)
    use_sim_time = use_sim_time_arg.perform(context).lower() in ('true', '1')

    valid_robots = ('mpo_700', 'mpo_500', 'mp_400', 'mp_500')
    if robot_name not in valid_robots:
        raise RuntimeError(
            "Invalid my_robot={!r}; expected one of {}".format(
                robot_name, ', '.join(valid_robots)))

    if arm_type and robot_name not in ('mpo_700', 'mpo_500'):
        raise RuntimeError(
            '{} does not support arm_type={!r}'.format(robot_name, arm_type))

    # The adapter belongs only to MPO 700, matching neo_simulation2's launcher.
    if robot_name != 'mpo_700':
        use_docking_adapter = 'false'

    xacro_file = os.path.join(
        robot_model_dir, 'robots', robot_name, robot_name + '.urdf.xacro')
    robot_description = xacro.process_file(
        xacro_file,
        mappings={
            'use_gazebo': 'true',
            'arm_type': arm_type,
            'use_docking_adapter': use_docking_adapter,
        }).toxml()

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': robot_description,
        }])

    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', robot_name,
            '-topic', '/robot_description',
            '-x', '3.45', '-y', '2.15', '-z', '0.10', '-Y', '3.14',
        ],
        output='screen')

    return [robot_state_publisher, spawn_entity]
