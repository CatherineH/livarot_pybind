# SPDX-License-Identifier: GPL-2.0-or-later
include(FindPackageHandleStandardArgs)
set(livarot_SRC
	path-description.cpp
	Path.cpp
	stringstream.cpp
	geom.cpp
	Shape.cpp
	sweep-event.cpp
	sweep-tree.cpp
	sweep-tree-list.cpp
	ShapeSweep.cpp
	ShapeMisc.cpp
	ShapeRaster.cpp
	ShapeDraw.cpp
	PathConversion.cpp
	PathStroke.cpp
	PathOutline.cpp
	PathSimplify.cpp
	PathCutting.cpp
	AlphaLigne.cpp
	AVL.cpp
	BitLigne.cpp
	float-line.cpp
	int-line.cpp


	# -------
	# Headers
	AVL.h
	AlphaLigne.h
	BitLigne.h
	float-line.h
	int-line.h
	LivarotDefs.h
	stringstream.h
	path-description.h
	Path.h
	stringstream.h
	bool-op.h
	Shape.h
	sweep-event-queue.h
	sweep-tree-list.h
	sweep-event.h
	sweep-tree.h
	geom.h
	geom-curves.h

)

find_package(PkgConfig REQUIRED)
pkg_check_modules(2Geom 2geom>=1.1.0)
pkg_check_modules(glib glib-2.0)
pkg_check_modules(GSL REQUIRED gsl)
#find_library(DoubleConversion_LIBRARY double-conversion PATHS ${DoubleConversion_LIBRARYDIR})

#find_path(DoubleConversion_INCLUDE_DIR double-conversion/double-conversion.h PATHS ${DoubleConversion_INCLUDEDIR})
find_package_handle_standard_args(DoubleConversion DEFAULT_MSG
	  DoubleConversion_LIBRARY
	    DoubleConversion_INCLUDE_DIR)

message("DoubleConversion libraries libdir ${DoubleConversion_LIBRARY} includedir ${DoubleConversion_INCLUDE_DIR}")

add_library(livarot STATIC ${livarot_SRC})
set_property(TARGET livarot PROPERTY POSITION_INDEPENDENT_CODE ON)
set_property(TARGET livarot PROPERTY CXX_STANDARD 17)
#add_inkscape_lib(livarot_LIB "${livarot_SRC}")
target_include_directories(livarot PUBLIC . ${glib_INCLUDE_DIRS} ${2Geom_INCLUDE_DIRS})
target_link_libraries(livarot PUBLIC 2geom glib-2.0 ${GSL_LDFLAGS} ${DoubleConversion_LIBRARY})