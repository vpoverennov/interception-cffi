from interception import ffi, lib
from interception.utils import raise_process_priority

SCANCODE_ESC = 0x01

if __name__ == '__main__':

    raise_process_priority()

    context = lib.interception_create_context()

    lib.interception_set_filter(context, lib.interception_is_keyboard, lib.INTERCEPTION_FILTER_KEY_DOWN | lib.INTERCEPTION_FILTER_KEY_UP)
    lib.interception_set_filter(context, lib.interception_is_mouse, lib.INTERCEPTION_FILTER_MOUSE_LEFT_BUTTON_DOWN)

    hardware_id = ffi.new('wchar_t[500]')
    stroke = ffi.new('InterceptionMouseStroke *')
    while True:
        device = lib.interception_wait(context)
        if not lib.interception_receive(context, device, stroke, 1):
            break

        if lib.interception_is_keyboard(device):
            kstroke = ffi.cast('InterceptionKeyStroke *', stroke)

            if kstroke.code == SCANCODE_ESC:
                break

        length = lib.interception_get_hardware_id(context, device, hardware_id, ffi.sizeof(hardware_id))
        if 0 < length < ffi.sizeof(hardware_id):
            print(ffi.string(hardware_id))
        lib.interception_send(context, device, stroke, 1)

    lib.interception_destroy_context(context)
