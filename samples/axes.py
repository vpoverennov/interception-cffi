from interception import ffi, lib

SCANCODE_ESC = 0x01

if __name__ == '__main__':

    # raise_process_priority()

    context = lib.interception_create_context()

    lib.interception_set_filter(context, lib.interception_is_keyboard, lib.INTERCEPTION_FILTER_KEY_DOWN | lib.INTERCEPTION_FILTER_KEY_UP)
    lib.interception_set_filter(context, lib.interception_is_mouse, lib.INTERCEPTION_FILTER_MOUSE_MOVE)

    stroke = ffi.new('InterceptionMouseStroke *')
    while True:
        device = lib.interception_wait(context)
        if not lib.interception_receive(context, device, stroke, 1):
            break
        if lib.interception_is_mouse(device):
            if not (stroke.flags & lib.INTERCEPTION_MOUSE_MOVE_ABSOLUTE):
                stroke.y *= -1

            lib.interception_send(context, device, stroke, 1)

        if lib.interception_is_keyboard(device):
            kstroke = ffi.cast('InterceptionKeyStroke *', stroke)

            lib.interception_send(context, device, stroke, 1)

            if kstroke.code == SCANCODE_ESC:
                break

    lib.interception_destroy_context(context)

