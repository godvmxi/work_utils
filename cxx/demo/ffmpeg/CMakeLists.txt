
cmake_minimum_required(VERSION 3.14 FATAL_ERROR)
project(ffmpeg)

set(TARGET_NAME frame_test)

find_library(AVCODEC_LIBRARY avcodec)
find_library(AVFORMAT_LIBRARY avformat)
find_library(AVUTIL_LIBRARY avutil)
find_library(GTEST_LIBRARY gtest)

list(APPEND TARGET_SRCs "${CMAKE_CURRENT_SOURCE_DIR}/brv_bit_stream_parser.cpp")
list(APPEND TARGET_SRCs "${CMAKE_CURRENT_SOURCE_DIR}/test_brv_bs_parser.cpp")

add_executable(${TARGET_NAME}  ${TARGET_SRCs})
target_include_directories(${TARGET_NAME} PRIVATE ${TARGET_INCLUDEs} )

target_link_libraries(${TARGET_NAME}    ${AVCODEC_LIBRARY}
                                        ${AVFORMAT_LIBRARY}
                                        ${AVUTIL_LIBRARY}
                                        ${GTEST_LIBRARY}
                                        pthread
)
set(BR_DIAG_BUILD_TOP_DIR      ${CMAKE_CURRENT_BINARY_DIR} )
set(BR_INSTALL_DIR "${BR_DIAG_BUILD_TOP_DIR}")


install(DIRECTORY   ${CMAKE_CURRENT_SOURCE_DIR}/decoder DESTINATION "${BR_INSTALL_DIR}/external/media/vcodec/stream" USE_SOURCE_PERMISSIONS)

