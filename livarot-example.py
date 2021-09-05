import sys
from os.path import dirname, join
sys.path.append(join(dirname(__file__), "linux-build"))

import pylivarot as livarot

shape = livarot.Shape()
d_string = "M 140.60714,82.398807 112.12372,76.862861 91.415657,97.188406 87.878796,68.388367 62.14891,54.974767 88.446424,42.71131 93.252544,14.095704 113.04216,35.31651 141.74239,31.044693 127.67554,56.423329 Z"
#d_string = "M 0,0 L 0,2 L 2,2 L 2,0 z"

path_vector = livarot.parse_svg_path(d_string)
print(path_vector)
my_path = livarot.Path()
my_path.LoadPathVector(path_vector)

