#!/usr/bin/env python
#
# Copyright 2012-2017 by Hartmut Goebel <h.goebel@crazy-compilers.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

__author__ = "Hartmut Goebel <h.goebel@crazy-compilers.com>"
__copyright__ = "Copyright 2012-2017 by Hartmut Goebel <h.goebel@crazy-compilers.com>"
__licence__ = "GNU General Public License version 3 (GPL v3)"

import pytest

from pdftools.pdfposter import papersizes, decide_num_pages
from pdftools.pdfposter.cmd import __parse_box as parse_box
import math

def Box(x, y, name):
    return {
        'width': x*papersizes[name][0],
        'height': y*papersizes[name][1],
        'offset_x': 0,
        'offset_y': 0,
        'unit': name,
        'units_x': x,
        'units_y': y,
        }
def Width(name): return papersizes[name][0]
def Height(name): return papersizes[name][1]

A4port = Box(1, 1, 'a4')
A4land = Box(1, 1, 'a4')
A4land['width'], A4land['height'] = A4land['height'], A4land['width']
A4land['unit'] = 'a4_land'

cm = papersizes['cm'][0]


def test_without_options(tmpdir):
    # default media-size is 1x1a4 and default poster-size is media-size
    inbox = parse_box('1x1a4')
    media = parse_box('1x1a4')
    poster = parse_box('1x1a4')
    cols, rows, scale, rotate = decide_num_pages(inbox, media, poster)
    assert cols == 1
    assert rows == 1
    assert scale == 1.0
    assert rotate == False

def test_mediasize(tmpdir):
    # default poster-size is media-size, so this is one page
    inbox = parse_box('1x1a4')
    media = parse_box('3x4a5')
    poster = parse_box('3x4a5')
    cols, rows, scale, rotate = decide_num_pages(inbox, media, poster)
    assert cols == 1
    assert rows == 1
    assert rotate == False

def test_postersize(tmpdir):
    # default media-size is 1x1a4 and poster fits on 3x2 pages
    inbox = parse_box('1x1a4')
    media = parse_box('1x1a4')
    poster = parse_box('3x4a5')
    cols, rows, scale, rotate = decide_num_pages(inbox, media, poster)
    assert cols == 2
    assert rows == 3
    assert rotate == True

def test_postersize_and_mediasize(tmpdir):
    # poster: 23 x 42 dinlang = 23 x 14 a4 = 13685 x 11802 pt - landscape(!)
    # inbox: 595 x 842 pt
    # -> scale = 16.25
    # -> printed size = 9671 x 13685 = 7.6 x 5.75 Media
    # media: 3 x 4 a5 = 1260 x 2380 pt,
    inbox = parse_box('1x1a4')
    media = parse_box('3x4a5')
    poster = parse_box('23x42dinla') # ca. 23x14a4
    cols, rows, scale, rotate = decide_num_pages(inbox, media, poster)
    assert cols == 8
    assert rows == 6
    #assert scale == 1.0
    assert rotate == False

def test_landscape_input_1(tmpdir):
    inbox = parse_box('20x10cm') # landscape
    media = parse_box('10x15cm') # portrait
    poster = parse_box('60x60cm')
    # scale will be 3
    cols, rows, scale, rotate = decide_num_pages(inbox, media, poster)
    assert round(scale, 6) == 3
    assert cols, rows in [(6,2), (4,3)] # twelve sheets either way round
    assert rotate == True

def test_landscape_input_2(tmpdir):
    inbox = parse_box('20x10cm') # landscape
    media = parse_box('15x10cm') # landscape
    poster = parse_box('60x60cm')
    # scale will be 3
    cols, rows, scale, rotate = decide_num_pages(inbox, media, poster)
    assert round(scale, 6) == 3
    assert cols, rows in [(6,2), (4,3)] # twelve sheets either way round
    assert rotate == True

def test_landscape_input_3(tmpdir):
    inbox = parse_box('20x10cm') # landscape
    media = parse_box('15x10cm') # landscape
    poster = parse_box('60x30cm') # landscape
    # scale will be 3
    cols, rows, scale, rotate = decide_num_pages(inbox, media, poster)
    assert round(scale, 6) == 3
    assert cols, rows in [(6,2), (4,3)] # twelve sheets either way round
    assert rotate == False # poster and inbox are both landscape

def test_landscape_input_4(tmpdir):
    inbox = parse_box('20x10cm') # landscape
    media = parse_box('15x10cm') # landscape
    poster = parse_box('30x60cm') # portrait
    # scale will be 3
    cols, rows, scale, rotate = decide_num_pages(inbox, media, poster)
    assert round(scale, 6) == 3
    assert cols, rows in [(6,2), (4,3)] # twelve sheets either way round
    assert rotate == True

def test_scale_by_two(tmpdir):
    inbox = parse_box('1x1a4')
    media = parse_box('1x1a4')
    cols, rows, scale, rotate = decide_num_pages(inbox, media, None, scale=2)
    assert cols == 2
    assert rows == 2
    assert scale == 2.0
    assert rotate == False

#---

def test_1x1_A4_on_A4():
    for mediabox in (A4port, A4land):
      for inbox in (A4port, A4land):
        for posterbox in (A4port, A4land):
            cols, rows, scale, rotate = decide_num_pages(
                inbox, mediabox, posterbox)
            # rotate if orientation does not match
            assert rotate == (mediabox != inbox)
            # output is a single page
            assert scale == 1
            assert rows == 1
            assert cols == 1


def test_1x1_A4port_to_1x2_A4port():
    cols, rows, scale, rotate = decide_num_pages(
        A4port, A4port, Box(1, 2, 'a4'))
    # output is a single page
    assert not rotate
    assert scale == 1
    assert rows == 1
    assert cols == 1

def test_1x1_A4port_to_2x1_A4port():
    cols, rows, scale, rotate = decide_num_pages(
        A4port, A4port, Box(2, 1, 'a4'))
    # output is two pages, scaled to A3
    assert rotate
    assert round(abs(scale-1.4142), 2) == 0
    assert rows == 2
    assert cols == 1

def test_1x1_A4port_to_2x99_A4port():
    cols, rows, scale, rotate = decide_num_pages(
        A4port, A4port, Box(2, 99, 'a4'))
    # output is four pages, scaled by 2
    assert not rotate
    assert scale == 2
    assert rows == 2
    assert cols == 2

def test_1x1_A4port_to_99x2_A4port():
    cols, rows, scale, rotate = decide_num_pages(
        A4port, A4port, Box(99, 2, 'a4'))
    ## 99 portrait pages wide and 2 portrait pages high.
    # output is four pages, scaled by ~2.8
    # poster is not rotated, so the output will be ~2x4.1A4
    assert not rotate
    assert round(abs(scale-2.0*Height('a4')/Width('a4')), 7) == 0
    assert round(abs(scale-2*1.4142), 2) == 0
    assert rows == math.ceil(Height('a4')*scale/Height('a4'))
    assert cols == math.ceil(Width('a4')*scale/Width('a4'))
    assert rows == 3
    assert cols == 3

