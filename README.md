Python 3 bindings to the inkscape libraries lib2geom and livarot.

Installation
------------

manylinux whls have been published to pypi, there's likely a whl for your distro/python version at:

```bash
pip install pylivarot
```

On windows, 

```bash
python3 setup.py bdist_wheel
```

should work in theory, but I currently have not gotten this working (boost is not configured right)

Usage
-----

Declaring Path Vectors:

```python
from pylivarot import py2geom

# using a path builder
_path_builder = py2geom.PathBuilder()
_path_builder.moveTo(py2geom.Point(0, 0))
_path_builder.lineTo(py2geom.Point(10, 20))
_path_builder.quadTo(py2geom.Point(10, 20), py2geom.Point(20, 50))
_path_builder.curveTo(py2geom.Point(10, 20), py2geom.Point(20, 50), py2geom.Point(40, 80))        
_path_builder.flush()
result = _path_builder.peek()

# using an SVG d string
diagonal_line = "M 0,0 L 3,3 z"
pv_diagonal_line = py2geom.parse_svg_path(diagonal_line) 
```

Format an SVG d string:

```python
from pylivarot import py2geom

pv = py2geom.PathVector()
target_d = py2geom.write_svg_path(pv)
```

Apply a transform:

```python
from pylivarot import py2geom

path_d =  "M 0,0 L 0,2 L 2,2 L 2,0 z"
pv_path = py2geom.parse_svg_path(path_d)
_affine = py2geom.Affine()
_affine *= py2geom.Translate(py2geom.Point(2, 4))
_affine *= py2geom.Rotate(3.14159/4.0) 
for _path in pv_path:
    for _curve in _path:
        _curve.transform(_affine)
```

Boolean operations

```python
from pylivarot import py2geom, union, intersection, difference

path_v_a = py2geom.parse_svg_path("M 0,0 L 0,2 L 2,2 L 2,0 z")
path_v_b = py2geom.parse_svg_path("M 0.5,0.5 L 0.5,1.5 L 1.5,1.5 L 1.5,0.5 z")

union_pv = union(path_v_a, path_v_b)
inters_pv = intersection(path_v_a, path_v_b)
diff_pv = difference(path_v_a, path_v_b)
```

Path Vector Bounding box (also works on Paths)

```python
from pylivarot import py2geom

opt_bbox = path_vector.boundsExact() # or pv.boundsFast()
bbox = py2geom.Rect(opt_bbox[py2geom.Dim2.X], opt_bbox[py2geom.Dim2.Y])
print(bbox.left(), bbox.right(), bbox.top(), bbox.bottom(), bbox.width(), bbox.height())
```

Inkscape's get_outline and get_outline_offset functionality

```python
from pylivarot import py2geom, get_outline, get_outline_offset

outline = get_outline(path_vector)
outline_offset = get_outline_offset(path_vector, stroke_width)
```