from cffi import FFI

ffibuilder = FFI()
ffibuilder.set_unicode(False)
ffibuilder.cdef(
    """
HANDLE GetCurrentProcess(void);
BOOL  SetPriorityClass(HANDLE hProcess, DWORD dwPriorityClass);
HANDLE CreateMutexA(void* lpMutexAttributes, BOOL bInitialOwner, LPCSTR lpName);
BOOL CloseHandle(HANDLE hObject);

int WINAPI GetSystemMetrics(int nIndex);

void raise_process_priority();
void lower_process_priority();
int get_screen_width();
int get_screen_height();
void* try_open_single_program(const char* full_name);
void close_single_program(void* program);
"""
)
ffibuilder.set_source(
    'interception._utils',
    libraries=['Kernel32', 'User32'],
    source="""
#include <windows.h>

void raise_process_priority() {
    SetPriorityClass(GetCurrentProcess(), HIGH_PRIORITY_CLASS);
}
void lower_process_priority() {
    SetPriorityClass(GetCurrentProcess(), NORMAL_PRIORITY_CLASS);
}
int get_screen_width() {
    return GetSystemMetrics(SM_CXSCREEN);
}
int get_screen_height() {
    return GetSystemMetrics(SM_CYSCREEN);
}
void* try_open_single_program(const char* full_name) {
    HANDLE program_instance = CreateMutexA(NULL, FALSE, full_name);
    if (GetLastError() == ERROR_ALREADY_EXISTS) {
        return NULL;
    }
    return program_instance;
}
void close_single_program(void* program) {
    CloseHandle(program);
}
""",
)

if __name__ == '__main__':
    ffibuilder.compile()
