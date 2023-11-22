from interception import ffi, lib
from interception.utils import close_single_program, raise_process_priority, try_open_single_program


class SCANCODE:
    ESC = 0x01
    CTRL = 0x1D
    CAPSLOCK = 0x3A


class KeyStroke:
    def __init__(self, code, state):
        self.code = code
        self.state = state
        self.c = ffi.new('InterceptionKeyStroke *', {'code': code, 'state': state})[0]

    def __eq__(self, other):
        return self.code == other.code and self.state == other.state


esc_down = KeyStroke(SCANCODE.ESC, lib.INTERCEPTION_KEY_DOWN)
ctrl_down = KeyStroke(SCANCODE.CTRL, lib.INTERCEPTION_KEY_DOWN)
capslock_down = KeyStroke(SCANCODE.CAPSLOCK, lib.INTERCEPTION_KEY_DOWN)
esc_up = KeyStroke(SCANCODE.ESC, lib.INTERCEPTION_KEY_UP)
ctrl_up = KeyStroke(SCANCODE.CTRL, lib.INTERCEPTION_KEY_UP)
capslock_up = KeyStroke(SCANCODE.CAPSLOCK, lib.INTERCEPTION_KEY_UP)

capslock_is_down = False
esc_give_up = False


def caps2esc(kstroke):
    global capslock_is_down, esc_give_up
    kstrokes = []
    if capslock_is_down:
        if kstroke == capslock_down or kstroke.code == SCANCODE.CTRL:
            return kstrokes
        if kstroke == capslock_up:
            if esc_give_up:
                esc_give_up = False
                kstrokes.append(ctrl_up.c)
            else:
                kstrokes.append(esc_down.c)
                kstrokes.append(esc_up.c)
            capslock_is_down = False
            return kstrokes
        if not esc_give_up and not (kstroke.state & lib.INTERCEPTION_KEY_UP):
            esc_give_up = True
            kstrokes.append(ctrl_down.c)
        if kstroke == esc_down:
            kstrokes.append(capslock_down.c)
        elif kstroke == esc_up:
            kstrokes.append(capslock_up.c)
        else:
            kstrokes.append(kstroke)

        return kstrokes

    if kstroke == capslock_down:
        capslock_is_down = True
        return kstrokes

    if kstroke == esc_down:
        kstrokes.append(capslock_down.c)
    elif kstroke == esc_up:
        kstrokes.append(capslock_up.c)
    else:
        kstrokes.append(kstroke)

    return kstrokes


if __name__ == '__main__':
    import sys

    program_instance = try_open_single_program('407631B6-78D3-4EFC-A868-40BBB7204CF1')
    if not program_instance:
        sys.exit()

    raise_process_priority()

    context = lib.interception_create_context()

    lib.interception_set_filter(context, lib.interception_is_keyboard, lib.INTERCEPTION_FILTER_KEY_DOWN | lib.INTERCEPTION_FILTER_KEY_UP)

    kstroke = ffi.new('InterceptionKeyStroke *')

    while True:
        device = lib.interception_wait(context)
        if not lib.interception_receive(context, device, kstroke, 1):
            break
        kstrokes = caps2esc(kstroke[0])

        if kstrokes:
            lib.interception_send(context, device, ffi.new('InterceptionKeyStroke []', kstrokes), len(kstrokes))
    lib.interception_destroy_context(context)
    close_single_program(program_instance)
