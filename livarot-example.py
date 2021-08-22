import livarot

d_string = "M 140.60714,82.398807 112.12372,76.862861 91.415657,97.188406 87.878796,68.388367 62.14891,54.974767 88.446424,42.71131 93.252544,14.095704 113.04216,35.31651 141.74239,31.044693 127.67554,56.423329 Z"
full_path =  f'''<path
       style="fill:#cd87de;stroke:#000000;stroke-width:1"
       id="path10"
       d="{d_string}"
/>'''

svg_parser = livarot.SVGPathParser(livarot.PathBuilder())
svg_parser.setZSnapThreshold(Geom::EPSILON);
path_vector = svg_parser.parse(d_string)
