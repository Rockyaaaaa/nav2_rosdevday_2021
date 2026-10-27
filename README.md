# nav2_rosdevday_2021

This project contains a step-by-step tutorial for basic Nav2 features using a Jupyter Notebook and a warehouse simulation. It was originally created for the [2021 ROS Developers Day](https://www.theconstructsim.com/ros-developers-day-2021/) talk by [Steve Macenski](https://www.linkedin.com/in/steve-macenski-41a985101/).

It includes:

- A Jupyter Notebook covering a Nav2 walkthrough
- An AWS small warehouse Gazebo simulation
- A Neobotix industrial robot simulation
- Keepout and speed-restricted zone examples
- Python examples using Nav2 as a library

## Compatibility

This fork has been tested successfully on:

- Ubuntu 22.04
- ROS 2 Humble
- Gazebo Classic 11

The original project targeted ROS 2 Galactic. This fork updates the dependency branches and selected parameters for ROS 2 Humble.

## Setup

Install ROS 2 Humble and Gazebo Classic 11 first. Then create a workspace and clone this repository together with its source dependencies as sibling packages:

```bash
mkdir -p ~/colcon_ws/src
cd ~/colcon_ws/src

git clone https://github.com/Rockyaaaaa/nav2_rosdevday_2021.git

git clone --branch humble https://github.com/neobotix/neo_simulation2.git
git clone --branch humble https://github.com/neobotix/neo_nav2_bringup.git
git clone --branch ros2 https://github.com/aws-robotics/aws-robomaker-small-warehouse-world.git
```

Install ROS dependencies and build the workspace:

```bash
cd ~/colcon_ws
source /opt/ros/humble/setup.bash
rosdep update
rosdep install --from-paths src --ignore-src --rosdistro humble -r -y
colcon build --symlink-install
```

`--symlink-install` is recommended for development because changes to Python, launch, and configuration files are reflected without copying them into the install space again.

## Run

After a successful build, source the workspace overlay. It loads ROS 2 Humble and the package environment hooks, including the warehouse model paths:

```bash
cd ~/colcon_ws
source install/setup.bash
ros2 launch nav2_rosdevday_2021 system_launch.py
```

The command starts the Gazebo warehouse simulation, RViz, Nav2, and the selected Neobotix robot. The default robot is `mpo_700`. Other supported values are `mpo_500`, `mp_400`, and `mp_500`.

Useful launch arguments include:

```bash
ros2 launch nav2_rosdevday_2021 system_launch.py \
  my_robot:=mp_400 \
  use_rviz:=True \
  headless:=False
```

To run one of the Python demos in another terminal:

```bash
cd ~/colcon_ws
source install/setup.bash
python3 src/nav2_rosdevday_2021/nav2_rosdevday_2021/scripts/nav_to_pose_demo.py
```

Available demos:

- `picking_demo.py`
- `security_demo.py`
- `inspection_demo.py`
- `nav_to_pose_demo.py`
- `nav_through_poses_demo.py`
- `waypoint_follower_demo.py`

The first three demonstrate application-level Nav2 workflows. The last three demonstrate the `robot_navigator.py` Nav2-as-a-library interface.

The original walkthrough is available in `main.ipynb` and can be opened with:

```bash
jupyter-notebook src/nav2_rosdevday_2021/main.ipynb
```

![](media/pose_set.png)
