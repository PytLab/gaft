# CMake script for gasol run executable program building.

include_directories(${PROJECT_SOURCE_DIR}/src)
link_directories(${CMAKE_BINARY_DIR}/../src/)
file(GLOB RUN_SRC *.cpp)
add_executable(example EXCLUDE_FROM_ALL ${RUN_SRC})
target_link_libraries(example GASol)

