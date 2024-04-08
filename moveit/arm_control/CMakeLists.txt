cmake_minimum_required(VERSION 3.16)
project(arm_control LANGUAGES CXX)

if(CMAKE_CXX_COMPILER_ID MATCHES "(GNU|Clang)")
  add_compile_options(-Wall -Wextra)
endif()

# find dependencies
set(HW_IF_INCLUDE_DEPENDS
  pluginlib
  rcpputils
  hardware_interface
)
set(REF_GEN_INCLUDE_DEPENDS
  kdl_parser
  rclcpp
  trajectory_msgs
)
set(CONTROLLER_INCLUDE_DEPENDS
  pluginlib
  rcpputils
  controller_interface
  realtime_tools
  trajectory_msgs
)

# find dependencies
find_package(ament_cmake REQUIRED)
foreach(Dependency IN ITEMS ${HW_IF_INCLUDE_DEPENDS})
  find_package(${Dependency} REQUIRED)
endforeach()
foreach(Dependency IN ITEMS ${REF_GEN_INCLUDE_DEPENDS})
  find_package(${Dependency} REQUIRED)
endforeach()
foreach(Dependency IN ITEMS ${CONTROLLER_INCLUDE_DEPENDS})
  find_package(${Dependency} REQUIRED)
endforeach()


## COMPILE
add_executable(send_trajectory reference_generator/send_trajectory.cpp)

ament_target_dependencies(
  send_trajectory PUBLIC
  ${REF_GEN_INCLUDE_DEPENDS}
)

add_library(
  arm_control
  SHARED
  hardware/armbot_hardware.cpp
  controller/armbot_controller.cpp
)

target_compile_features(arm_control PUBLIC cxx_std_17)
target_include_directories(arm_control PUBLIC
$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/hardware/include>
$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/controller/include>
$<INSTALL_INTERFACE:include/arm_control>
)
ament_target_dependencies(
  arm_control PUBLIC
  ${HW_IF_INCLUDE_DEPENDS}
  ${CONTROLLER_INCLUDE_DEPENDS}
)

# Causes the visibility macros to use dllexport rather than dllimport,
# which is appropriate when building the dll but not consuming it.
target_compile_definitions(${PROJECT_NAME} PRIVATE "ARM_CONTROL_BUILDING_DLL")

# Export hardware plugins
pluginlib_export_plugin_description_file(hardware_interface arm_control.xml)
# Export controller plugins
pluginlib_export_plugin_description_file(controller_interface arm_control.xml)

# INSTALL
install(
  DIRECTORY hardware/include/
  DESTINATION include/arm_control
)
install(
  DIRECTORY description/launch description/ros2_control description/urdf
  DESTINATION share/arm_control
)
install(
  DIRECTORY bringup/launch bringup/config
  DESTINATION share/arm_control
)
install(
    TARGETS send_trajectory
    RUNTIME DESTINATION lib/arm_control
)

install(TARGETS arm_control
  EXPORT export_arm_control
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

## if(BUILD_TESTING)
##  find_package(ament_cmake_pytest REQUIRED)

##  ament_add_pytest_test(example_7_urdf_xacro test/test_urdf_xacro.py)
##  ament_add_pytest_test(view_example_7_launch test/test_view_robot_launch.py)
## endif()

## EXPORTS
ament_export_targets(export_arm_control HAS_LIBRARY_TARGET)
ament_export_dependencies(${HW_IF_INCLUDE_DEPENDS} ${REF_GEN_INCLUDE_DEPENDS} ${CONTROLLER_INCLUDE_DEPENDS})
ament_package()
