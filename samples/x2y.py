from interception import ffi, lib

SCANCODE_X = 0x2D
SCANCODE_Y = 0x15
SCANCODE_ESC = 0x01

if __name__ == '__main__':

    # raise_process_priority()

    context = lib.interception_create_context()

    lib.interception_set_filter(context, lib.interception_is_keyboard, lib.INTERCEPTION_FILTER_KEY_DOWN | lib.INTERCEPTION_FILTER_KEY_UP)

    stroke = ffi.new('InterceptionKeyStroke *')
    while True:
        device = lib.interception_wait(context)
        if not lib.interception_receive(context, device, stroke, 1):
            break

        if stroke.code == SCANCODE_X:
            stroke.code = SCANCODE_Y

        lib.interception_send(context, device, stroke, 1)

        if stroke.code == SCANCODE_ESC:
            break

    lib.interception_destroy_context(context)
