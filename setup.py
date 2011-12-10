#!/usr/bin/env python

# distribute
from distribute_setup import use_setuptools
use_setuptools()
from setuptools import setup

# distutils
# from distutils.core import setup

# setuptools
# from setuptools import setup

setup(name='SeenThis',
      version='0.1',
      description='Use the SeenThis API',
      long_description='Use the SeenThis API. SeenThis <http://seenthis.net> is a social network mostly targeted towards the exchange of interesting URLs and short-blogging. See the source code and the example scripts for documentation.',
      license='BSD',
      author='Stephane Bortzmeyer',
      author_email='stephane+seenthis@bortzmeyer.org',
      url='https://github.com/bortzmeyer/seenthis-python',
      download_url='https://github.com/bortzmeyer/seenthis-python/tarball/master',
      py_modules=['SeenThis', 'FeedParserPlus'],
      scripts=['seenthis-backup.py', 'seenthis-post.py'],
      data_files=[('/usr/local/doc/SeenThis', ['README',]),],
      provides=['SeenThis',],
      install_requires=['feedparser'] # TODO: even when simpletal
      # is installed, distribute's setup.py tries to download it from PyPi,
      # probably because there is no locally installed egg for it in the Debian
      # package. The only solution is to install simpletal; by hand.
      )
# TODO: add classifiers
