import sys
from os.path import dirname
sys.path.append(dirname(__file__))

#mport _pylivarot.py2geom as py2geom
from _pylivarot import *

def Path_for_pathvector(epathv):
    """
    convert py2geom.PathVector to LivarotPath
    """
    dest = Path()
    dest.LoadPathVector(epathv)
    return dest

def get_threshold(path, threshold):
    box = path.boundsFast()
    if not box or box.empty():
        return threshold
    diagonal = py2geom.distance(py2geom.Point(box[py2geom.X].min(), box[py2geom.Y].min()),
     py2geom.Point(box[py2geom.X].max(), box[py2geom.Y].max()))
    return threshold * diagonal/ 100 


def sp_pathvector_boolop(pathva, pathvb, bop, fra, frb, skip_conversion=False):
    """
    do the boolean operation between pathva and pathvb. The syntax is the same as the code in the inkscape path code
    """
    # extract the livarot Paths from the source objects
    # also get the winding rule specified in the style    
    origWind = [fra, frb]
    # Livarot's outline of arcs is broken. So convert the path to linear and cubics only, for which the outline is created correctly.
    if skip_conversion:
        originaux = [Path_for_pathvector(pathva), Path_for_pathvector(pathvb)]
    else:
        originaux = [Path_for_pathvector(pathv_to_linear_and_cubic_beziers(pathva)), Path_for_pathvector(pathv_to_linear_and_cubic_beziers(pathvb))]
    # some temporary instances, first
    theShapeA = Shape()
    theShapeB = Shape()
    theShape = Shape()
    res = Path()
    res.SetBackData(False)
    toCut = None
    nbToCut = 0
    if bop == bool_op.bool_op_inters or bop == bool_op.bool_op_union or bop == bool_op.bool_op_diff or bop == bool_op.bool_op_symdiff:
        # get the polygons of each path, with the winding rule specified, and apply the operation iteratively
        originaux[0].ConvertWithBackData(get_threshold(pathva, 0.1))

        originaux[0].Fill(theShape, 0)

        theShapeA.ConvertToShape(theShape, origWind[0])

        originaux[1].ConvertWithBackData(get_threshold(pathvb, 0.1))

        originaux[1].Fill(theShape, 1)

        theShapeB.ConvertToShape(theShape, origWind[1])
        theShape.Booleen(theShapeB, theShapeA, bop)
    elif bop == bool_op.bool_op_cut:
        # cuts= sort of a bastard boolean operation, thus not the axact same modus operandi
        # technically, the cut path is not necessarily a polygon (thus has no winding rule)
        # it is just uncrossed, and cleaned from duplicate edges and points
        # then it's fed to Booleen() which will uncross it against the other path
        # then comes the trick: each edge of the cut path is duplicated (one in each direction),
        # thus making a polygon. the weight of the edges of the cut are all 0, but
        # the Booleen need to invert the ones inside the source polygon (for the subsequent
        # ConvertToForme)

        # the cut path needs to have the highest pathID in the back data
        # that's how the Booleen() function knows it's an edge of the cut
        originaux.reverse()
        origWind.reverse()
        originaux[0].ConvertWithBackData(get_threshold(pathva, 0.1))

        originaux[0].Fill(theShape, 0)

        theShapeA.ConvertToShape(theShape, origWind[0])
        originaux[1].ConvertWithBackData(get_threshold(pathvb, 0.1))

        originaux[1].Fill(theShape, 1,False, False, False) # do not closeIfNeeded

        theShapeB.ConvertToShape(theShape, FillRule.fill_justDont) # fill_justDont doesn't computes winding numbers

        # the elements arrive in reverse order in the list
        theShape.Booleen(theShapeB, theShapeA, bool_op.bool_op_cut, 1)
    elif bop == bool_op.bool_op_slice:
        # slice is not really a boolean operation
        # you just put the 2 shapes in a single polygon, uncross it
        # the points where the degree is > 2 are intersections
        # just check it's an intersection on the path you want to cut, and keep it
        # the intersections you have found are then fed to ConvertPositionsToMoveTo() which will
        # make new subpath at each one of these positions
        # reverse for the operation
        originaux.reverse()
        origWind.reverse()
        originaux[0].ConvertWithBackData(get_threshold(pathva, 0.1));

        originaux[0].Fill(theShapeA, 0, False, False, False) # don't closeIfNeeded

        originaux[1].ConvertWithBackData(get_threshold(pathvb, 0.1))

        originaux[1].Fill(theShapeA, 1, True, False, False) # don't closeIfNeeded and just dump in the shape, don't reset it

        theShape.ConvertToShape(theShapeA, FillRule.fill_justDont)
        if theShape.hasBackData():
            # should always be the case, but ya never know
            
            for i in range(theShape.numberOfPoints()):
                if theShape.getPoint(i).totalDegree() > 2 :
                    # possibly an intersection
                    # we need to check that at least one edge from the source path is incident to it
                    # before we declare it's an intersection
                    cb = theShape.getPoint(i).incidentEdge[FirstOrLast.FIRST]
                    nbOrig=0
                    nbOther=0
                    piece=-1
                    t=0.0
                    while cb >= 0 and cb < theShape.numberOfEdges():
                        if theShape.ebData[cb].pathID == 0:
                            # the source has an edge incident to the point, get its position on the path
                            piece=theShape.ebData[cb].pieceID
                            if theShape.getEdge(cb).st == i:
                                t=theShape.ebData[cb].tSt
                            else:
                                t=theShape.ebData[cb].tEn
                            nbOrig+=1
                        
                        if theShape.ebData[cb].pathID == 1:
                            nbOther+=1 # the cut is incident to this point
                        cb=theShape.NextAt(i, cb)
                    if nbOrig > 0 and nbOther > 0:
                        # point incident to both path and cut: an intersection
                        # note that you only keep one position on the source; you could have degenerate
                        # cases where the source crosses itself at this point, and you wouyld miss an intersection
                        # toCut=(Path::cut_position*)realloc(toCut, (nbToCut+1)*sizeof(Path::cut_position));
                        cut = cut_position()
                        cut.piece = piece
                        cut.t = t
                        toCut.append(cut)
    nbNest = 0
    conts = None
    nesting = None
    nbOriginaux = 2
    # to compensate for the previous swap
    if bop == bool_op.bool_op_slice:
        res.Copy(originaux[0])
        res.ConvertPositionsToMoveTo(nbToCut, toCut) # cut where you found intersections
    elif bop == bool_op.bool_op_cut: 
        # this function uses the point_data to get the winding number of each path (ie: is a hole or not)
        # for later reconstruction in objects, you also need to extract which path is parent of holes (nesting info)
        theShape.ConvertToFormeNested(res, nbOriginaux, originaux, 1, nbNest, nesting, conts)
    else:
        theShape.ConvertToForme(res, nbOriginaux, originaux)

    return res.MakePathVector()


