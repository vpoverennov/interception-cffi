#!/usr/bin/env python
from distutils.core import setup

setup(
    name='interception',
    version='0.5',
    description='interception cffi bindings',
    author='vpoverennov',
    author_email='vasya.poverennov@gmail.com',
    url='https://github.com/vpoverennov/interception-cffi',
    setup_requires=['cffi>=1.0.0'],
    py_modules=['interception_build'],
    cffi_modules=['interception_build.py:ffibuilder'],
    install_requires=['cffi>=1.0.0'],
    packages=['interception', 'interception.samples'],
    package_dir={
        'interception': 'interception',
        'interception.samples': 'samples',
    },
    package_data={
        'interception': ['interception.dll', 'interception64.dll'],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
)
