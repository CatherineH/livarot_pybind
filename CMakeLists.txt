cmake_minimum_required(VERSION 3.20)
project(LivarotPy)

include(FindPython3)
set(PYTHON_INCLUDE_DIRS C:\\Program\ Files\\Python39\\include)
set(Python_LIBRARIES C:\\Program\ Files\\Python39\\libs)
set(PYTHON_LIBRARY C:\\Program\ Files\\Python39\\libs\\python3.lib)
set(Python_EXECUTABLE C:\\Program\ Files\\Python39\\python.exe)
find_package(PythonLibs REQUIRED)
find_package(PkgConfig REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

pkg_check_modules(2Geom 2geom>=1.1.0)
pkg_check_modules(GSL REQUIRED gsl)
pkg_check_modules(glib glib-2.0)
add_subdirectory(livarot)

message("2geom libraries ${2Geom_INCLUDE_DIRS}")
python3_add_library(pylivarot MODULE livarot_pybind.cpp)
set_property(TARGET pylivarot PROPERTY CXX_STANDARD 17)
target_include_directories(pylivarot PUBLIC ${2Geom_INCLUDE_DIRS} livarot) 

target_link_libraries(pylivarot PUBLIC glib-2.0 2geom livarot gsl)

target_compile_definitions(pylivarot PRIVATE)
