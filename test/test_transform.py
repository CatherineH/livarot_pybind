from pylivarot import Path, py2geom
#from py2geom import SVGPathParser, parse_svg_path, write_svg_path

class TestTransform:
    def test_matrix_transform(self):
        path_to_transform =  "M 0,0 L 0,2 L 2,2 L 2,0 z"
        pv_path = py2geom.parse_svg_path(path_to_transform)
        _path = Path()
        _path.LoadPathVector(pv_path)
        _path.Transform(py2geom.Affine(3, 1, -1, 3, 30, 40))
        result_d = py2geom.write_svg_path(_path.MakePathVector())
        assert result_d == "M 30 40 L 28 46 L 34 48 L 36 42 z"

    def test_path_vector_transform(self):
        path_to_transform =  "M 0,0 L 0,2 L 2,2 L 2,0 z"
        pv_path = py2geom.parse_svg_path(path_to_transform)
        transform = py2geom.Affine(3, 1, -1, 3, 30, 40)
        for _path in pv_path:
            for _curve in _path:
                _curve.transform(transform)
        result_d = py2geom.write_svg_path(pv_path)
        assert result_d == "M 30 40 L 28 46 L 34 48 L 36 42 z"

    def test_path_vector_transform(self):
        path_to_transform =  "M 2,0 L 2,2 L 4,2 L 4,0 z"
        pv_path = py2geom.parse_svg_path(path_to_transform)
        transform = py2geom.Affine()
        transform *= py2geom.Translate(10, 0)
        transform *= py2geom.Translate(10, 0)
        for _path in pv_path:
            for _curve in _path:
                _curve.transform(transform)
        result_d = py2geom.write_svg_path(pv_path)
        assert result_d == "M 22 0 V 2 H 24 V 0 z"