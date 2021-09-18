#include <pybind11/pybind11.h>
#include <2geom/svg-path-parser.h>
#include <2geom/path-sink.h>
#include "livarot/Shape.h"
#include "livarot/Path.h"
#include "livarot/LivarotDefs.h"

namespace py = pybind11;


PYBIND11_MODULE(_pylivarot, m) {
    m.doc() = "python bindings to the functionality within livarot, with some helper classes from 2geom and inkscape"; 
    py::class_<Geom::PathVector>(m, "PathVector");
    py::class_<Geom::PathSink>(m, "PathSink");

    py::class_<Shape>(m, "Shape")
    .def(py::init<>())
    .def("getPoint", &Shape::getPoint)
    .def("hasBackData", &Shape::hasBackData)
    .def("ConvertToShape", &Shape::ConvertToShape)
    .def("getEdge", &Shape::getEdge)
    .def("Booleen", &Shape::Booleen);

    py::class_<Path>(m, "Path")
    .def(py::init<>())
    .def("LoadPathVector", py::overload_cast<Geom::PathVector const &>(&Path::LoadPathVector))
    .def("ConvertWithBackData", &Path::ConvertWithBackData)
    .def("Fill", &Path::Fill, py::arg("dest")=static_cast<Shape *>(nullptr), py::arg("pathID")=-1, py::arg("justAdd")=false, 
		    py::arg("closeIfNeeded")=true, py::arg("invert")=false);


    py::enum_<FillRule>(m, "FillRule")
	    .value("fill_oddEven", FillRule::fill_oddEven)
	    .value("fill_nonZero", FillRule::fill_nonZero)
	    .value("fill_positive", FillRule::fill_positive)
	    .value("fill_justDont", FillRule::fill_justDont)
	    .export_values();

    py::class_<Geom::PathBuilder, Geom::PathSink>(m, "PathBuilder")
    .def(py::init<>());
    py::class_<Geom::SVGPathParser>(m, "SVGPathParser")
    .def(py::init<Geom::PathSink &>())
    .def("setZSnapThreshold", &Geom::SVGPathParser::setZSnapThreshold)
    .def("parse", py::overload_cast<std::string const &>(&Geom::SVGPathParser::parse));

    m.def("parse_svg_path", py::overload_cast<char const *>(&Geom::parse_svg_path));

}
