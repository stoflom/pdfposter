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

from pdftools.pdfposter import decide_num_pages
from pdftools.pdfposter.cmd import __parse_box as parse_box


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
