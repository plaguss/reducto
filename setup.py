#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from setuptools import Extension, setup

here = os.path.abspath(os.path.dirname(__file__))

# Deal with extension if Cython is found.
# http://docs.cython.org/en/latest/src/userguide/source_files_and_compilation.html#distributing-cython-modules
# Check if cython command is found, then use it.
# https://stackoverflow.com/questions/11210104/check-if-a-program-exists-from-a-python-script
USE_CYTHON = bool(shutil.which('cython'))

ext = '.pyx' if USE_CYTHON else '.cpp'

extensions = [
    Extension("reducto_ext", ["reducto/ext/line"+ext])
]

if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize(extensions)


about = {}
with open(os.path.join(here, 'reducto', '__version__.py'), 'r') as f:
    exec(f.read(), about)

with open('README.md', 'r') as f:
    readme = f.read()


setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    # url=about['__url__'],
    # packages=packages,
    package_data={'': ['LICENSE']},
    # package_dir={'requests': 'requests'},
    include_package_data=True,
    # python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    # install_requires=requires,
    license=about['__license__'],
    zip_safe=False,
    ext_modukes=extensions
    # classifiers=[]
    # cmdclass={'test': PyTest},
    # tests_require=test_requirements
)
