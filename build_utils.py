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

void raise_process_priority(void);
void lower_process_priority(void);
int get_screen_width(void);
int get_screen_height(void);
void busy_wait(unsigned long count);
unsigned long calculate_busy_wait_millisecond(void);
void *try_open_single_program(const char *name);
void close_single_program(void *program_instance);
"""
)
ffibuilder.set_source(
    'interception._utils',
    libraries=['Kernel32', 'User32'],
    source="""
#include <time.h>
#include <string.h>
#include <windows.h>

void raise_process_priority(void) {
    SetPriorityClass(GetCurrentProcess(), HIGH_PRIORITY_CLASS);
}

void lower_process_priority(void) {
    SetPriorityClass(GetCurrentProcess(), NORMAL_PRIORITY_CLASS);
}

int get_screen_width(void) {
    return GetSystemMetrics(SM_CXSCREEN);
}

int get_screen_height(void) {
    return GetSystemMetrics(SM_CYSCREEN);
}

#pragma optimize("", off)
void busy_wait(unsigned long count){
    while(--count);
}

unsigned long calculate_busy_wait_millisecond(void)
{
    unsigned long count = 2000000000;
    time_t start = time(NULL);
    while(--count);
    return (unsigned long) (2000000 / difftime(time(NULL), start));
}

#pragma optimize("", on)

void* try_open_single_program(const char* full_name) {
    HANDLE program_instance = CreateMutexA(NULL, FALSE, full_name);
    if (GetLastError() == ERROR_ALREADY_EXISTS) {
        return NULL;
    }
    return program_instance;
}

void close_single_program(void *program_instance) {
    CloseHandle(program_instance);
}
""",
)

if __name__ == '__main__':
    ffibuilder.compile()
