from tkinter import *
from tkinter.ttk import *
import os
from tkinter import messagebox
import system.Auto_System as Auto_System

def name_preset(combo_order, window_preset, entry_preset, combo_repeat):
    path = "presets"
    dir_list = os.listdir(path)
    files = []
    for file in dir_list:
        files.append(file.replace('.txt', '').lower())
    if entry_preset.get().lower() in files:
        messagebox.showwarning(title = 'Invalid Name', message = 'This name is already in use. Try again!')
        print('Name already exists.')
    else:
        if '/' in entry_preset.get() or '\\' in entry_preset.get() or ':' in entry_preset.get() or '*' in entry_preset.get() or '?' in entry_preset.get() or '"' in entry_preset.get() or '>' in entry_preset.get() or '<' in entry_preset.get() or '|' in entry_preset.get():
            messagebox.showwarning(title = 'Invalid Name', message = 'You cannot use these characters in a file name: \ / : * ? " < > |')
            print('Invalid characters used.')
        else:
            print('Valid name!')
            print('Proceed to creating new preset.')
            Auto_System.create_preset(combo_order, entry_preset.get(), combo_repeat)
            window_preset.destroy()

def ask_preset(combo_preset):
    msg1 = messagebox.askyesno(title = 'Import Preset', message = 'You are about to replace all current actions with the ones from a preset. Do you wish to proceed?')
    if msg1:
        msg2 = messagebox.askyesno(title = 'Import Preset', message = "Do you wish to convert the preset's settings to ones that match your screen resolution?")
        if msg2:
            change_res = 1
        else:
            change_res = 0
        Auto_System.import_preset(combo_preset.get(), change_res)
        messagebox.showinfo(title = 'Import Preset', message = "The preset has been successfully imported! Press 'Ok' to return to the app.")
    else:
        combo_preset.current(0)
    return

def preset(combo_order, combo_repeat):
    window_preset = Tk()
    window_preset.geometry('245x85')
    window_preset.resizable(0, 0)
    window_preset.attributes('-topmost', True)
    window_preset.title('Name Preset')
    window_preset.iconbitmap('system/assets/aa_logo.ico')

    lbl_preset = Label(window_preset, text = 'Preset name:')
    lbl_preset.place(x = 5, y = 10)

    entry_preset = Entry(window_preset, width = 25)
    entry_preset.place(x = 80, y = 10)

    btn_cancel = Button(window_preset, text = 'Cancel', command = lambda: window_preset.destroy())
    btn_cancel.place(x = 30, y = 50)

    btn_done = Button(window_preset, text = 'Done', command = lambda: name_preset(combo_order, window_preset, entry_preset, combo_repeat))
    btn_done.place(x = 140, y = 50)

    window_preset.mainloop()