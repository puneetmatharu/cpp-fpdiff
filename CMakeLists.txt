# ==============================================================================

cmake_minimum_required(VERSION 3.24 FATAL_ERROR)
project(fpdiff VERSION 1.0.0)
enable_testing()

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

# Build in debugging mode by default
if(NOT CMAKE_BUILD_TYPE OR CMAKE_BUILD_TYPE STREQUAL "")
  set(CMAKE_BUILD_TYPE
      "Release"
      CACHE STRING "" FORCE)
endif()

# ---------------------------------[ PACKAGES ]---------------------------------

# Search for Boost
find_package(
  Boost
  COMPONENTS iostreams
  QUIET)

set(OVERRIDE_FIND_PACKAGE TRUE)
set(ENABLE_NEXT_GEN_ZLIB FALSE)

# See if we can find zlib
if(NOT OVERRIDE_FIND_PACKAGE)
  find_package(ZLIB REQUIRED)
endif()

# Download it ourselves
if((NOT ZLIB_FOUND) OR (OVERRIDE_FIND_PACKAGE))
  include(FetchContent)
  FetchContent_Declare(
    zlib
    GIT_REPOSITORY https://github.com/puneetmatharu/zlib.git
    GIT_TAG v1.2.14
    GIT_PROGRESS TRUE
    GIT_SHALLOW TRUE)
  FetchContent_MakeAvailable(zlib)
endif()

# ---------------------------[ VERSION 1: USE BOOST ]---------------------------

if(Boost_FOUND)
  set(TEST_NAME fpdiff_boost)

  # Define target and link to Boost libraries
  add_executable(${TEST_NAME} ${TEST_NAME}.cc)
  target_link_libraries(${TEST_NAME} PRIVATE Boost::iostreams)

  # Symlink the data/ folder into the build/ directory when building
  add_custom_command(
    TARGET ${TEST_NAME} COMMAND ln -sf "${CMAKE_CURRENT_LIST_DIR}/data"
                                "${CMAKE_CURRENT_BINARY_DIR}")

  # Add test
  add_test(
    NAME ${TEST_NAME}
    COMMAND ${BASH_PROGRAM} ${TEST_NAME}
    WORKING_DIRECTORY "${CMAKE_BINARY_DIR}")
endif()

# ---------------------------[ VERSION 2: USE ZLIB ]----------------------------

set(TEST_NAME fpdiff_zlib)

# Define target and link to Boost libraries
add_executable(${TEST_NAME} ${TEST_NAME}.cc)
target_link_libraries(${TEST_NAME} PRIVATE ZLIB::ZLIB)

# Symlink the data/ folder into the build/ directory when building
add_custom_command(
  TARGET ${TEST_NAME} COMMAND ln -sf "${CMAKE_CURRENT_LIST_DIR}/data"
                              "${CMAKE_CURRENT_BINARY_DIR}")

# Add test
add_test(
  NAME ${TEST_NAME}
  COMMAND ${BASH_PROGRAM} ${TEST_NAME}
  WORKING_DIRECTORY "${CMAKE_BINARY_DIR}")

# ----------------------------[ BASIC GZIP PARSER ]-----------------------------

set(TEST_NAME gzip_parser)

add_library(gzip_reader STATIC gzip_reader.cc gzip_reader.h)
target_link_libraries(gzip_reader PRIVATE ZLIB::ZLIB)
target_include_directories(gzip_reader PRIVATE ${CMAKE_CURRENT_LIST_DIR})

# Define target and link to Boost libraries
add_executable(${TEST_NAME} ${TEST_NAME}.cc)
target_link_libraries(${TEST_NAME} PRIVATE gzip_reader)

# Symlink the data/ folder into the build/ directory when building
add_custom_command(
  TARGET ${TEST_NAME} COMMAND ln -sf "${CMAKE_CURRENT_LIST_DIR}/data"
                              "${CMAKE_CURRENT_BINARY_DIR}")

# Add test
add_test(
  NAME ${TEST_NAME}
  COMMAND ${BASH_PROGRAM} ${TEST_NAME}
  WORKING_DIRECTORY "${CMAKE_BINARY_DIR}")

# ----------------------------[ BASIC GZIP PARSER ]-----------------------------

set(TEST_NAME load_gzip)

# Define target and link to Boost libraries
add_executable(${TEST_NAME} ${TEST_NAME}.cc)
target_link_libraries(${TEST_NAME} PRIVATE gzip_reader)

# Symlink the data/ folder into the build/ directory when building
add_custom_command(
  TARGET ${TEST_NAME} COMMAND ln -sf "${CMAKE_CURRENT_LIST_DIR}/data"
                              "${CMAKE_CURRENT_BINARY_DIR}")

# Add test
add_test(
  NAME ${TEST_NAME}
  COMMAND ${BASH_PROGRAM} ${TEST_NAME}
  WORKING_DIRECTORY "${CMAKE_BINARY_DIR}")

# ------------------------------------------------------------------------------
