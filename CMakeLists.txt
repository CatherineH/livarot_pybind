cmake_minimum_required(VERSION 3.20)
project(LivarotPy)

include(FindPython3)
set(PYTHON_INCLUDE_DIRS C:\\Program\ Files\\Python39\\include)
set(Python_LIBRARIES C:\\Program\ Files\\Python39\\libs)
set(PYTHON_LIBRARY C:\\Program\ Files\\Python39\\libs\\python3.lib)
set(Python_EXECUTABLE C:\\Program\ Files\\Python39\\python.exe)
find_package(PythonLibs REQUIRED)
find_package(PkgConfig REQUIRED)
find_package(Boost 1.60 REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
add_subdirectory(pybind11)

pkg_check_modules(2Geom 2geom>=1.1.0)
pkg_check_modules(GSL REQUIRED gsl)
pkg_check_modules(glib glib-2.0)
add_subdirectory(livarot)

message("2geom libraries ${2Geom_INCLUDE_DIRS}")
#python3_add_library(pylivarot MODULE livarot_pybind.cpp)
pybind11_add_module(_pylivarot MODULE livarot_pybind.cpp)
set_property(TARGET _pylivarot PROPERTY CXX_STANDARD 17)
target_include_directories(_pylivarot PUBLIC ${Python3_INCLUDE_DIRS} ${2Geom_INCLUDE_DIRS} livarot) 


target_link_libraries(_pylivarot PUBLIC 2geom livarot gsl)
get_property(dirs TARGET _pylivarot PROPERTY LINK_DIRECTORIES)
message("pylivarot link_directories")
foreach(dir ${dirs})
  message("dir='${dir}'")
endforeach()

target_compile_definitions(_pylivarot PRIVATE)
