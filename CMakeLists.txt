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
find_package(Boost 1.60 REQUIRED)
#find_package(sigc++ 3.0 REQUIRED)

pkg_check_modules(2Geom 2geom>=1.1.0)
pkg_check_modules(SIGC++ REQUIRED sigc++-3.0 )

#add_library(2Geom::2geom ALIAS PkgConfig::2Geom)
message("sigc++ libraries ${SIGC++_INCLUDE_DIRS}")
python3_add_library(livarot MODULE livarot_pybind.cpp)
set_property(TARGET livarot PROPERTY CXX_STANDARD 20)
target_include_directories(livarot PUBLIC ${2Geom_INCLUDEDIR} ${Boost_INCLUDE_DIRS} ${SIGC++_INCLUDE_DIRS})
include_directories(C:\\Users\\milan\\cpp_projects\\inkscape\\src C:\\Program\ Files\\Python39\\include 
C:\\Users\\milan\\AppData\\Roaming\\Python\\Python39\\site-packages\\pybind11\\include)



target_compile_definitions(livarot PRIVATE)