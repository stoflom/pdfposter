# -*- mode: python ; coding: utf-8 -*-
#
# Copyright (C) 2008-2025 Hartmut Goebel <h.goebel@crazy-compilers.com>
# SPDX-License-Identifier: GPL-3.0-or-later
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
#
# Build requirements
# - docutils
# - inkscape
#
# For building tests
# - pdf2ps (comes with ghostscript)
# - poster 
#
# For building examles
# Build requirements
# - ImageMagick
#

import os

ENV = {
    'PYTHONPATH': os.environ.get('PYTHONPATH'),
    'PATH': os.environ['PATH'],
    }

env = Environment(ENV=ENV)
env.SConsignFile()

env.Export(['env'])
env.SConscript(dirs='test')
env.SConscript(dirs='examples')

env.Command('docs/pdfposter.html', 'pdfposter.rst',
            'build-aux/gen-man-page.py $SOURCE html $TARGET')
env.Command('docs/pdfposter.1', 'pdfposter.rst',
            'build-aux/gen-man-page.py $SOURCE manpage $TARGET')
# create PNG projectlogo for project homepage
env.Command('projectlogo.png', 'projectlogo.svg',
            'inkscape --export-filename=$TARGET --export-height=100 $SOURCE')

hires_logo = env.Command('build/icons/projectlogo-hires.png', 'projectlogo.svg',
                         'inkscape --export-filename=$TARGET $SOURCE')

icon_parts = [
    env.Command('build/icons/project-${WIDTH}x${HEIGHT}.pnm', hires_logo,
                'pngtopnm $SOURCE ' \
                '| pnmscale -width=$WIDTH -height=$HEIGHT ' \
                '| ppmquant 256 > $TARGET',
                WIDTH=w, HEIGHT=w)
    for w in (16, 32, 48)
    ]

env.Command('projectlogo.ico', icon_parts,
            'ppmtowinicon $SOURCES > $TARGET')
