cmake_minimum_required(VERSION 3.0.2)
project(elec_charge)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES elec_charge
#  CATKIN_DEPENDS roscpp rospy std_msgs
#  DEPENDS system_lib
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS
  src/IR_mode_pub.py
  src/proj_cam_pub_with_T.py  
  src/proj_control_motor.py
  src/test_cam_pub.py
  src/test.py
  src/test_control_sub.py
  src/test_IR_TOF_pub.py
  src/test_TOF_pub.py
  src/proj_TOF_pub.py
  src/test_IR_pub.py
  src/functionalize_cam_pub.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

# 9d7903718cb9f8aab984130974b7fae9320eb7b5..28efc4eae233c3f27e3d93cedb6a0477fcac91ba