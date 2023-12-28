from __future__ import annotations

from typing import Any

from interception import ffi, lib


def test_key_stroke():
    stroke: Any = ffi.new('InterceptionKeyStroke *', {'code': 42, 'state': 0x1, 'information': 0xFF})

    assert stroke.code == 42
    assert stroke.state == 0x1
    assert stroke.information == 0xFF


def test_mouse_stroke():
    stroke: Any = ffi.new('InterceptionMouseStroke *', {'state': 0x1, 'flags': 0x2, 'rolling': 0x3, 'x': 100, 'y': 200, 'information': 0xFF})

    assert stroke.state == 0x1
    assert stroke.flags == 0x2
    assert stroke.rolling == 0x3
    assert stroke.x == 100
    assert stroke.y == 200
    assert stroke.information == 0xFF


def test_e2e():
    context = lib.interception_create_context()
    assert context is not None
    lib.interception_set_filter(context, lib.interception_is_keyboard, lib.INTERCEPTION_FILTER_KEY_DOWN | lib.INTERCEPTION_FILTER_KEY_UP)
    lib.interception_set_filter(context, lib.interception_is_mouse, lib.INTERCEPTION_FILTER_MOUSE_LEFT_BUTTON_DOWN)
    lib.interception_destroy_context(context)
