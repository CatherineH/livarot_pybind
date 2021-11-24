from pylivarot import py2geom
import pytest


class TestPath:
    @pytest.mark.skip(reason="segfaults on curve deallocation")
    def test_iterate(self):
        path_to_simplify = "M 0,0 L 0,1.5 L 0,2 L 0,2.5 L 0,3 L 0,3.5 z"
        pv_path = py2geom.parse_svg_path(path_to_simplify)
        """         print(len(pv_path))
        print(len(pv_path[0]))
        for i, path in enumerate(pv_path):
            for j,curve in enumerate(path):
                print(i, j, curve )"""
        print(pv_path[0][0])
        assert pv_path[0][0] == py2geom.LineSegment(py2geom.Point(0,0), py2geom.Point(0,1.5))

if __name__ == "__main__":
    TestPath().test_iterate()