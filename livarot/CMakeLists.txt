# SPDX-License-Identifier: GPL-2.0-or-later
cmake_minimum_required(VERSION 3.20)

project(livarot)

set(livarot_SRC
	AlphaLigne.cpp
	AVL.cpp
	BitLigne.cpp
	float-line.cpp
	int-line.cpp
	PathConversion.cpp
	Path.cpp
	PathCutting.cpp
	path-description.cpp
	PathOutline.cpp
	PathSimplify.cpp
	PathStroke.cpp
	Shape.cpp
	ShapeDraw.cpp
	ShapeMisc.cpp
	ShapeRaster.cpp
	ShapeSweep.cpp
	sweep-event.cpp
	sweep-tree.cpp
	sweep-tree-list.cpp


	# -------
	# Headers
	AVL.h
	AlphaLigne.h
	BitLigne.h
	LivarotDefs.h
	Path.h
	Shape.h
	float-line.h
	bool-op.h
	int-line.h
	path-description.h
	sweep-event-queue.h
	sweep-event.h
	sweep-tree-list.h
	sweep-tree.h
	stringstream.h
	geom.h
	geom-curves.h
)

find_package(PkgConfig REQUIRED)
pkg_check_modules(2Geom 2geom>=1.1.0)
pkg_check_modules(glib glib-2.0)

add_library(livarot STATIC ${livarot_SRC})

#add_inkscape_lib(livarot_LIB "${livarot_SRC}")
target_include_directories(livarot PUBLIC . ${glib_INCLUDE_DIRS} ${2Geom_INCLUDE_DIRS})
target_link_libraries(livarot PUBLIC 2geom glib-2.0)
