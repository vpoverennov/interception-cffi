import _cffi_backend

ffi: _cffi_backend.FFI

from typing import Any

InterceptionContext = int

InterceptionDevice = int

InterceptionPrecedence = int

InterceptionFilter = int


class _InterceptionMouseStroke:
    state: int
    flags: int
    rolling: int
    x: int
    y: int
    information: int


class _InterceptionKeyStroke:
    code: int
    state: int
    information: int


#InterceptionStroke = InterceptionMouseStroke | InterceptionKeyStroke
InterceptionStroke = Any


class InterceptionPredicate:
    def __call__(self, device: int) -> bool: ...


class _InterceptionLib:
    INTERCEPTION_KEY_DOWN: int
    INTERCEPTION_KEY_UP: int
    INTERCEPTION_KEY_E0: int
    INTERCEPTION_KEY_E1: int
    INTERCEPTION_KEY_TERMSRV_SET_LED: int
    INTERCEPTION_KEY_TERMSRV_SHADOW: int
    INTERCEPTION_KEY_TERMSRV_VKPACKET: int

    INTERCEPTION_FILTER_KEY_NONE: int
    INTERCEPTION_FILTER_KEY_ALL: int
    INTERCEPTION_FILTER_KEY_DOWN: int
    INTERCEPTION_FILTER_KEY_UP: int
    INTERCEPTION_FILTER_KEY_E0: int
    INTERCEPTION_FILTER_KEY_E1: int
    INTERCEPTION_FILTER_KEY_TERMSRV_SET_LED: int
    INTERCEPTION_FILTER_KEY_TERMSRV_SHADOW: int
    INTERCEPTION_FILTER_KEY_TERMSRV_VKPACKET: int

    INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN: int
    INTERCEPTION_MOUSE_LEFT_BUTTON_UP: int
    INTERCEPTION_MOUSE_RIGHT_BUTTON_DOWN: int
    INTERCEPTION_MOUSE_RIGHT_BUTTON_UP: int
    INTERCEPTION_MOUSE_MIDDLE_BUTTON_DOWN: int
    INTERCEPTION_MOUSE_MIDDLE_BUTTON_UP: int

    INTERCEPTION_MOUSE_BUTTON_1_DOWN: int
    INTERCEPTION_MOUSE_BUTTON_1_UP: int
    INTERCEPTION_MOUSE_BUTTON_2_DOWN: int
    INTERCEPTION_MOUSE_BUTTON_2_UP: int
    INTERCEPTION_MOUSE_BUTTON_3_DOWN: int
    INTERCEPTION_MOUSE_BUTTON_3_UP: int

    INTERCEPTION_MOUSE_BUTTON_4_DOWN: int
    INTERCEPTION_MOUSE_BUTTON_4_UP: int
    INTERCEPTION_MOUSE_BUTTON_5_DOWN: int
    INTERCEPTION_MOUSE_BUTTON_5_UP: int

    INTERCEPTION_MOUSE_WHEEL: int
    INTERCEPTION_MOUSE_HWHEEL: int

    INTERCEPTION_FILTER_MOUSE_NONE: int
    INTERCEPTION_FILTER_MOUSE_ALL: int

    INTERCEPTION_FILTER_MOUSE_LEFT_BUTTON_DOWN: int
    INTERCEPTION_FILTER_MOUSE_LEFT_BUTTON_UP: int
    INTERCEPTION_FILTER_MOUSE_RIGHT_BUTTON_DOWN: int
    INTERCEPTION_FILTER_MOUSE_RIGHT_BUTTON_UP: int
    INTERCEPTION_FILTER_MOUSE_MIDDLE_BUTTON_DOWN: int
    INTERCEPTION_FILTER_MOUSE_MIDDLE_BUTTON_UP: int

    INTERCEPTION_FILTER_MOUSE_BUTTON_1_DOWN: int
    INTERCEPTION_FILTER_MOUSE_BUTTON_1_UP: int
    INTERCEPTION_FILTER_MOUSE_BUTTON_2_DOWN: int
    INTERCEPTION_FILTER_MOUSE_BUTTON_2_UP: int
    INTERCEPTION_FILTER_MOUSE_BUTTON_3_DOWN: int
    INTERCEPTION_FILTER_MOUSE_BUTTON_3_UP: int

    INTERCEPTION_FILTER_MOUSE_BUTTON_4_DOWN: int
    INTERCEPTION_FILTER_MOUSE_BUTTON_4_UP: int
    INTERCEPTION_FILTER_MOUSE_BUTTON_5_DOWN: int
    INTERCEPTION_FILTER_MOUSE_BUTTON_5_UP: int

    INTERCEPTION_FILTER_MOUSE_WHEEL: int
    INTERCEPTION_FILTER_MOUSE_HWHEEL: int

    INTERCEPTION_FILTER_MOUSE_MOVE: int

    INTERCEPTION_MOUSE_MOVE_RELATIVE: int
    INTERCEPTION_MOUSE_MOVE_ABSOLUTE: int
    INTERCEPTION_MOUSE_VIRTUAL_DESKTOP: int
    INTERCEPTION_MOUSE_ATTRIBUTES_CHANGED: int
    INTERCEPTION_MOUSE_MOVE_NOCOALESCE: int
    INTERCEPTION_MOUSE_TERMSRV_SRC_SHADOW: int

    @staticmethod
    def interception_create_context() -> InterceptionContext: ...

    @staticmethod
    def interception_destroy_context(context: InterceptionContext) -> None: ...

    @staticmethod
    def interception_get_precedence(context: InterceptionContext, device: InterceptionDevice) -> InterceptionPrecedence: ...

    @staticmethod
    def interception_set_precedence(context: InterceptionContext, device: InterceptionDevice, precedence: InterceptionPrecedence) -> None: ...

    @staticmethod
    def interception_get_filter(context: InterceptionContext, device: InterceptionDevice) -> InterceptionFilter: ...

    @staticmethod
    def interception_set_filter(context: InterceptionContext, predicate: InterceptionPredicate, filter: InterceptionFilter) -> None: ...

    @staticmethod
    def interception_wait(context: InterceptionContext) -> InterceptionDevice: ...

    @staticmethod
    def interception_wait_with_timeout(context: InterceptionContext, milliseconds: int) -> InterceptionDevice: ...

    @staticmethod
    def interception_send(context: InterceptionContext, device: InterceptionDevice, stroke: InterceptionStroke, nstroke: int) -> int: ...

    @staticmethod
    def interception_receive(context: InterceptionContext, device: InterceptionDevice, stroke: InterceptionStroke, nstroke: int) -> int: ...

    @staticmethod
    def interception_get_hardware_id(context: InterceptionContext, device: InterceptionDevice, hardware_id_buffer: Any, buffer_size: int) -> int: ...

    # @staticmethod
    # def interception_is_invalid(device: InterceptionDevice) -> int: ...
    interception_is_invalid: InterceptionPredicate

    # @staticmethod
    # def interception_is_keyboard(device: InterceptionDevice) -> int: ...
    interception_is_keyboard: InterceptionPredicate

    # @staticmethod
    # def interception_is_mouse(device: InterceptionDevice) -> int: ...
    interception_is_mouse: InterceptionPredicate


lib: _InterceptionLib
