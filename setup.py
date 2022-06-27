
from setuptools import setup

from distutils.core import Command
from distutils import log
import os, sys

class build_docs(Command):
    description = "build documentation from rst-files"
    user_options=[]

    def initialize_options (self): pass
    def finalize_options (self):
        self.docpages = DOCPAGES
        
    def run(self):
        substitutions = ('.. |VERSION| replace:: '
                         + self.distribution.get_version())
        for writer, rstfilename, outfilename in self.docpages:
            distutils.dir_util.mkpath(os.path.dirname(outfilename))
            log.info("creating %s page %s", writer, outfilename)
            if not self.dry_run:
                try:
                    with open(rstfilename, "rb") as fh:
                        rsttext = fh.read().decode('utf-8')
                except IOError as e:
                    sys.exit(e)
                rsttext = '\n'.join((substitutions, '', rsttext))
                # docutils.core does not offer easy reading from a
                # string into a file, so we need to do it ourself :-(
                doc = docutils.core.publish_string(source=rsttext,
                                                   source_path=rstfilename,
                                                   writer_name=writer)
                try:
                    with open(outfilename, 'wb') as fh:
                        fh.write(doc) # is already encoded
                except IOError as e:
                    sys.exit(e)

cmdclass = {}

try:
    import docutils.core
    import docutils.io
    import docutils.writers.manpage
    import distutils.command.build
    distutils.command.build.build.sub_commands.append(('build_docs', None))
    cmdclass['build_docs'] = build_docs
except ImportError:
    log.warn("docutils not installed, can not build man pages. "
             "Using pre-build ones.")

DOCPAGES = (
    ('manpage', 'pdfposter.rst', 'docs/pdfposter.1'),
    ('html', 'pdfposter.rst', 'docs/pdfposter.html'),
    )

setup(cmdclass=cmdclass)
