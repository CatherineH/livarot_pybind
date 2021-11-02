from pylivarot import py2geom, Path


class TestSimplifyPath:
    def test_simplify(self):
        path_to_simplify = "M 0,0 L 0,1.5 L 0,2 L 0,2.5 L 0,3 L 0,3.5 z"
        pv_path = py2geom.parse_svg_path(path_to_simplify)
        _path = Path()
        _path.LoadPathVector(pv_path)
        _path.Simplify(0.1)
        result_d = py2geom.write_svg_path(_path.MakePathVector())
        assert result_d == "M 0 0 V 1.5 V 2 V 2.5 V 3 V 3.5 z"
