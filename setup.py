#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import Extension, setup

from setuptools import setup# Command, Distribution as _Distribution, Extension as _Extension
from setuptools.command.build_ext import build_ext as _build_ext

here = os.path.abspath(os.path.dirname(__file__))

# Deal with extension if Cython is found.
# http://docs.cython.org/en/latest/src/userguide/source_files_and_compilation.html#distributing-cython-modules

# ext = '.pyx' if USE_CYTHON else '.cpp'
USE_CYTHON = False
try:
    from Cython.Build import cythonize
    from Cython.Distutils.extension import Extension as _Extension
    from Cython.Distutils import build_ext as _build_ext
    USE_CYTHON = True
    # ext = '.pyx'
    extensions = [
        Extension(
            "reducto_ext",
            ["reducto/ext/line_wrap.pyx", "reducto/ext/_line.cpp"],
            include_dirs=[".", r"reducto/ext"],
            # depends=["reducto/ext/_line.h"]
        )
    ]
    extensions = cythonize(extensions)
except ModuleNotFoundError:
    raise NotImplementedError
    ext = '.cpp'
    extensions = [
        Extension(
            "reducto_ext",
            [r"reducto/ext/_line" + ext],
            include_dirs=[".", r"reducto/ext"],
            # depends=["reducto/ext/_line.h"]
        )
    ]


# Distribute wheels? (https://github.com/yaml/pyyaml/blob/master/setup.py)
try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:
    bdist_wheel = None


about = {}
with open(os.path.join(here, 'reducto', '_version.py'), 'r') as f:
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
    ext_modules=extensions,
    cmdclass={'build_ext': _build_ext}
    # classifiers=[]
    # cmdclass={'test': PyTest},
    # tests_require=test_requirements
)
