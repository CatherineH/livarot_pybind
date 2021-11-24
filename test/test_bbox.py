from pylivarot import Path, py2geom
#from py2geom import SVGPathParser, parse_svg_path, write_svg_path

class TestBBox:
    def test_get_bounds(self):
        path_to_bounds =  "M 0,0 L 0,2 L 2,2 L 2,0 z"
        pv_path = py2geom.parse_svg_path(path_to_bounds)
        bounds = pv_path.boundsFast()
        assert bounds[py2geom.Dim2.X].min() == 0
        assert bounds[py2geom.Dim2.X].max() == 2
        assert bounds[py2geom.Dim2.Y].min() == 0
        assert bounds[py2geom.Dim2.Y].max() == 2

    def test_bounds_union(self):
        path_to_bounds_left =  "M 0,0 L 0,2 L 2,2 L 2,0 z"
        path_to_bounds_right =  "M 2,0 L 2,2 L 4,2 L 4,0 z"
        pv_path = py2geom.parse_svg_path(path_to_bounds_left)
        pv_path_right = py2geom.parse_svg_path(path_to_bounds_right)

        bounds = pv_path.boundsFast()
        bounds_right = pv_path_right.boundsFast()
        bounds.unionWith(bounds_right)
        assert bounds[py2geom.Dim2.X].min() == 0
        assert bounds[py2geom.Dim2.X].max() == 4
        assert bounds[py2geom.Dim2.Y].min() == 0
        assert bounds[py2geom.Dim2.Y].max() == 2


    def test_bounds_union_rect(self):
        py_rect = py2geom.Rect()
        path_to_bounds_left =  "M 0,0 L 0,2 L 4,2 L 4,0 z"
        pv_path = py2geom.parse_svg_path(path_to_bounds_left)

        bounds = pv_path.boundsFast()
        assert py_rect.width() == 0
        assert py_rect.height() == 0        
        py_rect.unionWith(bounds)
        assert py_rect.width() == 4
        assert py_rect.height() == 2

    def test_rotate_bounds(self):
        path_to_bounds =  "M 0,0 L 0,2 L 2,2 L 2,0 z"
        pv_path = py2geom.parse_svg_path(path_to_bounds)
        _affine = py2geom.Affine()
        _affine *= py2geom.Rotate(3.14159/4.0) 
        for _path in pv_path:
            for _curve in _path:
                _curve.transform(_affine)
        bounds = pv_path.boundsFast()
        assert abs(bounds[py2geom.Dim2.X].min() + 1.4142126241871151) < 0.1
        assert abs(bounds[py2geom.Dim2.X].max() - 1.4142126241871151) < 0.1
        assert bounds[py2geom.Dim2.Y].min() == 0
        assert abs(bounds[py2geom.Dim2.Y].max() - 2.8284271247455677) < 0.1

    def test_translate_bounds(self):
        path_to_bounds =  "M 0,0 L 0,2 L 2,2 L 2,0 z"
        pv_path = py2geom.parse_svg_path(path_to_bounds)
        _affine = py2geom.Affine()
        _affine *= py2geom.Translate(2, 0) 
        for _path in pv_path:
            for _curve in _path:
                _curve.transform(_affine)
        bounds = pv_path.boundsFast()
        assert bounds[py2geom.Dim2.X].min() == 2
        assert bounds[py2geom.Dim2.X].max() == 4
        assert bounds[py2geom.Dim2.Y].min() == 0
        assert bounds[py2geom.Dim2.Y].max() == 2

    def test_convert_opt_rect(self):
        opt_rect = py2geom.OptRect(py2geom.Point(1.0, 1.0), py2geom.Point(2.4, 3.2))
        rect = py2geom.Rect(opt_rect[py2geom.Dim2.X], opt_rect[py2geom.Dim2.Y])
        assert rect.height() == 2.2
        assert rect.width() == 1.4

    def test_opt_rect_empty(self):
        opt_rect = py2geom.OptRect()
        assert opt_rect.empty()

    


if __name__ == "__main__":
    TestBBox().test_get_bounds()