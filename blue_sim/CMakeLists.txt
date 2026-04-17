cmake_minimum_required(VERSION 3.8)
project(blue_sim)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS blue_sim/ardusub_bridge.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME ardusub_bridge
)
install(PROGRAMS blue_sim/ardusub_init.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME ardusub_init
)

install(DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
