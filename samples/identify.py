from interception import ffi, lib

SCANCODE_ESC = 0x01

# as ABI mode is used macros are not available
INTERCEPTION_MAX_KEYBOARD = 10


def INTERCEPTION_KEYBOARD(index):
    return index + 1


def INTERCEPTION_MOUSE(index):
    return INTERCEPTION_MAX_KEYBOARD + index + 1


if __name__ == '__main__':

    # raise_process_priority()

    context = lib.interception_create_context()

    lib.interception_set_filter(context, lib.interception_is_keyboard,
                                lib.INTERCEPTION_FILTER_KEY_DOWN | lib.INTERCEPTION_FILTER_KEY_UP)
    lib.interception_set_filter(context, lib.interception_is_mouse, lib.INTERCEPTION_FILTER_MOUSE_LEFT_BUTTON_DOWN)

    stroke = ffi.new('InterceptionMouseStroke *')
    while True:
        device = lib.interception_wait(context)
        if not lib.interception_receive(context, device, stroke, 1):
            break

        if lib.interception_is_keyboard(device):
            kstroke = ffi.cast('InterceptionKeyStroke *', stroke)
            print('INTERCEPTION_KEYBOARD({})'.format(device - INTERCEPTION_KEYBOARD(0)))
            if kstroke.code == SCANCODE_ESC:
                break
        elif lib.interception_is_mouse(device):
            print('INTERCEPTION_MOUSE({})'.format(device - INTERCEPTION_MOUSE(0)))
        else:
            print('UNRECOGNIZED({})'.format(device))

        lib.interception_send(context, device, stroke, 1)

    lib.interception_destroy_context(context)
