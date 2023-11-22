from cffi import FFI

HIGH_PRIORITY_CLASS = 0x00000080
NORMAL_PRIORITY_CLASS = 0x00000020
SM_CXSCREEN = 0
SM_CYSCREEN = 1
FALSE = 0
TRUE = 1
ERROR_ALREADY_EXISTS = 0xB7

ffi = FFI()
ffi.set_unicode(False)
ffi.cdef(
    """
HANDLE GetCurrentProcess(void);
BOOL  SetPriorityClass(HANDLE hProcess, DWORD dwPriorityClass);
HANDLE CreateMutexA(void* lpMutexAttributes, BOOL bInitialOwner, LPCSTR lpName);
BOOL CloseHandle(HANDLE hObject);

int WINAPI GetSystemMetrics(int nIndex);

"""
)
kernel32 = ffi.dlopen('Kernel32.dll')
user32 = ffi.dlopen('User32.dll')


def raise_process_priority():
    kernel32.SetPriorityClass(kernel32.GetCurrentProcess(), HIGH_PRIORITY_CLASS)


def lower_process_priority():
    kernel32.SetPriorityClass(kernel32.GetCurrentProcess(), NORMAL_PRIORITY_CLASS)


def get_screen_width():
    return user32.GetSystemMetrics(SM_CXSCREEN)


def get_screen_height():
    return user32.GetSystemMetrics(SM_CYSCREEN)


def try_open_single_program(name):
    full_name = ffi.new('char[]', rb'Global\{%s}' % bytes(name, 'ascii'))

    program_instance = kernel32.CreateMutexA(ffi.NULL, FALSE, full_name)
    if ffi.getwinerror()[0] == ERROR_ALREADY_EXISTS or program_instance == ffi.NULL:
        return
    return program_instance


def close_single_program(program_instance):
    kernel32.CloseHandle(program_instance)
