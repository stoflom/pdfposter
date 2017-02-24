#
# Copyright 2008-2017 by Hartmut Goebel <h.goebel@crazy-compilers.com>
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

import pytest
import os, sys

import pdftools.pdfposter
from pdftools.pdfposter import cmd, __version__


def test_help(capsys):
    with pytest.raises(SystemExit) as excinfo:
        cmd.run(['foobar', '--help'])
    assert excinfo.value.code == 0
    out, err = capsys.readouterr()
    assert "Be verbose" in out

def test_help_media_names(capsys):
    with pytest.raises(SystemExit) as excinfo:
        cmd.run(['foobar', '--help-media-names'])
    assert excinfo.value.code == 0
    out, err = capsys.readouterr()
    assert "media and distance names" in out
    assert "a2 a3 a4" in out

def test_version(capsys):
    with pytest.raises(SystemExit) as excinfo:
        cmd.run(['foobar', '--version'])
    assert excinfo.value.code == 0
    out, err = capsys.readouterr()
    if sys.version_info < (3,0):
        # for Python 2.7 message are written to stderr
        out = err
    assert len(out.splitlines()) == 1
    progname = os.path.basename(sys.argv[0])
    assert out.strip() == ('%s %s' % (progname, __version__))

def test_without_options(monkeypatch):

    def mockmain(opts, infilename, outfilename, password_hook=None):
        assert infilename == 'in.pdf'
        assert outfilename == 'out.pdf'

    # 'main' is imported into `cmd`, need to monkeypath there
    monkeypatch.setattr(cmd, 'main', mockmain)
    cmd.run(['in.pdf', 'out.pdf'])


def test_can_parse_mediasize(monkeypatch):

    def mockmain(opts, infilename, outfilename, password_hook=None):
        media_size = opts.media_size
        assert media_size['unit'] == 'a5'
        assert media_size['units_x'] == 3
        assert media_size['units_y'] == 4

    # 'main' is imported into `cmd`, need to monkeypath there
    monkeypatch.setattr(cmd, 'main', mockmain)
    cmd.run(['in.pdf', '-m3x4a5', 'out.pdf'])

def test_can_parse_postersize(monkeypatch):

    def mockmain(opts, infilename, outfilename, password_hook=None):
        poster_size = opts.poster_size
        assert poster_size['unit'] == 'a5'
        assert poster_size['units_x'] == 3
        assert poster_size['units_y'] == 4

    # 'main' is imported into `cmd`, need to monkeypath there
    monkeypatch.setattr(cmd, 'main', mockmain)
    cmd.run(['in.pdf', '-p3x4a5', 'out.pdf'])


def test_postersize_defaults_to_mediasize(monkeypatch):

    def mockmain(opts, infilename, outfilename, password_hook=None):
        opts.poster_size == opts.media_size
        poster_size = opts.poster_size
        assert poster_size['unit'] == 'a5'
        assert poster_size['units_x'] == 3
        assert poster_size['units_y'] == 4

    # 'main' is imported into `cmd`, need to monkeypath there
    monkeypatch.setattr(cmd, 'main', mockmain)
    cmd.run(['in.pdf', '-m3x4a5', 'out.pdf'])


def test_postersize_and_mediasize_given(monkeypatch):

    def mockmain(opts, infilename, outfilename, password_hook=None):
        opts.poster_size == opts.media_size
        media_size = opts.media_size
        assert media_size['unit'] == 'a5'
        assert media_size['units_x'] == 3
        assert media_size['units_y'] == 4

        poster_size = opts.poster_size
        assert poster_size['unit'] == 'dinlang'
        assert poster_size['units_x'] == 23
        assert poster_size['units_y'] == 42

    # 'main' is imported into `cmd`, need to monkeypath there
    monkeypatch.setattr(cmd, 'main', mockmain)
    cmd.run(['in.pdf', '-m3x4a5', '-p23x42dinla', 'out.pdf'])
