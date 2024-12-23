# ==============================================================================
# Modified version of the file here:
# https://github.com/pablospe/cmake-example-library/blob/master/cmake/SetEnv.cmake
# ==============================================================================
# Print the logo
file(READ "${CMAKE_CURRENT_LIST_DIR}/AsciiLogo.txt" ASCII_OOMPH_LIB_LOGO)
message("${ASCII_OOMPH_LIB_LOGO}")

# Important: prohibit in-source builds!
if(PROJECT_SOURCE_DIR STREQUAL PROJECT_BINARY_DIR)
  message(
    FATAL_ERROR
      "In-source builds not allowed. Please make a new directory (called a build directory) and run CMake from there."
  )
endif()

# If the user hasn't specified a custom installation path, we're going to
# install to the install/ subdirectory. However, if the user builds with the
# flag -DENABLE_INSTALL_AS_SUPERUSER=ON to force us to use the default system
# install path
if(PROJECT_IS_TOP_LEVEL
   AND (NOT ENABLE_INSTALL_AS_SUPERUSER)
   AND (CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT))
  set(CMAKE_INSTALL_PREFIX "${CMAKE_CURRENT_SOURCE_DIR}/install" CACHE PATH
      "Default installation path" FORCE)
  message(
    STATUS
      "Overriding default installation location. Will install to: ${CMAKE_INSTALL_PREFIX}"
  )
else()
  message(STATUS "Will install to: ${CMAKE_INSTALL_PREFIX}")
endif()

# Is oomph-lib being used directly or as an external project?
set(OOMPH_IS_MAIN_PROJECT FALSE)
if(PROJECT_IS_TOP_LEVEL)
  set(OOMPH_IS_MAIN_PROJECT TRUE)
endif()

# ------------------------------------------------------------------------------
# Configuration variables; create custom variables to avoid issues with regular
# variables being overriden by third-party libraries or by parties that import
# this library.
# ------------------------------------------------------------------------------
# cmake-format: off

# The project directory; passed to consumers of the exported library in case they
# need to use anything from there, e.g. the demo_drivers nearly all need the
# fpdiff.py script from the scripts/ subdirectory.
# FIXME: Change this as we will be installing the fpdiff.py file...
set(OOMPH_ROOT_DIR "${PROJECT_SOURCE_DIR}")

# Define the key files we need to install
set(OOMPH_EXPORTS_TARGET_NAME "${PROJECT_NAME}Exports")
set(OOMPH_BUILD_DIR "${CMAKE_CURRENT_BINARY_DIR}")
set(OOMPH_CMAKE_CONFIG_FILE_TEMPLATE "${CMAKE_CURRENT_LIST_DIR}/${PROJECT_NAME}Config.cmake.in")
set(OOMPH_CMAKE_CONFIG_FILE "${OOMPH_BUILD_DIR}/${PROJECT_NAME}Config.cmake")
set(OOMPH_CMAKE_CONFIG_VERSION_FILE "${OOMPH_BUILD_DIR}/${PROJECT_NAME}ConfigVersion.cmake")
set(OOMPH_CMAKE_EXPORTS_FILE "${OOMPH_BUILD_DIR}/${PROJECT_NAME}Exports.cmake")

# Introduce CMAKE_INSTALL[_FULL]_LIBDIR, CMAKE_INSTALL[_FULL]_BINDIR, and
# CMAKE_INSTALL[_FULL]_INCLUDEDIR
include(GNUInstallDirs)

# Set the install paths. Note that we don't use the CMAKE_INSTALL_<XXX>DIR
# (relative paths; e.g. bin/, lib/, include/) variables instead of the
# CMAKE_INSTALL_FULL_<XXX>DIR (absolute paths; e.g. /usr/bin/, /usr/lib/,
# /usr/include) so that the user can still override the installation
# destination after the configuration step. For example, the user may configure
# and build oomph-lib but later pick a custom install path with
#
# cmake --install . --prefix <new-install-path>
#
# We have to make sure that we can handle this case
set(OOMPH_INSTALL_LIB_DIR "${CMAKE_INSTALL_LIBDIR}/${PROJECT_NAME}")
set(OOMPH_INSTALL_CONFIG_DIR "${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}")
set(OOMPH_INSTALL_INCLUDE_DIR "${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_NAME}")
set(OOMPH_INSTALL_BIN_DIR "${CMAKE_INSTALL_BINDIR}/${PROJECT_NAME}")

# Silence warnings on MacOS about targets of ranlib having no symbols. This
# occurs when there is no code to be compiled, e.g. when #ifdef directives
# exclude all of the code from all of the files required by a library. This
# could possibly moved to its own simple module. Found online somewhere...
if(APPLE)
  set(CMAKE_C_ARCHIVE_CREATE "<CMAKE_AR> Scr <TARGET> <LINK_FLAGS> <OBJECTS>")
  set(CMAKE_CXX_ARCHIVE_CREATE "<CMAKE_AR> Scr <TARGET> <LINK_FLAGS> <OBJECTS>")
endif()

# Define the namespace for libraries to be exported within
set(PROJECT_NAMESPACE oomph)

# Storage for the list of libraries exported by oomph-lib
set(OOMPHLIB_LIBRARIES CACHE INTERNAL "" FORCE)

# Storage for the list of libraries exported by oomph-lib
set(OOMPH_CONFIG_VARS
    CMAKE_BUILD_TYPE
    BUILD_SHARED_LIBS
    CMAKE_INSTALL_PREFIX
    CACHE INTERNAL "List of oomph-lib configuration options" FORCE)

# Storage for files that are installed but not necessarily in the
# install_manifest.txt, e.g. symlinks to headers
set(EXTRA_INSTALLED_FILES_FOR_CLEAN_UP CACHE INTERNAL "" FORCE)

# Make sure the library artifacts generated by different configurations (i.e.
# Debug, Release, RelWithDebInfo, and MinSizeRel) don't clash
set(CMAKE_RELEASE_POSTFIX "")
set(CMAKE_DEBUG_POSTFIX "d")
set(CMAKE_RELWITHDEBINFO_POSTFIX "rd")
set(CMAKE_MINSIZEREL_POSTFIX "mr")

# Set the export target for libraries built by oomph-lib
set(TARGETS_EXPORT_NAME ${PROJECT_NAME}Exports)

# cmake-format: on
# ------------------------------------------------------------------------------
