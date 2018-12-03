# CMake build script for GASol test.

# Compile google test.
set(GTEST_DIR ${CMAKE_CURRENT_SOURCE_DIR}/googletest/googletest)
message(STATUS "Google test path: ${GTEST_DIR}")
add_subdirectory(${GTEST_DIR})

# Build test executable file.

# Include from GASol source.
include_directories(AFTER SYSTEM ${GTEST_DIR}/include/)
include_directories(${PROJECT_SOURCE_DIR}/src)

# Link directories.
link_directories(${CMAKE_CURRENT_BINARY_DIR}/../src/)
link_directories(${CMAKE_CURRENT_BINARY_DIR}/googletest/googletest)

# Compile unittest.
file(GLOB TEST_SRCS *.cpp)
add_executable(unittest EXCLUDE_FROM_ALL ${TEST_SRCS})
target_link_libraries(unittest GASol gtest)

