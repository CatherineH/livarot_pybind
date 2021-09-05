# SPDX-License-Identifier: GPL-2.0-or-later

set(livarot_SRC
	path-description.cpp
	Path.cpp
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

add_library(livarot STATIC ${livarot_SRC})
set_property(TARGET livarot PROPERTY POSITION_INDEPENDENT_CODE ON)
set_property(TARGET livarot PROPERTY CXX_STANDARD 17)
#add_inkscape_lib(livarot_LIB "${livarot_SRC}")
target_include_directories(livarot PUBLIC . ${glib_INCLUDE_DIRS} ${2Geom_INCLUDE_DIRS})
target_link_libraries(livarot PUBLIC 2geom glib-2.0)
