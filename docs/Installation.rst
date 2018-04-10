
Download & Installation
=========================

Instructions for Windows Users
-----------------------------------

1. |pdfposter| requires Python. If you don't have Python installed already,
   download and install Python 3.6 from http://python.org/download/3.6/

   During installation, make sure to check "Include into PATH".

2. If you already have Python installed, please check that your Python
   directory (normally C:\Python36 for python 3.6) and the Python Scripts
   directory (normally C:\Python36\Scripts) are in the system path. If not,
   just add them in ``My computer->Properties->Advanced->Environment
   Variables`` to the ``Path`` system variable.

3. Install `pdfposter` by running ::

     pip install pdftools.pdfposter

   Then run the console command `pdfposter --help` to get detailed help.

Instructions for GNU/Linux
------------------------------

Most current GNU/Linux distributions provide packages for |pdposter|. Simply
search your distribution's software cataloge.

If your GNU/Linux distribution does not provide a current version of continue
with `installing pdfposter`_ below.
Optionally you might want to install `python-pypdf2`
- which is a requirement for |pdfposter| -
so at least this package will be maintained by your distribution.
The package might be named different in your distribution.


Instructions for other Operating Systems
----------------------------------------------

Many vendors provide Python. and some provie |pdfposter|.
Please check your vendor's software repository.
Otherwise please download Python 3.6 from http://www.python.org/download/ and
follow the installation instructions there.


Installing pdfposter
---------------------------------

After installing Python (and optionally pypdf2), just run::

  sudo pip install pdftools.pdfposter

to install |pdfposter| for all users. For installing |pdfposter| for yourself
only, run::

  pip install --user pdftools.pdfposter

If your system does not have network access
- download |pdfposter| from http://pypi.python.org/pypi/pdfposter,
- downlaod `pyPDF2` from http://mstamy2.github.io/PyPDF2/, and
- run::

    sudo pip install --user pdftools.pdfposter-*.tar.gz PyPDF2-*.zip

  respective ::

    pip install pdftools.pdfposter-*.tar.gz PyPDF2-*.zip


