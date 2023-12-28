from typing import Any

import _cffi_backend

ffi: _cffi_backend.FFI

class _UtilsLib:
    @staticmethod
    def raise_process_priority() -> None: ...
    @staticmethod
    def lower_process_priority() -> None: ...
    @staticmethod
    def get_screen_width() -> int: ...
    @staticmethod
    def get_screen_height() -> int: ...
    @staticmethod
    def try_open_single_program(full_name: bytes) -> Any: ...
    @staticmethod
    def close_single_program(program: Any) -> None: ...

lib: _UtilsLib
