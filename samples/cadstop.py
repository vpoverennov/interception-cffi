from interception import ffi, lib
from interception.utils import raise_process_priority


class SCANCODE:
    ESC = 0x01
    CTRL = 0x1D
    ALT = 0x38
    DEL = 0x53


class KeyStroke(object):
    def __init__(self, code, state):
        self.code = code
        self.state = state

    def __eq__(self, other):
        return self.code == other.code and self.state == other.state


ctrl_down = KeyStroke(SCANCODE.CTRL, lib.INTERCEPTION_KEY_DOWN)
alt_down = KeyStroke(SCANCODE.ALT, lib.INTERCEPTION_KEY_DOWN)
del_down = KeyStroke(SCANCODE.DEL, lib.INTERCEPTION_KEY_DOWN | lib.INTERCEPTION_KEY_E0)
ctrl_up = KeyStroke(SCANCODE.CTRL, lib.INTERCEPTION_KEY_UP)
alt_up = KeyStroke(SCANCODE.ALT, lib.INTERCEPTION_KEY_UP)
del_up = KeyStroke(SCANCODE.DEL, lib.INTERCEPTION_KEY_UP | lib.INTERCEPTION_KEY_E0)

ctrl_is_down = False
alt_is_down = False
del_is_down = False


def shall_produce_keystroke(kstroke):
    global ctrl_is_down, alt_is_down, del_is_down

    if ctrl_is_down + alt_is_down + del_is_down < 2:
        if kstroke == ctrl_down:
            ctrl_is_down = True
        if kstroke == ctrl_up:
            ctrl_is_down = False
        if kstroke == alt_down:
            alt_is_down = True
        if kstroke == alt_up:
            alt_is_down = False
        if kstroke == del_down:
            del_is_down = True
        if kstroke == del_up:
            del_is_down = False
        return True

    if ctrl_is_down == 0 and (kstroke == ctrl_down or kstroke == ctrl_up):
        return False

    if alt_is_down == 0 and (kstroke == alt_down or kstroke == alt_up):
        return False

    if del_is_down == 0 and (kstroke == del_down or kstroke == del_up):
        return False

    if kstroke == ctrl_up:
        ctrl_is_down = False
    elif kstroke == alt_up:
        alt_is_down = False
    elif kstroke == del_up:
        del_is_down = False

    return True


if __name__ == '__main__':
    raise_process_priority()

    context = lib.interception_create_context()

    lib.interception_set_filter(context, lib.interception_is_keyboard, lib.INTERCEPTION_FILTER_KEY_ALL)

    stroke = ffi.new('InterceptionKeyStroke *')
    while True:
        device = lib.interception_wait(context)
        if not lib.interception_receive(context, device, stroke, 1):
            break

        if not shall_produce_keystroke(stroke):
            print('ctrl-alt-del pressed')
            continue

        lib.interception_send(context, device, stroke, 1)

        if stroke.code == SCANCODE.ESC:
            break

    lib.interception_destroy_context(context)
