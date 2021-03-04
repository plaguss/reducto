#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

from setuptools import setup# Command, Distribution as _Distribution, Extension as _Extension

here = os.path.abspath(os.path.dirname(__file__))

# install_requires =

try:
    # Deal with extension if Cython is found.
    # http://docs.cython.org/en/latest/src/userguide/source_files_and_compilation.html#distributing-cython-modules
    from Cython.Distutils.extension import Extension
    from Cython.Distutils import build_ext
    USE_CYTHON = True
    ext = '.pyx'
except ModuleNotFoundError:
    USE_CYTHON = False
    ext = '.cpp'


cmdclass = {'build_ext': build_ext}

extensions = [
    Extension(
        "reducto._ext.line_ext",
        ["reducto/_ext/line_wrap" + ext, "reducto/_ext/_line.cpp"],
        include_dirs=[".", r"reducto/_ext"]
    ),
    Extension(
        "reducto._ext.pyfile_wrap",
        ["reducto/_ext/pyfile_wrap" + ext, "reducto/_ext/_pyfile.cpp"],
        depends=["reducto/_ext/_pyfile.h"],
        include_dirs=[".", r"reducto/_ext"]
    )
]


if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize(extensions)


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
    url=about['__url__'],
    # packages=packages,
    package_data={'': ['LICENSE']},
    # package_dir={'requests': 'requests'},
    include_package_data=True,
    python_requires=">=3.6",
    # install_requires=requires,
    license=about['__license__'],
    zip_safe=False,
    ext_modules=extensions,
    cmdclass=cmdclass
    # classifiers=[]
    # cmdclass={'test': PyTest},
    # tests_require=test_requirements
)
