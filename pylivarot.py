import _pylivarot.py2geom as py2geom
from _pylivarot import Path, pathv_to_linear_and_cubic_beziers, Shape, bool_op

def Path_for_pathvector(epathv):
    """
    convert py2geom.PathVector to LivarotPath
    """
    dest = Path()
    dest.LoadPathVector(epathv)
    return dest

def get_threshold(path, threshold):
    box = path.boundsFast()
    if not box:
        return threshold
    diagonal = py2geom.distance(py2geom.Point(box[py2geom.X].min(), box[py2geom.Y].min()),
     py2geom.Point(box[py2geom.X].max(), py2geom.Point(box[py2geom.Y].max())))
    return threshold * diagonal/ 100 


def sp_pathvector_boolop(pathva, pathvb, bop, fra, frb):
    """
    do the boolean operation between pathva and pathvb. The syntax is the same as the code in the inkscape path code
    """
    # extract the livarot Paths from the source objects
    # also get the winding rule specified in the style    
    origWind = [fra, frb]
    # Livarot's outline of arcs is broken. So convert the path to linear and cubics only, for which the outline is created correctly.
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
        originaux[0].ConvertWithBackData(get_threshold(pathva, 0.1));

        originaux[0].Fill(theShape, 0);

        theShapeA.ConvertToShape(theShape, origWind[0]);

        originaux[1].ConvertWithBackData(get_threshold(pathvb, 0.1));

        originaux[1].Fill(theShape, 1);

        theShapeB.ConvertToShape(theShape, origWind[1]);
        
        theShape.Booleen(theShapeB, theShapeA, bop);
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

        theShapeB.ConvertToShape(theShape, fill_justDont) # fill_justDont doesn't computes winding numbers

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

        theShape.ConvertToShape(theShapeA, fill_justDont)
        if theShape.hasBackData():
            # should always be the case, but ya never know
            
            for i in range(theShape.numberOfPoints()):
                if theShape.getPoint(i).totalDegree() > 2 :
                    # possibly an intersection
                    # we need to check that at least one edge from the source path is incident to it
                    # before we declare it's an intersection
                    cb = theShape.getPoint(i).incidentEdge[FIRST]
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
"""
Geom::PathVector 
sp_pathvector_boolop(Geom::PathVector const &pathva, Geom::PathVector const &pathvb, bool_op bop, fill_typ fra, fill_typ frb)
{        

    int*    nesting=nullptr;
    int*    conts=nullptr;
    int     nbNest=0;
    // pour compenser le swap juste avant
    if ( bop == bool_op_slice ) {
//    theShape->ConvertToForme(res, nbOriginaux, originaux, true);
//    res->ConvertForcedToMoveTo();
        res->Copy(originaux[0]);
        res->ConvertPositionsToMoveTo(nbToCut, toCut); // cut where you found intersections
        free(toCut);
    } else if ( bop == bool_op_cut ) {
        // il faut appeler pour desallouer PointData (pas vital, mais bon)
        // the Booleen() function did not deallocate the point_data array in theShape, because this
        // function needs it.
        // this function uses the point_data to get the winding number of each path (ie: is a hole or not)
        // for later reconstruction in objects, you also need to extract which path is parent of holes (nesting info)
        theShape->ConvertToFormeNested(res, nbOriginaux, &originaux[0], 1, nbNest, nesting, conts);
    } else {
        theShape->ConvertToForme(res, nbOriginaux, &originaux[0]);
    }

    delete theShape;
    delete theShapeA;
    delete theShapeB;
    delete originaux[0];
    delete originaux[1];

    gchar *result_str = res->svg_dump_path();
    Geom::PathVector outres =  Geom::parse_svg_path(result_str);
    g_free(result_str);

    delete res;
    return outres;
}
"""