#!/usr/bin/env python
from textwrap import dedent

from setuptools import setup

setup(
    name='interception',
    version='0.6.dev0',
    description='interception cffi bindings',
    long_description=dedent(
        """
        Interception
        ============
        
        Low-level python binding for the `interception library <https://github.com/oblitum/Interception>`_ built using cffi
        
        Documentation
        -------------
        
        `github <https://github.com/vpoverennov/interception-cffi>`_
        """
    ),
    author='Vasiliy Poverennov',
    author_email='vasiliy@poverennov.com',
    url='https://github.com/vpoverennov/interception-cffi',
    setup_requires=['cffi @ git+https://github.com/python-cffi/cffi.git'],
    cffi_modules=[
        'src/interception_build.py:ffibuilder',
        'src/utils_build.py:ffibuilder',
    ],
    install_requires=['cffi>=1.0.0'],
    python_requires='>=3.8',
    packages=['interception', 'interception.samples'],
    package_dir={
        'interception': 'src/interception',
        'interception.samples': 'src/samples',
    },
    package_data={
        'interception': ['py.typed'],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
