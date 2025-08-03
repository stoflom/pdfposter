#! /usr/bin/python
#
# Copyright 2008-2025 by Hartmut Goebel <h.goebel@crazy-compilers.com>
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
# SPDX-License-Identifier: GPL-3.0-or-later


import argparse
import subprocess
import sys
from pathlib import Path

import docutils.core
import docutils.io
import docutils.writers.manpage


def _(text):
    return text


def _get_version():
    project_dir = Path(__file__).parent.parent
    result = subprocess.run(
        [sys.executable, '-c', 'from setuptools import *; setup()', '--version'],
        capture_output=True, check=True, cwd=project_dir)
    version = result.stdout.decode().strip()
    return version


def run(writer, rstfile, outfile, version=None):
    if not version:
        version = _get_version()
    substitutions = f'.. |VERSION| replace:: {version}'
    rsttext = rstfile.read_text()
    rsttext = '\n'.join((substitutions, '', rsttext))
    # docutils.core does not offer easy reading from a
    # string into a file, so we need to do it ourselves :-(
    try:
        doc = docutils.core.publish_string(source=rsttext,
                                           source_path=str(rstfile),
                                           writer_name=writer)
    except ImportError as e:
        raise SystemExit(e)
    outfile.write_bytes(doc)  # is already encoded
    print(_("{filename} written").format(filename=outfile))


def main():
    parser = argparse.ArgumentParser(
        description=_("build documentation from rst-files"))
    parser.add_argument('--version', nargs='?',
                        help=_("default: ask setuptools"))
    parser.add_argument('rstfile', metavar=_("rstfile"), type=Path)
    parser.add_argument('writer', metavar=_("writer"),
                        help="name of docutils writer to use")
    parser.add_argument('outfile', metavar=_("outfile"), type=Path)
    args = parser.parse_args()
    try:
        run(**vars(args))
    except (IOError, subprocess.SubprocessError) as e:
        raise SystemExit(e)


if __name__ == '__main__':
    main()
