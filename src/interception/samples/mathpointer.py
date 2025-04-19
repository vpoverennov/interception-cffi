import math
from dataclasses import dataclass
from enum import IntEnum

from interception import ffi, lib
from interception.utils import busy_wait, calculate_busy_wait_millisecond, get_screen_height, get_screen_width, lower_process_priority, raise_process_priority

SCALE = 15
SCREEN_WIDTH = get_screen_width()
SCREEN_HEIGHT = get_screen_height()


class Scancode(IntEnum):
    esc = 0x01
    num_0 = 0x0B
    num_1 = 0x02
    num_2 = 0x03
    num_3 = 0x04
    num_4 = 0x05
    num_5 = 0x06
    num_6 = 0x07
    num_7 = 0x08
    num_8 = 0x09
    num_9 = 0x0A


@dataclass
class Point:
    x: float
    y: float


def circle(t: float) -> Point:
    f = 10

    return Point(SCALE * f * math.cos(t), SCALE * f * math.sin(t))


def mirabilis(t: float) -> Point:
    f = 1.0 / 2.0
    k = 1.0 / (2.0 * math.pi)

    return Point(SCALE * f * (math.exp(k * t) * math.cos(t)), SCALE * f * (math.exp(k * t) * math.sin(t)))


def epitrochoid(t: float) -> Point:
    f = 1
    R = 6
    r = 2
    d = 1
    c = R + r

    return Point(SCALE * f * (c * math.cos(t) - d * math.cos((c * t) / r)), SCALE * f * (c * math.sin(t) - d * math.sin((c * t) / r)))


def hypotrochoid(t: float) -> Point:
    f = 10.0 / 7.0
    R = 5
    r = 3
    d = 5
    c = R - r

    return Point(SCALE * f * (c * math.cos(t) + d * math.cos((c * t) / r)), SCALE * f * (c * math.sin(t) - d * math.sin((c * t) / r)))


def hypocycloid(t: float) -> Point:
    f = 10.0 / 3.0
    R = 3
    r = 1
    c = R - r

    return Point(SCALE * f * (c * math.cos(t) + r * math.cos((c * t) / r)), SCALE * f * (c * math.sin(t) - r * math.sin((c * t) / r)))


def bean(t: float) -> Point:
    f = 10
    c = math.cos(t)
    s = math.sin(t)

    return Point(SCALE * f * ((pow(c, 3) + pow(s, 3)) * c), SCALE * f * ((pow(c, 3) + pow(s, 3)) * s))


def Lissajous(t: float) -> Point:
    f = 10
    a = 2
    b = 3

    return Point(SCALE * f * (math.sin(a * t)), SCALE * f * (math.sin(b * t)))


def epicycloid(t: float) -> Point:
    f = 10.0 / 42.0
    R = 21
    r = 10
    c = R + r

    return Point(SCALE * f * (c * math.cos(t) - r * math.cos((c * t) / r)), SCALE * f * (c * math.sin(t) - r * math.sin((c * t) / r)))


def rose(t: float) -> Point:
    f = 10
    R = 1
    k = 2.0 / 7.0

    return Point(SCALE * f * (R * math.cos(k * t) * math.cos(t)), SCALE * f * (R * math.cos(k * t) * math.sin(t)))


def butterfly(t: float) -> Point:
    f = 10.0 / 4.0
    c = math.exp(math.cos(t)) - 2 * math.cos(4 * t) + pow(math.sin(t / 12), 5)

    return Point(SCALE * f * (math.sin(t) * c), SCALE * f * (math.cos(t) * c))


def math_track(context, mouse: int, curve, center: Point, t1: float, t2: float, partitioning: int):
    lower_process_priority()

    mstroke = ffi.new('InterceptionMouseStroke *')
    delta = t2 - t1
    position = curve(t1)

    mstroke.flags = lib.INTERCEPTION_MOUSE_MOVE_ABSOLUTE

    mstroke.state = lib.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
    mstroke.x = int((0xFFFF * center.x) / SCREEN_WIDTH)
    mstroke.y = int((0xFFFF * center.y) / SCREEN_HEIGHT)
    lib.interception_send(context, mouse, mstroke, 1)

    mstroke.state = 0
    mstroke.x = int((0xFFFF * (center.x + position.x)) / SCREEN_WIDTH)
    mstroke.y = int((0xFFFF * (center.y - position.y)) / SCREEN_HEIGHT)
    lib.interception_send(context, mouse, mstroke, 1)

    i = 0
    j = 0
    # for (unsigned int i = 0, j = 0 i <= partitioning + 2 ++i, ++j) {
    while i < partitioning + 2:
        if j % 250 == 0:
            busy_wait(25 * milliseconds)
            mstroke.state = lib.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
            lib.interception_send(context, mouse, mstroke, 1)

            busy_wait(25 * milliseconds)
            mstroke.state = lib.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
            lib.interception_send(context, mouse, mstroke, 1)
            mstroke.state = 0

            if i > 0:
                i -= 2
                assert i > 0

        position = curve(t1 + (i * delta) / partitioning)
        mstroke.x = int((0xFFFF * (center.x + position.x)) / SCREEN_WIDTH)
        mstroke.y = int((0xFFFF * (center.y - position.y)) / SCREEN_HEIGHT)
        lib.interception_send(context, mouse, mstroke, 1)

        busy_wait(3 * milliseconds)
        j += 1
        i += 1

    busy_wait(25 * milliseconds)
    mstroke.state = lib.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
    lib.interception_send(context, mouse, mstroke, 1)

    busy_wait(25 * milliseconds)
    mstroke.state = lib.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
    lib.interception_send(context, mouse, mstroke, 1)

    busy_wait(25 * milliseconds)
    mstroke.state = 0
    mstroke.x = int((0xFFFF * center.x) / SCREEN_WIDTH)
    mstroke.y = int((0xFFFF * center.y) / SCREEN_HEIGHT)
    lib.interception_send(context, mouse, mstroke, 1)

    raise_process_priority()


