# -*- coding: ISO-8859-15 -*-
# =================================================================
#
# $Id$
#
# Authors: Tom Kralidis <tomkralidis@hotmail.com>
#
# Copyright (c) 2010 Tom Kralidis
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import config

def get_today_and_now():
    import time
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime())

def get_version_integer(version):
    if version is not None:  # split and make integer
        a = version.split('.')
        if len(a) != 3:
            return -1
        try:
            return int(a[0]) * 10000 + int(a[1]) * 100 + int(a[2])
        except:
            return -1
    else:  # not a valid version string
         return -1

def nspath_eval(xpath, namespaces=config.namespaces):
    out = []
    for s in xpath.split('/'):
        ns, el = s.split(':')
        out.append('{%s}%s' % (namespaces[ns],el))
    return '/'.join(out)

def xmltag_split(tag):
    return tag.split('}')[1]

def bbox2polygon(bbox):
    # like '-180,-90,180,90'
    minx,miny,maxx,maxy=bbox.split(',')
    poly = []
    poly.append((float(minx),float(miny)))
    poly.append((float(minx),float(maxy)))
    poly.append((float(maxx),float(maxy)))
    poly.append((float(maxx),float(miny)))
    return poly

def bbox2wkt(bbox):
    tmp=bbox.split(',')
    minx = float(tmp[0])
    miny = float(tmp[1])
    maxx = float(tmp[2])
    maxy = float(tmp[3])
    return 'POLYGON((%.2f %.2f, %.2f %.2f, %.2f %.2f, %.2f %.2f, %.2f %.2f))' % (minx, miny, minx, maxy, maxx, maxy, maxx, miny, minx, miny)

def query_not_bbox(bbox_data,bbox_input):
    if bbox_input is None:
        return 'false'

    if bbox_data is None:
        return 'true'

    from shapely.wkt import loads
    from shapely.geometry import Polygon

    b1 = loads(bbox2wkt(bbox_data))
    b2 = loads(bbox2wkt(bbox_input))

    if b1.disjoint(b2) is True:
        return 'true' 
    else:
        return 'false'

def query_bbox(bbox_data,bbox_input):
    if bbox_data is None or bbox_input is None:
        return 'false'

    from shapely.wkt import loads
    from shapely.geometry import Polygon

    b1 = loads(bbox2wkt(bbox_data))
    b2 = loads(bbox2wkt(bbox_input))

    if b1.intersects(b2) is True:
        return 'true' 
    else:
        return 'false'

def query_anytext(xml, searchterm):
    # perform fulltext search against XML
    exml=etree.fromstring(xml)
    for el in exml.xpath('//text()'):  # all elements
        if el.lower().find(searchterm.lower()) != -1:
            return 'true'
    for att in exml.xpath('//attribute::*'):  # all attributes
        if att.lower().find(searchterm.lower()) != -1:
            return 'true'
    return 'false'

def query_xpath(xml, xpath, searchterm, matchcase=False):
    # perform search against XPath
    exml=etree.fromstring(xml)
    for x in xml.xpath(xpath):  # all elements
        if matchcase is True:
            if x.text == searchterm:
                return 'true'
        else:
            if x.text.lower() == searchterm.lower():
                return 'true'
    return 'false'
