#include <pybind11/pybind11.h>
#include <2geom/svg-path-parser.h>
#include <2geom/path-sink.h>
#include "livarot/Shape.h"
#include "livarot/Path.h"


namespace py = pybind11;


PYBIND11_MODULE(pylivarot, m) {
    m.doc() = "python bindings to the functionality within livarot, with some helper classes from 2geom and inkscape"; 
    py::class_<Geom::PathVector>(m, "PathVector");
    py::class_<Geom::PathSink>(m, "PathSink");
    py::class_<Path>(m, "Path")
    .def(py::init<>())
    .def("LoadPathVector", py::overload_cast<Geom::PathVector const &>(&Path::LoadPathVector));

    py::class_<Geom::PathBuilder, Geom::PathSink>(m, "PathBuilder")
    .def(py::init<>());
    py::class_<Geom::SVGPathParser>(m, "SVGPathParser")
    .def(py::init<Geom::PathSink &>())
    .def("setZSnapThreshold", &Geom::SVGPathParser::setZSnapThreshold)
    .def("parse", py::overload_cast<std::string const &>(&Geom::SVGPathParser::parse));
    py::class_<Shape>(m, "Shape")
    .def(py::init<>())
    .def("Booleen", &Shape::Booleen);

    m.def("parse_svg_path", py::overload_cast<char const *>(&Geom::parse_svg_path));

}