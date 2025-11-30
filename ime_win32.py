# ime_win32.py
import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
imm32  = ctypes.windll.imm32

class RECT(ctypes.Structure):
    _fields_ = [
        ("left",   wintypes.LONG),
        ("top",    wintypes.LONG),
        ("right",  wintypes.LONG),
        ("bottom", wintypes.LONG),
    ]

class GUITHREADINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize",        wintypes.DWORD),
        ("flags",         wintypes.DWORD),
        ("hwndActive",    wintypes.HWND),
        ("hwndFocus",     wintypes.HWND),
        ("hwndCapture",   wintypes.HWND),
        ("hwndMenuOwner", wintypes.HWND),
        ("hwndMoveSize",  wintypes.HWND),
        ("hwndCaret",     wintypes.HWND),
        ("rcCaret",       RECT),
    ]

user32.GetForegroundWindow.restype = wintypes.HWND

user32.GetWindowThreadProcessId.argtypes = [
    wintypes.HWND,
    ctypes.POINTER(wintypes.DWORD),
]
user32.GetWindowThreadProcessId.restype  = wintypes.DWORD

user32.GetGUIThreadInfo.argtypes = [
    wintypes.DWORD,
    ctypes.POINTER(GUITHREADINFO),
]
user32.GetGUIThreadInfo.restype  = wintypes.BOOL

imm32.ImmGetContext.argtypes      = [wintypes.HWND]
imm32.ImmGetContext.restype       = wintypes.HANDLE

imm32.ImmReleaseContext.argtypes  = [wintypes.HWND, wintypes.HANDLE]
imm32.ImmReleaseContext.restype   = wintypes.BOOL

imm32.ImmGetOpenStatus.argtypes   = [wintypes.HANDLE]
imm32.ImmGetOpenStatus.restype    = wintypes.BOOL


def get_focus_hwnd():
    hwnd_fore = user32.GetForegroundWindow()
    if not hwnd_fore:
        return None

    pid = wintypes.DWORD()
    thread_id = user32.GetWindowThreadProcessId(hwnd_fore, ctypes.byref(pid))
    if not thread_id:
        return None

    gti = GUITHREADINFO()
    gti.cbSize = ctypes.sizeof(GUITHREADINFO)

    if not user32.GetGUIThreadInfo(thread_id, ctypes.byref(gti)):
        return None

    return gti.hwndFocus or hwnd_fore


def get_ime_on_for_hwnd(hwnd):
    if not hwnd:
        return None

    hIMC = imm32.ImmGetContext(hwnd)
    if not hIMC:
        return None

    try:
        is_open = imm32.ImmGetOpenStatus(hIMC)
        return bool(is_open)
    finally:
        imm32.ImmReleaseContext(hwnd, hIMC)
