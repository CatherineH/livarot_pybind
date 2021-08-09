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


pkg_check_modules(2Geom 2geom>=1.1.0)
pkg_check_modules(SIGC++ REQUIRED sigc++-2.0 )
pkg_check_modules(glibmm glibmm-2.4)
pkg_check_modules(Cairo cairo>=1.14)
pkg_check_modules(gtk gtk+-3.0)
pkg_check_modules(gtkmm gtkmm-3.0)

#add_library(2Geom::2geom ALIAS PkgConfig::2Geom)
message("cairo librarie ${Cairo_INCLUDE_DIRS}")
message("sigc++ libraries ${SIGC++_INCLUDE_DIRS}")
message("2geom libraries ${2Geom_INCLUDE_DIRS}")
message("gtk libraires ${gtk_INCLUDE_DIRS}")
python3_add_library(livarot MODULE livarot_pybind.cpp)
set_property(TARGET livarot PROPERTY CXX_STANDARD 20)
target_include_directories(livarot PUBLIC ${2Geom_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS} ${SIGC++_INCLUDE_DIRS} ${Python3_INCLUDE_DIRS} 
	${glibmm_INCLUDE_DIRS} ${Cairo_INCLUDE_DIRS} ${gtk_INCLUDE_DIRS} ${gtkmm_INCLUDE_DIRS})
include_directories(..\\inkscape\\src) 



target_compile_definitions(livarot PRIVATE)
