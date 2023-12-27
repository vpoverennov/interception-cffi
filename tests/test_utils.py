import ctypes

from interception import utils

user32 = ctypes.windll.user32


def test_interface():
    assert utils.HIGH_PRIORITY_CLASS == 0x00000080
    assert utils.NORMAL_PRIORITY_CLASS == 0x00000020
    assert utils.SM_CXSCREEN == 0
    assert utils.SM_CYSCREEN == 1
    assert utils.FALSE == 0
    assert utils.TRUE == 1
    assert utils.ERROR_ALREADY_EXISTS == 0xB7


def test_ffi():
    x = utils.ffi.new('int *', 42)
    assert x[0] == 42


def test_raise_lower():
    utils.raise_process_priority()
    utils.lower_process_priority()


def test_open_close_single_program():
    first = utils.try_open_single_program('interception_test')
    second = utils.try_open_single_program('interception_test')

    assert first is not None
    assert second is None

    utils.close_single_program(first)


def test_screen_width():
    ct_sw = user32.GetSystemMetrics(0)

    sw = utils.get_screen_width()

    assert sw == ct_sw


def test_screen_height():
    ct_sh = user32.GetSystemMetrics(1)

    sh = utils.get_screen_height()

    assert sh == ct_sh
