cmake_minimum_required(VERSION 3.20)
project(LivarotPy)
# this is unfortunately required in order to make a "manylinux" wheel suitable for pypi
set(BUILD_SHARED_LIBS OFF)
set(CMAKE_CXX_FLAGS "-static-libstdc++ -static-libgcc -fpermissive" ) # -std=c++17 needed for windows/msys2

find_package(Python3 ${PYTHON_MAJOR_VERSION}.${PYTHON_MINOR_VERSION} EXACT REQUIRED COMPONENTS Interpreter Development.Module)
add_subdirectory(pybind11)


find_package(PkgConfig REQUIRED)
#pkg_check_modules(2Geom 2geom>=1.1.0)
pkg_check_modules(GSL REQUIRED gsl)
pkg_check_modules(glib glib-2.0)
add_subdirectory(livarot)

pybind11_add_module(_pylivarot MODULE livarot_pybind.cpp)
#add_link_options("-static")
set_property(TARGET _pylivarot PROPERTY CXX_STANDARD 17)
target_include_directories(_pylivarot PUBLIC ${Python3_INCLUDE_DIRS} ${2GEOM_INCLUDE_DIR}) 

target_link_directories(_pylivarot PUBLIC)
#target_link_libraries(_pylivarot PUBLIC livarot gsl 2geom)
target_link_libraries(_pylivarot PUBLIC livarot 2geom double-conversion)
get_property(dirs TARGET _pylivarot PROPERTY LINK_DIRECTORIES)
message("pylivarot link_directories")
foreach(dir ${dirs})
  message("dir='${dir}'")
endforeach()

get_property(dirs TARGET _pylivarot PROPERTY LINK_LIBRARIES)
message("pylivarot link_libraries")
foreach(dir ${dirs})
  message("lib='${dir}'")
endforeach()

target_compile_definitions(_pylivarot PRIVATE)
