cmake_minimum_required(VERSION 3.12)
project(gmock CXX) 
#set(CMAKE_CXX_FLAGS "-std=c++11 -g -O0")
SET(CMAKE_CXX_STANDARD 11)
SET(CMAKE_CXX_STANDARD_REQUIRED ON)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()


set(target mock01)
message(STATUS "CXX FLAGS: ${CMAKE_CXX_FLAGS}")
message("-- Conan libs: ${CONAN_LIBS}")
message("-- Conan flags: ${CONAN_FLAGS}")

add_executable (${target} ${target}.cpp)

target_link_libraries (${target} 
            ${CONAN_LIBS}
            )

