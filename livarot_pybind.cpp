#include <pybind11/pybind11.h>
#include <2geom/svg-path-parser.h>
#include <2geom/svg-path-writer.h>
#include <2geom/path-sink.h>
#include <2geom/pathvector.h>
#include "livarot/Shape.h"
#include "livarot/Path.h"
#include "livarot/LivarotDefs.h"
#include "livarot/geom.h"

namespace py = pybind11;


PYBIND11_MODULE(_pylivarot, m) {
    m.doc() = "python bindings to the functionality within livarot"; 
    py::module_ m2geom = m.def_submodule("py2geom", "python bindings to the functionality within 2geom");
    py::class_<Geom::PathVector>(m2geom, "PathVector")
        .def(py::init<>())
        .def("push_back", &Geom::PathVector::push_back)
        .def("back", py::overload_cast<>(&Geom::PathVector::back))
        .def("boundsFast", &Geom::PathVector::boundsFast);
    py::class_<Geom::Path>(m2geom, "Path")
        .def(py::init<>())
        .def("setStitching", &Geom::Path::setStitching)
        .def("start", &Geom::Path::start)
        .def("initialPoint", &Geom::Path::initialPoint);

    py::class_<Geom::PathSink>(m2geom, "PathSink");
    py::class_<Geom::PathBuilder, Geom::PathSink>(m2geom, "PathBuilder")
        .def(py::init<>());
    py::class_<Geom::SVGPathParser>(m2geom, "SVGPathParser")
        .def(py::init<Geom::PathSink &>())
        .def("setZSnapThreshold", &Geom::SVGPathParser::setZSnapThreshold)
        .def("parse", py::overload_cast<std::string const &>(&Geom::SVGPathParser::parse));
    py::class_<Geom::SVGPathWriter>(m2geom, "SVGPathWriter")
        .def(py::init<>())
        .def("str", &Geom::SVGPathWriter::str);
    m2geom.def("parse_svg_path", py::overload_cast<char const *>(&Geom::parse_svg_path));

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

    py::enum_<bool_op>(m, "bool_op")
        .value("bool_op_union", bool_op::bool_op_union)
        .value("bool_op_inters", bool_op::bool_op_inters)
        .value("bool_op_diff", bool_op::bool_op_diff)
        .value("bool_op_symdiff", bool_op::bool_op_symdiff)
        .value("bool_op_cut", bool_op::bool_op_cut)
        .value("bool_op_slice", bool_op::bool_op_slice)
        .export_values();

    py::enum_<FirstOrLast>(m, "FirstOrLast")
        .value("FIRST", FirstOrLast::FIRST)
        .value("LAST", FirstOrLast::LAST)
        .export_values();

    py::class_<Path::cut_position>(m, "cut_position")
        .def_readwrite("piece", &Path::cut_position::piece)
        .def_readwrite("t", &Path::cut_position::t);

    m.def("pathv_to_linear_and_cubic_beziers", pathv_to_linear_and_cubic_beziers);    

}
