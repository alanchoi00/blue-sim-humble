from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.conditions import LaunchConfigurationEquals
from launch.launch_description_sources import (
    AnyLaunchDescriptionSource,
    PythonLaunchDescriptionSource,
)
from launch.substitutions import (
    Command,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.substitutions import FindPackageShare


CONTROLLER_DELAY = 30.0
TELEOP_DELAY = CONTROLLER_DELAY + 10.0


def generate_launch_description():
    use_sim = LaunchConfiguration("use_sim")
    use_rviz = LaunchConfiguration("use_rviz")

    declare_model = DeclareLaunchArgument(
        "model",
        default_value="bluerov2_heavy",
        choices=["bluerov2", "bluerov2_heavy"],
        description="BlueROV2 model variant (bluerov2 or bluerov2_heavy)",
    )
    declare_use_sim = DeclareLaunchArgument(
        "use_sim",
        default_value="true",
        description="Launch Gazebo + ArduSub SITL",
    )
    declare_use_rviz = DeclareLaunchArgument(
        "use_rviz",
        default_value="false",
        description="Open RViz",
    )
    declare_use_joy = DeclareLaunchArgument(
        "use_teleop_joy",
        default_value="false",
        description="Use joystick for teleoperation",
    )
    declare_use_key = DeclareLaunchArgument(
        "use_key",
        default_value="false",
        description="Use keyboard for teleoperation",
    )
    declare_gazebo_world_file = DeclareLaunchArgument(
        "gazebo_world_file",
        default_value=PathJoinSubstitution([
            FindPackageShare("blue_description"),
            "gazebo/worlds/underwater.world",
        ]),
        description="Path to Gazebo world file",
    )

    robot_description_heavy = Command([
        "xacro ",
        PathJoinSubstitution([
            FindPackageShare("blue_control"),
            "description/urdf/bluerov2_heavy.config.xacro",
        ]),
        " use_sim:=",
        use_sim,
    ])

    robot_description_standard = Command([
        "xacro ",
        PathJoinSubstitution([
            FindPackageShare("blue_control"),
            "description/urdf/bluerov2.config.xacro",
        ]),
        " use_sim:=",
        use_sim,
    ])

    bringup_heavy = IncludeLaunchDescription(
        AnyLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("blue_bringup"),
                "launch/bluerov2_heavy/bluerov2_heavy.launch.yaml",
            ])
        ),
        launch_arguments={
            "use_sim": use_sim,
            "use_rviz": use_rviz,
            "robot_description": robot_description_heavy,
            "gazebo_world_file": LaunchConfiguration("gazebo_world_file"),
        }.items(),
        condition=LaunchConfigurationEquals("model", "bluerov2_heavy"),
    )

    bringup_standard = IncludeLaunchDescription(
        AnyLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("blue_bringup"),
                "launch/bluerov2/bluerov2.launch.yaml",
            ])
        ),
        launch_arguments={
            "use_sim": use_sim,
            "use_rviz": use_rviz,
            "robot_description": robot_description_standard,
            "gazebo_world_file": LaunchConfiguration("gazebo_world_file"),
        }.items(),
        condition=LaunchConfigurationEquals("model", "bluerov2"),
    )

    controllers_heavy = TimerAction(
        period=CONTROLLER_DELAY,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution([
                        FindPackageShare("blue_control"),
                        "launch/controllers_heavy.launch.py",
                    ])
                ),
                condition=LaunchConfigurationEquals("model", "bluerov2_heavy"),
            ),
        ],
    )

    controllers_standard = TimerAction(
        period=CONTROLLER_DELAY,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution([
                        FindPackageShare("blue_control"),
                        "launch/controllers.launch.py",
                    ])
                ),
                condition=LaunchConfigurationEquals("model", "bluerov2"),
            ),
        ],
    )

    teleop_keyboard = TimerAction(
        period=TELEOP_DELAY,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution([
                        FindPackageShare("blue_teleop"),
                        "launch/keyboard.launch.py",
                    ])
                ),
                condition=LaunchConfigurationEquals("use_key", "true"),
            ),
        ],
    )

    teleop_joystick = TimerAction(
        period=TELEOP_DELAY,
        actions=[
            IncludeLaunchDescription(
                AnyLaunchDescriptionSource(
                    PathJoinSubstitution([
                        FindPackageShare("blue_teleop"),
                        "launch/joystick.launch.yaml",
                    ])
                ),
                condition=LaunchConfigurationEquals("use_teleop_joy", "true"),
            ),
        ],
    )

    return LaunchDescription([
        declare_model,
        declare_use_sim,
        declare_use_rviz,
        declare_use_key,
        declare_use_joy,
        declare_gazebo_world_file,
        bringup_heavy,
        bringup_standard,
        controllers_heavy,
        controllers_standard,
        teleop_keyboard,
        teleop_joystick,
    ])
