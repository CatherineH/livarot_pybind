#include <pybind11/pybind11.h>
#include <2geom/svg-path-writer.h>
#include <path/path-boolop.h>
#include <svg/svg.h>

namespace py = pybind11;


PYBIND11_MODULE(livarot, m) {
    m.doc() = "python bindings to the functionality within livarot, with some helper classes from 2geom and inkscape"; 
    py::_class<Geom::PathVector>(m, "PathVector");
    m.def("sp_svg_read_pathv", sp_svg_read_pathv);
}