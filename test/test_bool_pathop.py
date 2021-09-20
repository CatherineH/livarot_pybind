from pylivarot import sp_pathvector_boolop, bool_op, FillRule
import pylivarot.py2geom as py2geom
from py2geom import SVGPathParser, parse_svg_path, write_svg_path

class TestPathBoolop:
    def __init__(self) -> None:
        self.rectangle_bigger =  "M 0,0 L 0,2 L 2,2 L 2,0 z"
        self.rectangle_smaller = "M 0.5,0.5 L 0.5,1.5 L 1.5,1.5 L 1.5,0.5 z"
        rectangle_outside =  "M 0,1.5 L 0.5,1.5 L 0.5,2.5 L 0,2.5 z"
        rectangle_outside_union = "M 0,0 L 0,1.5 L 0,2 L 0,2.5 L 0.5,2.5 L 0.5,2 L 2,2 L 2,0 L 0,0 z"
        self.pvRectangleBigger = parse_svg_path(self.rectangle_bigger)
        self.pvRectangleSmaller = parse_svg_path(self.rectangle_smaller)
        self.pvRectangleOutside = parse_svg_path(rectangle_outside)
        self.pvTargetUnion = parse_svg_path(rectangle_outside_union)
        self.pvEmpty = parse_svg_path("") 

    def compare_paths(result, target):
        result_d = write_svg_path(result)
        target_d = write_svg_path(target)
        assert result_d == target_d

    def test_union_outside(self):
        # test that the union of two objects where one is outside the other results in a new larger shape
        pvRectangleUnion  = sp_pathvector_boolop(self.pvRectangleBigger, self.pvRectangleOutside, bool_op.bool_op_union, FillRule.fill_oddEven, FillRule.fill_oddEven)
        self.compare_paths(pvRectangleUnion, self.pvTargetUnion)

    def test_union_outside_swap(self):
        # test that the union of two objects where one is outside the other results in a new larger shape, even when the order is reversed
        pvRectangleUnion  = sp_pathvector_boolop(self.pvRectangleOutside, self.pvRectangleBigger, bool_op.bool_op_union, FillRule.fill_oddEven, FillRule.fill_oddEven)
        self.compare_paths(pvRectangleUnion, self.pvTargetUnion)

    def test_union_inside_swap(self):
        # test that the union of two objects where one is completely inside the other is the larger shape, even when the order is swapped
        pvRectangleUnion  = sp_pathvector_boolop(self.pvRectangleSmaller, self.pvRectangleBigger, bool_op.bool_op_union, FillRule.fill_oddEven, FillRule.fill_oddEven)
        self.compare_paths(pvRectangleUnion, self.pvRectangleBigger)

    def test_intersection_inside(self):
        # test that the intersection of two objects where one is completely inside the other is the smaller shape
        pvRectangleIntersection  = sp_pathvector_boolop(self.pvRectangleBigger, self.pvRectangleSmaller, bool_op.bool_op_inters, FillRule.fill_oddEven, FillRule.fill_oddEven)
        self.compare_paths(pvRectangleIntersection, self.pvRectangleSmaller)    

    def test_difference_inside(self):
        # test that the difference of two objects where one is completely inside the other is an empty path
        pvRectangleDifference  = sp_pathvector_boolop(self.pvRectangleBigger, self.pvRectangleSmaller, bool_op.bool_op_diff, FillRule.fill_oddEven, FillRule.fill_oddEven)
        self.compare_paths(pvRectangleDifference, self.pvEmpty)

    def test_difference_outside(self):
        # test that the difference of two objects where one is completely outside the other is multiple shapes
        pvRectangleDifference = sp_pathvector_boolop(self.pvRectangleSmaller, self.pvRectangleBigger, bool_op.bool_op_diff, FillRule.fill_oddEven, FillRule.fill_oddEven)
        pvRectangleSmallerReversed = self.pvRectangleSmaller
        pvBothPaths = self.pvRectangleBigger
        pvRectangleSmallerReversed.reverse()
        for _path in pvRectangleSmallerReversed:
            pvBothPaths.push_back(_path)
        self.compare_paths(pvRectangleDifference, pvBothPaths);
