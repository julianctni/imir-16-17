"""
py2app/py2exe build script for SimilarImage.

Will automatically ensure that all build prerequisites are available
via ez_setup

Usage (Mac OS X):
    python setup.py py2app

Usage (Windows):
    python setup.py py2exe

Usage (Unix):
    python setup.py install
"""
import ez_setup

ez_setup.use_setuptools()

import sys
from setuptools import setup

APP = ['src/app.py']
APP_NAME = 'SimilarImage'
DATA_FILES = ['assets/index.csv']

if sys.platform == 'darwin':
    extra_options = dict(
        setup_requires=['py2app'],
        app=APP,
        # Cross-platform applications generally expect sys.argv to
        # be used for opening files.
        options=dict(py2app=dict(argv_emulation=True, packages=['PIL']))
    )
elif sys.platform == 'win32':
    extra_options = dict(
         setup_requires=['py2exe'],
         app=APP,
    )
else:
    extra_options = dict(
         # Normally unix-like platforms will use "setup.py install"
         # and install the main script as such
         scripts=APP,
    )

setup(
    name=APP_NAME,
    data_files=DATA_FILES,
    **extra_options
)
