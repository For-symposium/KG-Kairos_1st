cmake_minimum_required(VERSION 3.0.2)
project(ros_serial_py)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS
  scripts/ros_serial.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
