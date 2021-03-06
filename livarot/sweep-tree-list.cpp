// SPDX-License-Identifier: GPL-2.0-or-later
/** @file
 * TODO: insert short description here
 *//*
 * Authors: see git history
 *
 * Copyright (C) 2018 Authors
 * Released under GNU GPL v2+, read the file 'COPYING' for more information.
 */
#include "sweep-tree.h"
#include "sweep-tree-list.h"


SweepTreeList::SweepTreeList(int s) :
    nbTree(0),
    maxTree(s),
    trees((SweepTree *) malloc(s * sizeof(SweepTree))),
    racine(nullptr)
{
    /* FIXME: Use new[] for trees initializer above, but watch out for bad things happening when
     * SweepTree::~SweepTree is called.
     */
}


SweepTreeList::~SweepTreeList()
{
    free(trees);
    trees = nullptr;
}


SweepTree *SweepTreeList::add(Shape *iSrc, int iBord, int iWeight, int iStartPoint, Shape */*iDst*/)
{
    if (nbTree >= maxTree) {
        return nullptr;
    }

    int const n = nbTree++;
    trees[n].MakeNew(iSrc, iBord, iWeight, iStartPoint);

    return trees + n;
}


/*
  Local Variables:
  mode:c++
  c-file-style:"stroustrup"
  c-file-offsets:((innamespace . 0)(inline-open . 0)(case-label . +))
  indent-tabs-mode:nil
  fill-column:99
  End:
*/
// vim: filetype=cpp:expandtab:shiftwidth=4:tabstop=8:softtabstop=4:fileencoding=utf-8:textwidth=99 :
