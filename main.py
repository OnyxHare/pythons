# main.py
import tkinter as tk
import win32gui

from ime_win32 import get_focus_hwnd, get_ime_on_for_hwnd


def get_window_title(hwnd):
    if not hwnd:
        return ""
    return win32gui.GetWindowText(hwnd)


def main():
    root = tk.Tk()
    root.title("IME 状態モニタ")

    label_ime   = tk.Label(root, text="IME: N/A", font=("Meiryo", 16))
    label_ime.pack(padx=20, pady=10)

    label_title = tk.Label(root, text="Window: ", wraplength=400)
    label_title.pack(padx=20, pady=10)

    state = {"last_hwnd": None, "last_ime": None}

    def poll():
        hwnd   = get_focus_hwnd()
        ime_on = get_ime_on_for_hwnd(hwnd)

        ime_str = "ON" if ime_on else "OFF" if ime_on is not None else "N/A"

        if hwnd != state["last_hwnd"] or ime_on != state["last_ime"]:
            title = get_window_title(hwnd)
            label_ime.config(text=f"IME: {ime_str}")
            label_title.config(text=f"Window: {title}")
            state["last_hwnd"] = hwnd
            state["last_ime"]  = ime_on

        root.after(100, poll)

    poll()
    root.mainloop()


if __name__ == "__main__":
    main()
