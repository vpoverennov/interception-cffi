from interception import ffi, lib as interception

SCANCODE_X = 0x2D
SCANCODE_Y = 0x15
SCANCODE_ESC = 0x01

if __name__ == '__main__':

    # raise_process_priority()

    context = interception.interception_create_context()

    interception.interception_set_filter(
        context, interception.interception_is_keyboard,
        interception.INTERCEPTION_FILTER_KEY_DOWN | interception.INTERCEPTION_FILTER_KEY_UP,
    )

    stroke = ffi.new('InterceptionKeyStroke *')
    while True:
        device = interception.interception_wait(context)
        if not interception.interception_receive(context, device, stroke, 1):
            break

        if stroke.code == SCANCODE_X:
            stroke.code = SCANCODE_Y

        interception.interception_send(context, device, stroke, 1)

        if stroke.code == SCANCODE_ESC:
            break

    interception.interception_destroy_context(context)
