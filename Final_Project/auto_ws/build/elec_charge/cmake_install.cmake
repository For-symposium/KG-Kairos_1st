# Install script for directory: /home/jetson/auto_ws/KG-Kairos_1st/Final_Project/auto_ws/src/elec_charge

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/jetson/auto_ws/KG-Kairos_1st/Final_Project/auto_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/jetson/auto_ws/KG-Kairos_1st/Final_Project/auto_ws/build/elec_charge/catkin_generated/installspace/elec_charge.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/elec_charge/cmake" TYPE FILE FILES
    "/home/jetson/auto_ws/KG-Kairos_1st/Final_Project/auto_ws/build/elec_charge/catkin_generated/installspace/elec_chargeConfig.cmake"
    "/home/jetson/auto_ws/KG-Kairos_1st/Final_Project/auto_ws/build/elec_charge/catkin_generated/installspace/elec_chargeConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/elec_charge" TYPE FILE FILES "/home/jetson/auto_ws/KG-Kairos_1st/Final_Project/auto_ws/src/elec_charge/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/elec_charge" TYPE PROGRAM FILES "/home/jetson/auto_ws/KG-Kairos_1st/Final_Project/auto_ws/build/elec_charge/catkin_generated/installspace/IR_mode_pub.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/elec_charge" TYPE PROGRAM FILES "/home/jetson/auto_ws/KG-Kairos_1st/Final_Project/auto_ws/build/elec_charge/catkin_generated/installspace/proj_cam_pub_with_T.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/elec_charge" TYPE PROGRAM FILES "/home/jetson/auto_ws/KG-Kairos_1st/Final_Project/auto_ws/build/elec_charge/catkin_generated/installspace/proj_control_motor.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/elec_charge" TYPE PROGRAM FILES "/home/jetson/auto_ws/KG-Kairos_1st/Final_Project/auto_ws/build/elec_charge/catkin_generated/installspace/test_cam_pub.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/elec_charge" TYPE PROGRAM FILES "/home/jetson/auto_ws/KG-Kairos_1st/Final_Project/auto_ws/build/elec_charge/catkin_generated/installspace/test.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/elec_charge" TYPE PROGRAM FILES "/home/jetson/auto_ws/KG-Kairos_1st/Final_Project/auto_ws/build/elec_charge/catkin_generated/installspace/test_control_sub.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/elec_charge" TYPE PROGRAM FILES "/home/jetson/auto_ws/KG-Kairos_1st/Final_Project/auto_ws/build/elec_charge/catkin_generated/installspace/test_IR_TOF_pub.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/elec_charge" TYPE PROGRAM FILES "/home/jetson/auto_ws/KG-Kairos_1st/Final_Project/auto_ws/build/elec_charge/catkin_generated/installspace/test_TOF_pub.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/elec_charge" TYPE PROGRAM FILES "/home/jetson/auto_ws/KG-Kairos_1st/Final_Project/auto_ws/build/elec_charge/catkin_generated/installspace/proj_TOF_pub.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/elec_charge" TYPE PROGRAM FILES "/home/jetson/auto_ws/KG-Kairos_1st/Final_Project/auto_ws/build/elec_charge/catkin_generated/installspace/test_IR_pub.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/elec_charge" TYPE PROGRAM FILES "/home/jetson/auto_ws/KG-Kairos_1st/Final_Project/auto_ws/build/elec_charge/catkin_generated/installspace/functionalize_cam_pub.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/elec_charge" TYPE PROGRAM FILES "/home/jetson/auto_ws/KG-Kairos_1st/Final_Project/auto_ws/build/elec_charge/catkin_generated/installspace/temp_TOF_pub.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/elec_charge" TYPE PROGRAM FILES "/home/jetson/auto_ws/KG-Kairos_1st/Final_Project/auto_ws/build/elec_charge/catkin_generated/installspace/temp_robotarm.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/elec_charge" TYPE PROGRAM FILES "/home/jetson/auto_ws/KG-Kairos_1st/Final_Project/auto_ws/build/elec_charge/catkin_generated/installspace/charging_state.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/elec_charge" TYPE PROGRAM FILES "/home/jetson/auto_ws/KG-Kairos_1st/Final_Project/auto_ws/build/elec_charge/catkin_generated/installspace/add_manual_mode.py")
endif()

