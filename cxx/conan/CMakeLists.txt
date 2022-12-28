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
message("-- Conan gtest include dir : ${CONAN_INCLUDE_DIRS_GTEST}")
message("-- Conan gtest cxx  flags  : ${CONAN_CXX_FLAGS_GTEST}")
message("-- Conan gtest link flags  : ${CONAN_SHARED_LINK_FLAGS_GTEST}")

message("-- Conan zlib include dir : ${CONAN_INCLUDE_DIRS_ZLIB}")
message("-- Conan zlib cxx  flags  : ${CONAN_CXX_FLAGS_ZLIB}")
message("-- Conan zlib link flags  : ${CONAN_SHARED_LINK_FLAGS_ZLIB}")

message("-- CONAN_DEFINES  : ${CONAN_DEFINES}")
message("-- CONAN_COMPILE_DEFINITIONS  : ${CONAN_COMPILE_DEFINITIONS}")
message("-- CONAN_CXX_FLAGS	  : ${CONAN_CXX_FLAGS}")
message("-- CONAN_LIB_DIRS  : ${CONAN_LIB_DIRS}")
message("-- CONAN_LIBS  : ${CONAN_LIBS}")
message("-- CONAN_PKG_LIBS  : ${CONAN_PKG_LIBS}")
message("-- CONAN_EXE_LINKER_FLAGS  : ${CONAN_EXE_LINKER_FLAGS}")
message("-- CONAN_SHARED_LINK_FLAGS  : ${CONAN_SHARED_LINK_FLAGS}")

message("-- CONAN_DEFINES  : ${CONAN_DEFINES}")

add_executable (${target} ${target}.cpp)

target_link_libraries (${target} 
            ${CONAN_LIBS}
            )

