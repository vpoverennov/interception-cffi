import sys as _sys
import os as _os

from ._interception import ffi

_is_64bits = _sys.maxsize > 2 ** 32

if _is_64bits:
    _libname = 'interception64.dll'
else:
    _libname = 'interception.dll'

_path = _os.path.dirname(_os.path.abspath(__file__))
lib = ffi.dlopen(_os.path.join(_path, _libname))
