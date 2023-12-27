from interception import ffi, lib


def test_key_stroke():
    x = ffi.new('InterceptionKeyStroke *', {'code': 42, 'state': 0x1, 'information': 0xff})

    assert x.code == 42
    assert x.state == 0x1
    assert x.information == 0xff


def test_mouse_stroke():
    x = ffi.new('InterceptionMouseStroke *', {'state': 0x1, 'flags': 0x2, 'rolling': 0x3, 'x': 100, 'y': 200, 'information': 0xff})

    assert x.state == 0x1
    assert x.flags == 0x2
    assert x.rolling == 0x3
    assert x.x == 100
    assert x.y == 200
    assert x.information == 0xff


def test_e2e():
    context = lib.interception_create_context()
    assert context is not None
    lib.interception_set_filter(context, lib.interception_is_keyboard, lib.INTERCEPTION_FILTER_KEY_DOWN | lib.INTERCEPTION_FILTER_KEY_UP)
    lib.interception_set_filter(context, lib.interception_is_mouse, lib.INTERCEPTION_FILTER_MOUSE_LEFT_BUTTON_DOWN)
    lib.interception_destroy_context(context)
