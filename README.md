Dependencies:
    GZ transport

Build the tank drive plugin:

    cmake -S tank_plugin -B tank_plugin/build
    cmake --build tank_plugin/build

Run Gazebo with the plugin and model paths available:

    export GZ_SIM_SYSTEM_PLUGIN_PATH=$PWD/tank_plugin/build
    export GZ_SIM_RESOURCE_PATH=$PWD
    gz sim test_world.sdf

Send wheel speed commands:

    gz topic -t /tank_cmd -m gz.msgs.Vector2d -p 'x: 2.0, y: 2.0'
    
# VexGazeboSim
