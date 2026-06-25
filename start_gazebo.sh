#!/bin/bash

cd "$(dirname "$0")"

export GZ_SIM_RESOURCE_PATH="$PWD:$GZ_SIM_RESOURCE_PATH"
export GZ_SIM_SYSTEM_PLUGIN_PATH="$PWD/tank_plugin/build:$GZ_SIM_SYSTEM_PLUGIN_PATH"

/opt/homebrew/bin/gz sim -s test_world.sdf