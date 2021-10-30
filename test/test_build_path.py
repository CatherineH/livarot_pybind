from pylivarot import py2geom

class TestPathBoolop:
    def test_move_to(self):
        _path_builder = py2geom.PathBuilder()
        _path_builder.moveTo(py2geom.Point(10, 20))
        _path_builder.flush()
        result = _path_builder.peek()
        output_path = py2geom.write_svg_path(result)
        assert output_path == "M 10 20"
    
    def test_line_to(self):
        _path_builder = py2geom.PathBuilder()
        _path_builder.lineTo(py2geom.Point(10, 20))
        _path_builder.flush()
        result = _path_builder.peek()
        output_path = py2geom.write_svg_path(result)
        assert output_path == "M 0 0 L 10 20"
    
    def test_quad_to(self):
        _path_builder = py2geom.PathBuilder()
        _path_builder.quadTo(py2geom.Point(10, 20), py2geom.Point(20, 50))
        _path_builder.flush()
        result = _path_builder.peek()
        output_path = py2geom.write_svg_path(result)
        assert output_path == "M 0 0 Q 10 20 20 50"

    def test_curve_to(self):
        _path_builder = py2geom.PathBuilder()
        _path_builder.curveTo(py2geom.Point(10, 20), py2geom.Point(20, 50), py2geom.Point(40, 80))
        _path_builder.flush()
        result = _path_builder.peek()
        output_path = py2geom.write_svg_path(result)
        assert output_path == "M 0 0 C 10 20 20 50 40 80"
    