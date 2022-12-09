cmake_minimum_required(VERSION 3.12)
project(gmock CXX) 
INCLUDE(FindPkgConfig)
pkg_check_modules(PKGS_DEP REQUIRED 
    gtest
    gmock
)
set(CMAKE_CXX_FLAGS "-g -O0")

FOREACH(flag ${PKGS_DEP_CFLAGS})
    #message(STATUS "flag: ${flag}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${flag}")
ENDFOREACH()
FOREACH(flag ${PKGS_DEP_LDFLAGS})
    message(STATUS "link flag: ${flag}")
    #set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${flag}")
ENDFOREACH()

set(LDFLAGS_BASE ${PKGS_DEP_LDFLAGS}) 

set(target mock01)
set(${target}_link "${LDFLAGS_BASE}")


message(STATUS "CXX FLAGS: ${CMAKE_CXX_FLAGS}")
message(STATUS "LD  FLAGS: ${${target}_link}")

add_executable (${target} ${target}.cpp)

target_link_libraries (${target} LINK_PUBLIC ${LDFLAGS_BASE})

#target_link_libraries (${target} LINK_PUBLIC ${${target}_link})
