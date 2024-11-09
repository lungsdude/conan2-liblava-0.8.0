cmake_minimum_required(VERSION 3.6)
project(test_package LANGUAGES CXX)

find_package(liblava REQUIRED)

add_executable(${PROJECT_NAME} example.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE liblava::liblava)