INTERCEPTION_MAX_KEYBOARD = 10


def INTERCEPTION_MOUSE(index):
    return INTERCEPTION_MAX_KEYBOARD + index + 1


if __name__ == '__main__':
    NUM_SCANCODES = (
        Scancode.num_0,
        Scancode.num_1,
        Scancode.num_2,
        Scancode.num_3,
        Scancode.num_4,
        Scancode.num_5,
        Scancode.num_6,
        Scancode.num_7,
        Scancode.num_8,
        Scancode.num_9,
    )
    mouse = None
    milliseconds = calculate_busy_wait_millisecond()

    position = Point(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    raise_process_priority()

    context = lib.interception_create_context()

    lib.interception_set_filter(context, lib.interception_is_keyboard, lib.INTERCEPTION_FILTER_KEY_DOWN | lib.INTERCEPTION_FILTER_KEY_UP)
    lib.interception_set_filter(context, lib.interception_is_mouse, lib.INTERCEPTION_FILTER_MOUSE_MOVE)

    print('NOTICE: This example works on real machines.')
    print('        Virtual machines generally work with absolute mouse')
    print("        positioning over the screen, which this samples isn't")
    print('        prepared to handle.\n')

    print("Now please, first move the mouse that's going to be impersonated.")

    stroke = ffi.new('InterceptionMouseStroke *')
    while True:
        device = lib.interception_wait(context)
        if not lib.interception_receive(context, device, stroke, 1):
            break
        if lib.interception_is_mouse(device):
            if mouse is None:
                mouse = device
                print(f'Impersonating mouse {device - INTERCEPTION_MOUSE(0)}.')
                print()

                print('Now:')
                print('  - Go to Paint (or whatever place you want to draw)')
                print('  - Select your pencil')
                print('  - Position your mouse in the drawing board')
                print('  - Press any digit (not numpad) on your keyboard to draw an equation')
                print('  - Press ESC to exit.')

            mstroke = stroke

            position.x += mstroke.x
            position.y += mstroke.y

            if position.x < 0:
                position.x = 0
            if position.x > SCREEN_WIDTH - 1:
                position.x = SCREEN_WIDTH - 1
            if position.y < 0:
                position.y = 0
            if position.y > SCREEN_HEIGHT - 1:
                position.y = SCREEN_HEIGHT - 1

            mstroke.flags = lib.INTERCEPTION_MOUSE_MOVE_ABSOLUTE
            mstroke.x = int((0xFFFF * position.x) / SCREEN_WIDTH)
            mstroke.y = int((0xFFFF * position.y) / SCREEN_HEIGHT)

            lib.interception_send(context, device, stroke, 1)

        if mouse is not None and lib.interception_is_keyboard(device):
            kstroke = ffi.cast('InterceptionKeyStroke *', stroke)

            if kstroke.state == lib.INTERCEPTION_KEY_DOWN:
                if kstroke.code == Scancode.num_0:
                    math_track(context, mouse, circle, position, 0, 2 * math.pi, 200)
                elif kstroke.code == Scancode.num_1:
                    math_track(context, mouse, mirabilis, position, -(6 * math.pi), 6 * math.pi, 200)
                elif kstroke.code == Scancode.num_2:
                    math_track(context, mouse, epitrochoid, position, 0, 2 * math.pi, 200)
                elif kstroke.code == Scancode.num_3:
                    math_track(context, mouse, hypotrochoid, position, 0, 6 * math.pi, 200)
                elif kstroke.code == Scancode.num_4:
                    math_track(context, mouse, hypocycloid, position, 0, 2 * math.pi, 200)
                elif kstroke.code == Scancode.num_5:
                    math_track(context, mouse, bean, position, 0, math.pi, 200)
                elif kstroke.code == Scancode.num_6:
                    math_track(context, mouse, Lissajous, position, 0, 2 * math.pi, 200)
                elif kstroke.code == Scancode.num_7:
                    math_track(context, mouse, epicycloid, position, 0, 20 * math.pi, 1000)
                elif kstroke.code == Scancode.num_8:
                    math_track(context, mouse, rose, position, 0, 14 * math.pi, 500)
                elif kstroke.code == Scancode.num_9:
                    math_track(context, mouse, butterfly, position, 0, 21 * math.pi, 2000)
                else:
                    lib.interception_send(context, device, stroke, 1)
            elif kstroke.state == lib.INTERCEPTION_KEY_UP:
                if kstroke.code not in NUM_SCANCODES:
                    lib.interception_send(context, device, stroke, 1)
            else:
                lib.interception_send(context, device, stroke, 1)

            if kstroke.code == Scancode.esc:
                break

    lib.interception_destroy_context(context)
