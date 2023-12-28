from pathlib import Path

from cffi import FFI

base = Path(__file__).parent
ffibuilder = FFI()
with open(base / '../interception_library/interception.c') as interception_c:
    ffibuilder.set_source(
        'interception._interception',
        f"""
    #define INTERCEPTION_STATIC
    
    #include "interception.h"
    
    {interception_c.read()}
    """,
        include_dirs=[base / '../interception_library'],
    )

ffibuilder.cdef(
    """
typedef void *InterceptionContext;
typedef int InterceptionDevice;
typedef int InterceptionPrecedence;
typedef unsigned short InterceptionFilter;
typedef int (*InterceptionPredicate)(InterceptionDevice device);

enum InterceptionKeyState {
    INTERCEPTION_KEY_DOWN,
    INTERCEPTION_KEY_UP,
    INTERCEPTION_KEY_E0,
    INTERCEPTION_KEY_E1,
    INTERCEPTION_KEY_TERMSRV_SET_LED,
    INTERCEPTION_KEY_TERMSRV_SHADOW,
    INTERCEPTION_KEY_TERMSRV_VKPACKET,
};

enum InterceptionFilterKeyState {
    INTERCEPTION_FILTER_KEY_NONE,
    INTERCEPTION_FILTER_KEY_ALL,
    INTERCEPTION_FILTER_KEY_DOWN,
    INTERCEPTION_FILTER_KEY_UP,
    INTERCEPTION_FILTER_KEY_E0,
    INTERCEPTION_FILTER_KEY_E1,
    INTERCEPTION_FILTER_KEY_TERMSRV_SET_LED,
    INTERCEPTION_FILTER_KEY_TERMSRV_SHADOW,
    INTERCEPTION_FILTER_KEY_TERMSRV_VKPACKET,
};

enum InterceptionMouseState {
    INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN,
    INTERCEPTION_MOUSE_LEFT_BUTTON_UP,
    INTERCEPTION_MOUSE_RIGHT_BUTTON_DOWN,
    INTERCEPTION_MOUSE_RIGHT_BUTTON_UP,
    INTERCEPTION_MOUSE_MIDDLE_BUTTON_DOWN,
    INTERCEPTION_MOUSE_MIDDLE_BUTTON_UP,

    INTERCEPTION_MOUSE_BUTTON_1_DOWN,
    INTERCEPTION_MOUSE_BUTTON_1_UP,
    INTERCEPTION_MOUSE_BUTTON_2_DOWN,
    INTERCEPTION_MOUSE_BUTTON_2_UP,
    INTERCEPTION_MOUSE_BUTTON_3_DOWN,
    INTERCEPTION_MOUSE_BUTTON_3_UP,

    INTERCEPTION_MOUSE_BUTTON_4_DOWN,
    INTERCEPTION_MOUSE_BUTTON_4_UP,
    INTERCEPTION_MOUSE_BUTTON_5_DOWN,
    INTERCEPTION_MOUSE_BUTTON_5_UP,

    INTERCEPTION_MOUSE_WHEEL,
    INTERCEPTION_MOUSE_HWHEEL,
};

enum InterceptionFilterMouseState {
    INTERCEPTION_FILTER_MOUSE_NONE,
    INTERCEPTION_FILTER_MOUSE_ALL,

    INTERCEPTION_FILTER_MOUSE_LEFT_BUTTON_DOWN,
    INTERCEPTION_FILTER_MOUSE_LEFT_BUTTON_UP,
    INTERCEPTION_FILTER_MOUSE_RIGHT_BUTTON_DOWN,
    INTERCEPTION_FILTER_MOUSE_RIGHT_BUTTON_UP,
    INTERCEPTION_FILTER_MOUSE_MIDDLE_BUTTON_DOWN,
    INTERCEPTION_FILTER_MOUSE_MIDDLE_BUTTON_UP,

    INTERCEPTION_FILTER_MOUSE_BUTTON_1_DOWN,
    INTERCEPTION_FILTER_MOUSE_BUTTON_1_UP,
    INTERCEPTION_FILTER_MOUSE_BUTTON_2_DOWN,
    INTERCEPTION_FILTER_MOUSE_BUTTON_2_UP,
    INTERCEPTION_FILTER_MOUSE_BUTTON_3_DOWN,
    INTERCEPTION_FILTER_MOUSE_BUTTON_3_UP,

    INTERCEPTION_FILTER_MOUSE_BUTTON_4_DOWN,
    INTERCEPTION_FILTER_MOUSE_BUTTON_4_UP,
    INTERCEPTION_FILTER_MOUSE_BUTTON_5_DOWN,
    INTERCEPTION_FILTER_MOUSE_BUTTON_5_UP,

    INTERCEPTION_FILTER_MOUSE_WHEEL,
    INTERCEPTION_FILTER_MOUSE_HWHEEL,

    INTERCEPTION_FILTER_MOUSE_MOVE,
};

enum InterceptionMouseFlag {
    INTERCEPTION_MOUSE_MOVE_RELATIVE,
    INTERCEPTION_MOUSE_MOVE_ABSOLUTE,
    INTERCEPTION_MOUSE_VIRTUAL_DESKTOP,
    INTERCEPTION_MOUSE_ATTRIBUTES_CHANGED,
    INTERCEPTION_MOUSE_MOVE_NOCOALESCE,
    INTERCEPTION_MOUSE_TERMSRV_SRC_SHADOW,
};

typedef struct {
    unsigned short state;
    unsigned short flags;
    short rolling;
    int x;
    int y;
    unsigned int information;
} InterceptionMouseStroke;

typedef struct {
    unsigned short code;
    unsigned short state;
    unsigned int information;
} InterceptionKeyStroke;

typedef void *InterceptionStroke;

InterceptionContext interception_create_context(void);

void interception_destroy_context(InterceptionContext context);

InterceptionPrecedence interception_get_precedence(InterceptionContext context, InterceptionDevice device);

void interception_set_precedence(InterceptionContext context, InterceptionDevice device, InterceptionPrecedence precedence);

InterceptionFilter interception_get_filter(InterceptionContext context, InterceptionDevice device);

void interception_set_filter(InterceptionContext context, InterceptionPredicate predicate, InterceptionFilter filter);

InterceptionDevice interception_wait(InterceptionContext context);

InterceptionDevice interception_wait_with_timeout(InterceptionContext context, unsigned long milliseconds);

int interception_send(InterceptionContext context, InterceptionDevice device, const InterceptionStroke stroke, unsigned int nstroke);

int interception_receive(InterceptionContext context, InterceptionDevice device, InterceptionStroke stroke, unsigned int nstroke);

unsigned int interception_get_hardware_id(InterceptionContext context, InterceptionDevice device, void *hardware_id_buffer, unsigned int buffer_size);

int interception_is_invalid(InterceptionDevice device);

int interception_is_keyboard(InterceptionDevice device);

int interception_is_mouse(InterceptionDevice device);
"""
)

if __name__ == '__main__':
    ffibuilder.compile()
