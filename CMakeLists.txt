# ==============================================================================

cmake_minimum_required(VERSION 3.24 FATAL_ERROR)
project(fpdiff VERSION 0.0.1)
enable_testing()

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

# Build in debugging mode by default
if(NOT CMAKE_BUILD_TYPE OR CMAKE_BUILD_TYPE STREQUAL "")
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING "" FORCE)
endif()

# Silence Apple warning
if(APPLE)
  set(CMAKE_OSX_DEPLOYMENT_TARGET 13.0)
endif()

# ---------------------------[ VERSION 1: USE BOOST ]---------------------------

# FIXME: Argh! Boost might not always be provided!

# Search for Boost
find_package(
  Boost
  COMPONENTS iostreams
  QUIET)

if(Boost_FOUND)
  # Define target and link to Boost libraries
  add_executable(fpdiff_boost fpdiff_boost.cc)
  target_link_libraries(fpdiff_boost PRIVATE Boost::iostreams)

  # Symlink the data/ folder into the build/ directory when building
  add_custom_command(
    TARGET fpdiff_boost COMMAND ln -sf "${CMAKE_CURRENT_LIST_DIR}/data"
                                "${CMAKE_CURRENT_BINARY_DIR}")

  # Add test
  add_test(
    NAME fpdiff_boost
    COMMAND ${BASH_PROGRAM} fpdiff_boost
    WORKING_DIRECTORY "${CMAKE_BINARY_DIR}")
endif()

# ---------------------------[ VERSION 2: USE ZLIB ]----------------------------

# Find ZLib
find_package(ZLIB REQUIRED)
if(NOT ZLIB_FOUND)
  # Download the zlib library
  include(FetchContent)
  FetchContent_Declare(
    zlib
    GIT_REPOSITORY https://github.com/puneetmatharu/zlib.git
    GIT_TAG v1.2.14
    GIT_PROGRESS TRUE
    GIT_SHALLOW TRUE)
  FetchContent_MakeAvailable(zlib)
endif()

# Define target and link to Boost libraries
add_executable(fpdiff fpdiff.cc fpdiff.h)
target_link_libraries(fpdiff PRIVATE ZLIB::ZLIB)

# Symlink the data/ folder into the build/ directory when building fpdiff
add_custom_command(
  TARGET fpdiff COMMAND ln -sf "${CMAKE_CURRENT_LIST_DIR}/data"
                        "${CMAKE_CURRENT_BINARY_DIR}")

# Add test
add_test(
  NAME fpdiff
  COMMAND ${BASH_PROGRAM} fpdiff
  WORKING_DIRECTORY "${CMAKE_BINARY_DIR}")

# ------------------------------------------------------------------------------