def union(path_vector_a, path_vector_b):
    return sp_pathvector_boolop(path_vector_a, path_vector_b, bool_op.bool_op_union, FillRule.fill_oddEven, FillRule.fill_oddEven)


def intersection(path_vector_a, path_vector_b):
    return sp_pathvector_boolop(path_vector_a, path_vector_b, bool_op.bool_op_inters, FillRule.fill_oddEven, FillRule.fill_oddEven)


def difference(path_vector_a, path_vector_b):
    return sp_pathvector_boolop(path_vector_a, path_vector_b, bool_op.bool_op_diff, FillRule.fill_oddEven, FillRule.fill_oddEven)


def get_outline_offset(pathva, stroke_width):
    orig = Path()
    orig.LoadPathVector(pathva)
    res = Path()
    res.SetBackData(False)
    butt = ButtType.butt_straight
    join = JoinType.join_straight
    orig.OutsideOutline(res, stroke_width, join, butt, 20.0)
    if stroke_width >= 1:
        res.ConvertWithBackData(1.0)
    else:
        res.ConvertWithBackData(stroke_width)
    theShape = Shape()
    theRes = Shape()
    res.Fill(theShape, 0)
    theRes.ConvertToForme(orig, 1, [res])
    # skipping the coalesce 
    res_d = orig.svg_dump_path()
    return py2geom.parse_svg_path(res_d)


def get_outline(pathva, stroke_width):
    bbox_only = False
    pathv = pathv_to_linear_and_cubic_beziers( pathva )
    if stroke_width < py2geom.EPSILON:
        # https://bugs.launchpad.net/inkscape/+bug/1244861
        stroke_width = py2geom.EPSILON
    
    butt = ButtType.butt_straight
    join = JoinType.join_straight
    miter = stroke_width
    '''
    double miter = style->stroke_miterlimit.value * stroke_width;

    JoinType join;
    switch (style->stroke_linejoin.computed) {
        case SP_STROKE_LINEJOIN_MITER:
            join = join_pointy;
            break;
        case SP_STROKE_LINEJOIN_ROUND:
            join = join_round;
            break;
        default:
            join = join_straight;
            break;
    }
    switch (style->stroke_linecap.computed) {
        case SP_STROKE_LINECAP_SQUARE:
            butt = butt_square;
            break;
        case SP_STROKE_LINECAP_ROUND:
            butt = butt_round;
            break;
        default:
            butt = butt_straight;
            break;
    }
    '''
    origin = Path() # Fill
    offset = Path()

    '''
    Geom::Affine const transform(item->transform);
    double const scale = transform.descrim();
    '''

    origin.LoadPathVector(pathv)
    offset.SetBackData(False)

    '''
    if (!style->stroke_dasharray.values.empty()) {
        // We have dashes!
        origin->ConvertWithBackData(0.005); // Approximate by polyline
        origin->DashPolylineFromStyle(style, scale, 0);
        auto bounds = Geom::bounds_fast(pathv);
        if (bounds) {
            double size = Geom::L2(bounds->dimensions());
            origin->Simplify(size * 0.000005); // Polylines to Beziers
        }
    }
    '''

    # Finally do offset!
    origin.Outline(offset, 0.5 * stroke_width, join, butt, 0.5 * miter);

    if bbox_only:
        stroke = offset.MakePathVector()
    else:
        # Clean-up shape

        offset.ConvertWithBackData(1.0) # Approximate by polyline

        theShape  = Shape();
        offset.Fill(theShape, 0) # Convert polyline to shape, step 1.

        theOffset = Shape()
        theOffset.ConvertToShape(theShape, FillRule.fill_positive) # Create an intersection free polygon (theOffset), step2.
        theOffset.ConvertToForme(origin, 1, [offset]) # Turn shape into contour (stored in origin).

        stroke = origin.MakePathVector() #  Note origin was replaced above by stroke!
    
    return stroke