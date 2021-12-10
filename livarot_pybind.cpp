#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <2geom/svg-path-parser.h>
#include <2geom/svg-path-writer.h>
#include <2geom/path.h>
#include <2geom/path-sink.h>
#include <2geom/pathvector.h>
#include <2geom/point.h>
#include <2geom/interval.h>
#include "livarot/Shape.h"
#include "livarot/Path.h"
#include "livarot/LivarotDefs.h"
#include "livarot/geom.h"

namespace py = pybind11;


PYBIND11_MODULE(_pylivarot, m) {
    m.doc() = "python bindings to the functionality within livarot"; 
    py::module_ m2geom = m.def_submodule("py2geom", "python bindings to the functionality within 2geom");
    m2geom.attr("EPSILON") = &Geom::EPSILON;

    py::class_<Geom::PathVector>(m2geom, "PathVector")
        .def(py::init<>())
        .def("__eq__", [](const Geom::PathVector &s, const Geom::PathVector &other){return (s == other);})
        .def("__iter__", [](const Geom::PathVector &s) { return py::make_iterator(s.begin(), s.end()); },
                         py::keep_alive<0, 1>() /* Essential: keep object alive while iterator exists */)
        .def("__len__", &Geom::PathVector::size)
        .def("__getitem__", [](const Geom::PathVector &s, int index){ return s[index]; })
        .def("push_back", &Geom::PathVector::push_back)
        .def("boundsFast", &Geom::PathVector::boundsFast)
        .def("boundsExact", &Geom::PathVector::boundsExact)
        .def("back", py::overload_cast<>(&Geom::PathVector::back))
        .def("curveCount", &Geom::PathVector::curveCount)
        .def("size", &Geom::PathVector::size)
        .def("reverse", &Geom::PathVector::reverse, py::arg("reverse_paths") = true);

    py::class_<Geom::Path>(m2geom, "Path")
        .def(py::init<>())
        .def("__iter__", [](const Geom::Path &s) { return py::make_iterator(s.begin(), s.end()); },
                         py::keep_alive<0, 1>())
        .def("__eq__", [](const Geom::Path &s, const Geom::Path &other){return (s == other);})
        //.def("__getitem__", [](const Geom::Path &s, int index){ std::unique_ptr<Geom::Curve> out(*s[index]); return out; })
        .def("__getitem__", [](const Geom::Path &s, int index){ return &s[index];})
        .def("__len__", &Geom::Path::size)
        .def("setStitching", &Geom::Path::setStitching)
        .def("start", &Geom::Path::start)
        .def("initialPoint", &Geom::Path::initialPoint)
        .def("boundsFast", &Geom::Path::boundsFast)
        .def("boundsExact", &Geom::Path::boundsExact)
        .def("closed", &Geom::Path::closed);

    py::class_<Geom::PathSink>(m2geom, "PathSink")
        .def("feed", py::overload_cast<Geom::Curve const &, bool>(&Geom::PathSink::feed));
    py::class_<Geom::Rect>(m2geom, "Rect")
        .def(py::init<>())
        .def(py::init<Geom::Interval const &, Geom::Interval const &>())
        .def(py::init<Geom::Coord &, Geom::Coord &, Geom::Coord &, Geom::Coord &>())
        .def(py::init<Geom::Point &, Geom::Point &>())
        .def("height", &Geom::Rect::height)
        .def("width", &Geom::Rect::width)
        .def("top", &Geom::Rect::top)
        .def("bottom", &Geom::Rect::bottom)
        .def("left", &Geom::Rect::left)
        .def("right", &Geom::Rect::right)
        .def("unionWith", [](Geom::Rect &self, Geom::OptRect &other){ self.unionWith(other);})
        .def("unionWith", [](Geom::Rect &self, Geom::Rect &other){ self.unionWith(other);})
	    .def("__getitem__", [](Geom::Rect &self, int i) {return self[i];});
    py::class_<Geom::OptRect>(m2geom, "OptRect")
        .def(py::init<>())
        .def(py::init<Geom::Interval const &, Geom::Interval const &>())
        .def(py::init<Geom::Coord &, Geom::Coord &, Geom::Coord &, Geom::Coord &>())
        .def(py::init<Geom::Point &, Geom::Point &>())
	    .def("__getitem__", [](Geom::OptRect &self, int i) { return self.value()[i]; } )
        .def("unionWith", [](Geom::OptRect &self, Geom::OptRect &other){ self.unionWith(other);})
        .def("unionWith", [](Geom::OptRect &self, Geom::Rect &other){ self.unionWith(other);})
        .def("empty", &Geom::OptRect::empty);

    py::class_<Geom::Point>(m2geom, "Point")
    	.def(py::init<>())
	    .def(py::init<Geom::Coord &, Geom::Coord &>());
    
    m2geom.def("atan2", py::overload_cast<Geom::Point const &>(&Geom::atan2));

    py::class_<Geom::Affine>(m2geom, "Affine")
        .def(py::init<>())
        .def(py::init<Geom::Coord &, Geom::Coord &,Geom::Coord &, Geom::Coord &, Geom::Coord &, Geom::Coord &>())
        .def("__imul__", [](Geom::Affine self, Geom::Translate other){ self *= other; return self;})
        .def("__imul__", [](Geom::Affine self, Geom::Rotate other){ self *= other; return self;})
        .def("expansionX", &Geom::Affine::expansionX)
        .def("expansionY", &Geom::Affine::expansionY);

    py::class_<Geom::Translate>(m2geom, "Translate")
        .def(py::init<>())
        .def(py::init<Geom::Point const &>())
        .def(py::init<Geom::Coord const &, Geom::Coord const &>());
        
    py::class_<Geom::Rotate>(m2geom, "Rotate")
        .def(py::init<>())
        .def(py::init<Geom::Coord const &>())
        .def(py::init<Geom::Point const &>())
        .def(py::init<Geom::Coord const &, Geom::Coord const &>());

    py::class_<Geom::Curve>(m2geom, "Curve")
        .def("__eq__", [](const Geom::Curve &s, const Geom::Curve &other){return (s == other);})
        .def("transform", &Geom::Curve::transform);
    py::class_<Geom::LineSegment, Geom::Curve>(m2geom, "LineSegment")
        .def(py::init<Geom::Point const &, Geom::Point const &>())
        ;
    py::class_<Geom::Path::ClosingSegment, Geom::LineSegment, Geom::Curve>(m2geom, "ClosingSegment");

    py::class_<Geom::QuadraticBezier, Geom::Curve>(m2geom, "QuadraticBezier")
        .def(py::init<Geom::Point const &, Geom::Point const &, Geom::Point const &>());    
    py::class_<Geom::CubicBezier, Geom::Curve>(m2geom, "CubicBezier")
        .def(py::init<Geom::Point const &, Geom::Point const &, Geom::Point const &, Geom::Point const &>());
        

    py::class_<Geom::Interval>(m2geom, "Interval")
    	.def("max", &Geom::Interval::max)
	    .def("min", &Geom::Interval::min);

    py::class_<Geom::PathBuilder, Geom::PathSink>(m2geom, "PathBuilder")
        .def(py::init<>())
        .def("flush", &Geom::PathBuilder::flush)
        .def("moveTo", &Geom::PathBuilder::moveTo)
        .def("arcTo", &Geom::PathBuilder::arcTo)
        .def("lineTo", &Geom::PathBuilder::lineTo)
        .def("quadTo", &Geom::PathBuilder::quadTo)
        .def("curveTo", &Geom::PathBuilder::curveTo)
        .def("closePath", &Geom::PathBuilder::closePath)
        .def("peek", &Geom::PathBuilder::peek);
    py::class_<Geom::SVGPathParser>(m2geom, "SVGPathParser")
        .def(py::init<Geom::PathSink &>())
        .def("setZSnapThreshold", &Geom::SVGPathParser::setZSnapThreshold)
        .def("feed",  py::overload_cast<std::string const &>(&Geom::SVGPathParser::feed))
        .def("parse", py::overload_cast<std::string const &>(&Geom::SVGPathParser::parse));
    py::class_<Geom::SVGPathWriter, Geom::PathSink>(m2geom, "SVGPathWriter")
        .def(py::init<>())
        .def("str", &Geom::SVGPathWriter::str);
    py::enum_<Geom::Dim2>(m2geom, "Dim2")
	   .value("X", Geom::Dim2::X)
	   .value("Y", Geom::Dim2::Y)
	   .export_values();


    m2geom.def("write_svg_path", &Geom::write_svg_path, py::arg("pv"), py::arg("prec")=-1, py::arg("optimize")=false, 
                py::arg("shorthands")=true);    

    m2geom.def("parse_svg_path", py::overload_cast<char const *>(&Geom::parse_svg_path));

    m2geom.def("distance", py::overload_cast<Geom::Point const &, Geom::Point const &>(&Geom::distance));

    py::enum_<butt_typ>(m, "ButtType")
        .value("butt_straight", butt_typ::butt_straight)
        .value("butt_square", butt_typ::butt_square)
        .value("butt_round", butt_typ::butt_round)
        .value("butt_pointy", butt_typ::butt_pointy)
        .export_values();

    py::enum_<join_typ>(m, "JoinType")
        .value("join_straight", join_typ::join_straight)
        .value("join_round", join_typ::join_round)
        .value("join_pointy", join_typ::join_pointy)
        .export_values();

    py::enum_<FillRule>(m, "FillRule")
	    .value("fill_oddEven", FillRule::fill_oddEven)
	    .value("fill_nonZero", FillRule::fill_nonZero)
	    .value("fill_positive", FillRule::fill_positive)
	    .value("fill_justDont", FillRule::fill_justDont)
	    .export_values();

    py::class_<Shape>(m, "Shape")
        .def(py::init<>())
        .def("getPoint", &Shape::getPoint)
        .def("hasBackData", &Shape::hasBackData)
        .def("ConvertToShape", &Shape::ConvertToShape, py::arg("a"), py::arg("directed") = fill_nonZero, py::arg("invert")=false)
        .def("getEdge", &Shape::getEdge)
        .def("Booleen", &Shape::Booleen, py::arg("a"), py::arg("b"), py::arg("mod"), py::arg("cutPathID") = -1 )
        .def("ConvertToForme", py::overload_cast<Path *>(&Shape::ConvertToForme))
		//.def("ConvertToForme", [](Shape self, Path* dest, int& nbP, Path** orig, bool& splitWhenForced){self.ConvertToForme(dest, nbP, orig, splitWhenForced);});
        .def("ConvertToForme", py::overload_cast<Path *, int, std::vector<Path> *, bool>(&Shape::ConvertToForme), py::arg("dest"), py::arg("nbP"), py::arg("orig"), py::arg("splitWhenForced") = false);

    py::class_<Path>(m, "Path")
        .def(py::init<>())
        .def("LoadPathVector", py::overload_cast<Geom::PathVector const &>(&Path::LoadPathVector))
        .def("ConvertWithBackData", &Path::ConvertWithBackData)
        .def("SetBackData", &Path::SetBackData)
        .def("Outline", &Path::Outline)
        .def("OutsideOutline", &Path::OutsideOutline)
        .def("Simplify", &Path::Simplify)
        .def("MakePathVector", &Path::MakePathVector)
        .def("svg_dump_path", &Path::svg_dump_path)
        .def("Transform", &Path::Transform)
        .def("Fill", &Path::Fill, py::arg("dest")=static_cast<Shape *>(nullptr), py::arg("pathID")=-1, py::arg("justAdd")=false, 
                py::arg("closeIfNeeded")=true, py::arg("invert")=false);

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
