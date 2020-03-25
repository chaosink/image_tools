cmake_minimum_required(VERSION 3.5)
project(block)

set(CMAKE_CXX_STANDARD 14)

set (CMAKE_MODULE_PATH
		"${PROJECT_SOURCE_DIR}/cmake/Modules")

find_package(OpenEXR)
find_package(Boost REQUIRED COMPONENTS filesystem)

add_executable(exrscale exrscale.cpp)
target_link_libraries(exrscale
		${OPENEXR_LIBRARIES}
		${Boost_LIBRARIES})
