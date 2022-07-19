cmake_minimum_required(VERSION 3.10 FATAL_ERROR)
set(TARGET js_wark)

set (CMAKE_CMN_CXX_FLAGS "-Wall -std=c++11")
if ( "${CMAKE_BUILD_TYPE}" STREQUAL Release )
    message(STATUS "Build version: Release")
    set ( BR_BUILD_TYPE "rel")
    set ( CMAKE_CXX_FLAGS "${CMAKE_CMN_CXX_FLAGS} -DNDEBUG" )
else ()
    message(STATUS "Build version: Debug")
    set ( BR_BUILD_TYPE "dbg")
    set ( CMAKE_CXX_FLAGS "${CMAKE_CMN_CXX_FLAGS} -g -O0" )
endif ()


list(APPEND TARGET_SRCs "main.cpp")

list(APPEND TARGET_INCLUDEs "./" )


add_executable(${TARGET}  ${TARGET_SRCs})
target_include_directories(${TARGET} PRIVATE ${TARGET_INCLUDEs} )



install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/data DESTINATION ${CMAKE_CURRENT_BINARY_DIR})