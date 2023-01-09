from tkinter import *
from tkinter.ttk import *
import os
import keyboard
from tkinter import messagebox

global hotkey_start, hotkey_stop
hotkey_start = 'Alt + C'
hotkey_stop = 'Alt + C'

def check_hotkey(combo_hotkey, combo2_hotkey, window_hotkey):
    global hotkey_start, hotkey_stop
    try:
        keyboard.release(combo_hotkey.get().lower())
        keyboard.release(combo2_hotkey.get().lower())
    except:
        messagebox.showwarning(title = 'Invalid Hotkey Name', message = f'Invalid key name for Hotkey(s).')
        return
    hotkey_start = combo_hotkey.get()
    hotkey_stop = combo2_hotkey.get()

    window_hotkey.destroy()

def hotkey():
    window_hotkey = Tk()
    window_hotkey.geometry('235x120')
    window_hotkey.resizable(0, 0)
    window_hotkey.attributes('-topmost', True)
    window_hotkey.title('Set Hotkeys')
    window_hotkey.iconbitmap('system/assets/aa_logo.ico')

    lbl_hotkey = Label(window_hotkey, text = 'Hotkey Start:')
    lbl_hotkey.place(x = 5, y = 10)

    combo_hotkey_values = ('Alt + C', 'Ctrl + C', 'Enter', 'Backspace', 'Tab', 'Esc', 'Ctrl + V', 'Left Shift', 'Right Shift', 'Caps Lock', 'Menu', 'Left Alt', 'Alt Gr', 'Left Ctrl', 'Right Ctrl', 'Delete', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12') #Right Alt, Fn, Numpad Lock
    combo_hotkey = Combobox(window_hotkey, width = 20, values = combo_hotkey_values)
    combo_hotkey.insert(0, hotkey_start)
    combo_hotkey.place(x = 80, y = 10)

    lbl2_hotkey = Label(window_hotkey, text = 'Hotkey Stop:')
    lbl2_hotkey.place(x = 5, y = 40)

    combo2_hotkey = Combobox(window_hotkey, width = 20, values = combo_hotkey_values)
    combo2_hotkey.insert(0, hotkey_stop)
    combo2_hotkey.place(x = 80, y = 40)

    btn_cancel = Button(window_hotkey, text = 'Cancel', command = lambda: window_hotkey.destroy())
    btn_cancel.place(x = 20, y = 80)

    btn_done = Button(window_hotkey, text = 'Done', command = lambda: check_hotkey(combo_hotkey, combo2_hotkey, window_hotkey))
    btn_done.place(x = 138, y = 80)

    window_hotkey.mainloop()