# Install script for directory: /home/bhg/project/KG-Kairos_1st/Final_Project/catkin_ws/src/elec_charge_with_ir

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/bhg/project/KG-Kairos_1st/Final_Project/catkin_ws/install")
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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/bhg/project/KG-Kairos_1st/Final_Project/catkin_ws/build/elec_charge_with_ir/catkin_generated/installspace/elec_charge_with_ir.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/elec_charge_with_ir/cmake" TYPE FILE FILES
    "/home/bhg/project/KG-Kairos_1st/Final_Project/catkin_ws/build/elec_charge_with_ir/catkin_generated/installspace/elec_charge_with_irConfig.cmake"
    "/home/bhg/project/KG-Kairos_1st/Final_Project/catkin_ws/build/elec_charge_with_ir/catkin_generated/installspace/elec_charge_with_irConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/elec_charge_with_ir" TYPE FILE FILES "/home/bhg/project/KG-Kairos_1st/Final_Project/catkin_ws/src/elec_charge_with_ir/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/elec_charge_with_ir" TYPE PROGRAM FILES "/home/bhg/project/KG-Kairos_1st/Final_Project/catkin_ws/build/elec_charge_with_ir/catkin_generated/installspace/IR_mode_pub.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/elec_charge_with_ir" TYPE PROGRAM FILES "/home/bhg/project/KG-Kairos_1st/Final_Project/catkin_ws/build/elec_charge_with_ir/catkin_generated/installspace/proj_cam_pub_with_T.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/elec_charge_with_ir" TYPE PROGRAM FILES "/home/bhg/project/KG-Kairos_1st/Final_Project/catkin_ws/build/elec_charge_with_ir/catkin_generated/installspace/proj_control_motor.py")
endif()

