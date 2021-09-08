// SPDX-License-Identifier: GPL-2.0-or-later
/** @file
 * TODO: insert short description here
 *//*
 * Authors: see git history
 *
 * Copyright (C) 2018 Authors
 * Released under GNU GPL v2+, read the file 'COPYING' for more information.
 */
#include "stringstream.h"
#include <2geom/point.h>
#include <glib.h>

std::string
strip_trailing_zeros(std::string str)
{
    std::string::size_type p_ix = str.find('.');
    if (p_ix != std::string::npos) {
        std::string::size_type e_ix = str.find('e', p_ix);
        /* N.B. In some contexts (e.g. CSS) it is an error for a number to contain `e'.  fixme:
         * Default to avoiding `e', e.g. using sprintf(str, "%17f", d).  Add a new function that
         * allows use of `e' and use that function only where the spec allows it.
         */
        std::string::size_type nz_ix = str.find_last_not_of('0', (e_ix == std::string::npos
                                                                  ? e_ix
                                                                  : e_ix - 1));
        if (nz_ix == std::string::npos || nz_ix < p_ix || nz_ix >= e_ix) {
            g_error("have `.' but couldn't find non-0");
        } else {
            str.erase(str.begin() + (nz_ix == p_ix
                                     ? p_ix
                                     : nz_ix + 1),
                      (e_ix == std::string::npos
                       ? str.end()
                       : str.begin() + e_ix));
        }
    }
    return str;
}

Inkscape::SVGOStringStream::SVGOStringStream()
{
    /* These two are probably unnecessary now that we provide our own operator<< for float and
     * double. */
    ostr.imbue(std::locale::classic());
    ostr.setf(std::ios::showpoint);

    ostr.precision(8);
}

Inkscape::SVGOStringStream &
Inkscape::SVGOStringStream::operator<<(double d)
{
    auto &os = *this;

    /* Try as integer first. */
    {
        int const n = int(d);
        if (d == n) {
            os << n;
            return os;
        }
    }

    std::ostringstream s;
    s.imbue(std::locale::classic());
    s.flags(os.setf(std::ios::showpoint));
    s.precision(os.precision());
    s << d;
    os << strip_trailing_zeros(s.str());
    return os;
}

Inkscape::SVGOStringStream &
Inkscape::SVGOStringStream::operator<<(Geom::Point const & p)
{
    auto &os = *this;
    os << p[0] << ',' << p[1];
    return os;
}

Inkscape::SVGIStringStream::SVGIStringStream():std::istringstream()
{
    this->imbue(std::locale::classic());
    this->setf(std::ios::showpoint);
    this->precision(8);
}

Inkscape::SVGIStringStream::SVGIStringStream(const std::string& str):std::istringstream(str)
{
    this->imbue(std::locale::classic());
    this->setf(std::ios::showpoint);

    this->precision(8);
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
