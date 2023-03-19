#
# Copyright 2008-2022 by Hartmut Goebel <h.goebel@crazy-compilers.com>
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#

import pytest
import os, sys

from pdfposter import cmd
import PyPDF2

CHESSBOARD = os.path.join(os.path.dirname(__file__), '..', 'chessboard.pdf')

def get_num_pages(filename):
    with open(filename, 'rb') as fh:
        reader = PyPDF2.PdfReader(fh)
        return len(reader.pages)

def test_without_options(tmpdir):
    outname = str(tmpdir.join('out.pdf'))
    cmd.run([CHESSBOARD, outname])
    # default media-size is 1x1a4 and default poster-size is media-size
    assert get_num_pages(outname) == 1

def test_mediasize(tmpdir):
    outname = str(tmpdir.join('out.pdf'))
    cmd.run([CHESSBOARD, '-m3x4a5', outname])
    # default poster-size is media-size, so this is one page
    assert get_num_pages(outname) == 1

def test_postersize(tmpdir):
    outname = str(tmpdir.join('out.pdf'))
    cmd.run([CHESSBOARD, '-p3x4a5', outname])
    # default media-size is 1x1a4 and poster fits on 3x2 pages
    assert get_num_pages(outname) == 6

def test_postersize_and_mediasize(tmpdir):
    outname = str(tmpdir.join('out.pdf'))
    cmd.run([CHESSBOARD, '-m3x4a5', '-p23x42dinla', outname])
    # see tests/unit/test_decide for calculation
    assert get_num_pages(outname) == 48

def test_scale_by_two(tmpdir):
    outname = str(tmpdir.join('out.pdf'))
    # Need to specify media a bit larger since the page in the input
    # file is sightly larger than a4
    cmd.run([CHESSBOARD, '-s2', '-m1.1x1.1a4', outname])
    assert get_num_pages(outname) == 4
