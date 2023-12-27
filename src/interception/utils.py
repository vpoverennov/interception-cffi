from __future__ import annotations

from dataclasses import dataclass as _dataclass

from ._utils import ffi, lib as _utils_lib

__all__ = [
    'raise_process_priority',
    'lower_process_priority',
    'ProgramHandle',
    'try_open_single_program',
    'HIGH_PRIORITY_CLASS',
    'NORMAL_PRIORITY_CLASS',
    'SM_CXSCREEN',
    'SM_CYSCREEN',
    'FALSE',
    'TRUE',
    'ERROR_ALREADY_EXISTS',
]

HIGH_PRIORITY_CLASS = 0x00000080
NORMAL_PRIORITY_CLASS = 0x00000020
SM_CXSCREEN = 0
SM_CYSCREEN = 1
FALSE = 0
TRUE = 1
ERROR_ALREADY_EXISTS = 0xB7


def raise_process_priority():
    """SetPriorityClass(GetCurrentProcess(), HIGH_PRIORITY_CLASS)"""
    _utils_lib.raise_process_priority()


def lower_process_priority():
    """SetPriorityClass(GetCurrentProcess(), NORMAL_PRIORITY_CLASS)"""
    _utils_lib.lower_process_priority()


get_screen_width = _utils_lib.get_screen_width
get_screen_height = _utils_lib.get_screen_height


@_dataclass
class ProgramHandle:
    ptr: ffi.CData


def try_open_single_program(name: str) -> ProgramHandle | None:
    program_instance = _utils_lib.try_open_single_program(rb'Global\{%s}' % name.encode('ascii'))
    if program_instance == ffi.NULL:
        return None
    return ProgramHandle(program_instance)


def close_single_program(program_instance: ProgramHandle) -> None:
    _utils_lib.CloseHandle(program_instance.ptr)
