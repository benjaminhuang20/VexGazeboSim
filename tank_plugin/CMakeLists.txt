cmake_minimum_required(VERSION 3.16)

if(APPLE AND NOT CMAKE_OSX_ARCHITECTURES)
  set(CMAKE_OSX_ARCHITECTURES arm64 CACHE STRING "Build architecture" FORCE)
endif()

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(APPLE AND CMAKE_OSX_ARCHITECTURES STREQUAL "arm64")
  list(PREPEND CMAKE_PREFIX_PATH /opt/homebrew)
  list(APPEND CMAKE_IGNORE_PREFIX_PATH /usr/local)
endif()

project(TankDrivePlugin LANGUAGES CXX)

find_package(gz-cmake3 REQUIRED)
find_package(gz-plugin2 REQUIRED COMPONENTS register)
set(CPPZMQ_HEADER_PATH /usr/local/include)
find_package(CPPZMQ MODULE REQUIRED)
find_package(gz-transport13 REQUIRED)
find_package(gz-msgs10 REQUIRED)
find_package(gz-common5 REQUIRED)
find_package(sdformat14 REQUIRED)

find_path(GZ_SIM_INCLUDE_DIR
  NAMES gz/sim/System.hh
  PATH_SUFFIXES gz/sim8
  REQUIRED
)

find_library(GZ_SIM_LIBRARY
  NAMES gz-sim8
  REQUIRED
)

add_library(TankDrivePlugin SHARED TankDrivePlugin.cc)

target_compile_features(TankDrivePlugin PRIVATE cxx_std_17)

target_compile_options(TankDrivePlugin
  PRIVATE
    -I/opt/homebrew/Cellar/protobuf/35.1/include
)

target_include_directories(TankDrivePlugin
  BEFORE PRIVATE
    /opt/homebrew/include
    ${GZ_SIM_INCLUDE_DIR}
)

target_link_libraries(TankDrivePlugin
  PRIVATE
    ${GZ_SIM_LIBRARY}
    gz-plugin2::register
    gz-transport13::core
    gz-msgs10::core
    gz-common5::core
    sdformat14::sdformat14
)
