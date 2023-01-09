from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import keyboard
from PIL import ImageTk, Image
import system.Auto_System as Auto_System
import system.Preset_Window as Preset_Window
import system.Hotkey_Window as Hotkey_Window
import system.Help_Function as Help_Function
import os

placeoffset = 0
delayswitch = False
defaultsize = 'small'
defaulttype = 'click'
settingsoffset = 0
addedoffset = 0
scroll_height = 0
last_selectedAction = 0
play_down = False

typeslist = ['click', 'text', 'key']

actionTypes = {}

def check_key():
    global actionTypes
    actionTypes = Auto_System.actionTypes
    currentActions = Auto_System.currentActions
    for x in range(len(actionTypes)):
        if actionTypes[x + 1] == 'key':
            try:
                keyboard.release(currentActions[x + 1][0])
            except:
                messagebox.showwarning(title = 'Invalid Key Name', message = f'Invalid key name for Key Input for Action {x + 1}.')
                return
        try:
            if combo_repeat.get().lower() != 'unlimited':
                int(float(combo_repeat.get()))
        except:
            messagebox.showwarning(title = 'Invalid Repeat Input', message = f"'{combo_repeat.get()}' is not a valid repeat option.")
            return
    btn_play.config(state = 'disabled')
    btn_stop.config(state = 'enabled')
    Auto_System.play(combo_repeat, window, btn_play, btn_stop)

def stop():
    Auto_System.stop()

def play_key():
    global play_down
    if keyboard.is_pressed(Hotkey_Window.hotkey_start.lower()) and Auto_System.playing == False and play_down == False:
        window.after(0, play)
        play_down = True
    if not keyboard.is_pressed(Hotkey_Window.hotkey_start.lower()):
        play_down = False
        
    btn_play['text'] = f"Play ({Hotkey_Window.hotkey_start})"
    btn_stop['text'] = f"Stop ({Hotkey_Window.hotkey_stop})"
    window.after(20, play_key)

def play():
    global last_selectedAction
    try:
        last_selectedAction = int(combo_order.get())
        update_actions(None)
        window.after(5, check_key())
    except:
        pass

def action_delay():
    global placeoffset, delayswitch
    if delayswitch:
        return
    lbl_action.place(x = 10, y = 5)
    entrys_action.place(x = 93, y = 5)
    lbl2_action.place(x = 130, y = 5)
    placeoffset = 25
    delayswitch = True
    showMore(defaulttype, defaultsize, addedoffset + 25)
    MoreActionSettings()
    Auto_System.update_delay(entry_delay.get(), int(var_delay.get()))
    entrys_action.delete(0, 'end')
    entrys_action.insert(0, entry_delay.get())

def sequence_delay():
    global placeoffset, delayswitch
    if not delayswitch:
        return
    lbl_action.place_forget()
    entrys_action.place_forget()
    lbl2_action.place_forget()
    placeoffset = 0
    delayswitch = False
    showMore(defaulttype, defaultsize, addedoffset - 25)
    MoreActionSettings()
    
def MoreActionSettings():
    global placeoffset
    if btn_actionMore['image'] == ('pyimage2',):
        radio_action.place(x = 10, y = 5 + placeoffset)
        radio2_action.place(x = 10, y = 25 + placeoffset)
        lblf_action.config(height = 70 + placeoffset)
    else:
        radio_action.place_forget()
        radio2_action.place_forget()
        lblf_action.config(height = 25 + placeoffset)

def insert_settings():
    global actionTypes, last_selectedAction
    actionTypes = Auto_System.actionTypes
    currentActions = Auto_System.get_actions()
    actionDelay = Auto_System.actionDelay
    actionWait = Auto_System.actionWait

    entrys_action.delete(0, 'end')
    entrys_action.insert(0, actionDelay[int(combo_order.get())])

    var_action.set(actionWait[int(combo_order.get())])

    if actionTypes[int(combo_order.get())] == 'click':
        click_type = currentActions[int(combo_order.get())][2]
        if click_type == 'left':
            combo_click.current(0)
        if click_type == 'right':
            combo_click.current(2)
        if click_type == 'middle':
            combo_click.current(1)
        entryx_click.delete(0, 'end')
        entryy_click.delete(0, 'end')
        entryx2_click.delete(0, 'end')
        entryy2_click.delete(0, 'end')
        entrys_click.delete(0, 'end')

        entryx_click.insert(0, str(currentActions[int(combo_order.get())][0]))
        entryy_click.insert(0, str(currentActions[int(combo_order.get())][1]))
        entryx2_click.insert(0, str(currentActions[int(combo_order.get())][4]))
        entryy2_click.insert(0, str(currentActions[int(combo_order.get())][5]))
        entrys_click.insert(0, str(currentActions[int(combo_order.get())][3]))
    if actionTypes[int(combo_order.get())] == 'text':
        entry_text.delete(0, 'end')
        entrys_text.delete(0, 'end')

        entry_text.insert(0, str(currentActions[int(combo_order.get())][0]))
        entrys_text.insert(0, str(currentActions[int(combo_order.get())][1]))
    if actionTypes[int(combo_order.get())] == 'key':
        combo_key.delete(0, 'end')
        combo_key.insert(0, currentActions[int(combo_order.get())][0])
        entrys_key.delete(0, 'end')
        entrys_key.insert(0, str(currentActions[int(combo_order.get())][1]))

    last_selectedAction = int(combo_order.get())

def update_actions(type):
    global actionTypes, last_selectedAction
    actionTypes = Auto_System.actionTypes

    currentActions = Auto_System.get_actions()
    totalActions = Auto_System.totalActions

    actionDelay = Auto_System.actionDelay
    totalDelay = Auto_System.totalDelay

    actionWait = Auto_System.actionWait
    totalActionWait = Auto_System.totalActionWait

    if int(var_delay.get()) == 2:
        actionDelay[last_selectedAction] = entrys_action.get()
    else:
        Auto_System.update_delay(entry_delay.get(), int(var_delay.get()))

    if len(actionTypes) < 1:
            return

    actionWait[last_selectedAction] = int(var_action.get())

    if actionTypes[last_selectedAction] == 'click':
        currentActions[last_selectedAction][2] = combo_click.get().lower()

        currentActions[last_selectedAction][0] = int(float(entryx_click.get()))
        currentActions[last_selectedAction][1] = int(float(entryy_click.get()))
        currentActions[last_selectedAction][4] = int(float(entryx2_click.get()))
        currentActions[last_selectedAction][5] = int(float(entryy2_click.get()))
        currentActions[last_selectedAction][3] = float(entrys_click.get())

    if actionTypes[last_selectedAction] == 'text':
        currentActions[last_selectedAction][0] = str(entry_text.get())
        currentActions[last_selectedAction][1] = float(entrys_text.get())

    if actionTypes[last_selectedAction] == 'key':
        currentActions[last_selectedAction][0] = str(combo_key.get())
        currentActions[last_selectedAction][1] = float(entrys_key.get())

    if type == None:
        totalActions[last_selectedAction] = currentActions[last_selectedAction]
        totalDelay[last_selectedAction] = actionDelay[last_selectedAction]
        totalActionWait[last_selectedAction] = actionWait[last_selectedAction]
        
    last_selectedAction = int(combo_order.get())

def update_scroll(offset):
    second_frame.configure(height = frame_height + offset)
    canvas.configure(scrollregion = canvas.bbox("all"))
    if second_frame['height'] < 300:
        scrollbar.place_forget()
        windowgeo(height, width)
    else:
        windowgeo(height, width + 17)
        scrollbar.place(x = width, y = 0, height = height)

def forgetTypes():
    lblf_click.place_forget()
    lblf_key.place_forget()
    lblf_text.place_forget()

def showMore(types, size, offset):
    global defaultsize, defaulttype, settingsoffset, addedoffset, last_selectedAction
    for x in typeslist:
        if types != x:
            globals()['lblf_' + x].place_forget()

    var = 'lblf_' + types
    globals()[var].place(x = 230, y = 188)
    if size == 'large':
        if types == 'click':
            globals()[var]['height'] = 142
        else:
            globals()[var]['height'] = 82
    else:
        globals()[var]['height'] = 52
    h = globals()[var]['height']

    if types != 'click':
        last_selectedAction = int(combo_order.get())
    lblf_action.place(x = 230, y = 188 + h + 8)
    btn_actionMore.place(x = 405, y = 188 + h + 8)
    radio2_delay.config(state = 'enabled')
    btn_moreSettings.place(x = 405, y = 188)

    if offset == None:
        offset = addedoffset

    update_scroll(h - 52 + offset)
    
    defaultsize, defaulttype, addedoffset = size, types, offset

def record_loop():
    global scroll_height, last_selectedAction
    file = open('system/function.txt', 'r')
    txt = file.readline()
    file.close()
    if txt == 'Done\n':
        file = open('system/function.txt', 'w')
        file.write('None\n')
        file.write('None')
        file.close()
        update_scroll(scroll_height)
        scroll_height = 0
        last_selectedAction = int(combo_order.get())
        window.after(5, insert_settings)
    else:
        window.after(5, record_loop)

def record_click(types, combo_order, delay):
    global scroll_height
    canvas_prompt.place(x = 220, y = 180)
    lbl_prompt.config(text = ''' Click Anywhere to 
record mouse click!''')
    btn_actionSelect.config(state = 'disabled')
    scroll_height = second_frame['height'] - frame_height
    window.after(10, lambda: update_scroll(-100))
    Auto_System.record(window, types, combo_order, delay, btn_actionSelect, canvas_prompt, int(var_delay.get()), 1)
    record_loop()

def NewAction():
    global actionTypes, defaultsize, last_selectedAction
    var = var_actionSelect.get()
    delay = entry_delay.get()
    canvas_prompt.place_forget()
    
    if actionTypes != {}:
        last_selectedAction = int(combo_order.get())
        update_actions(None)

    if var == 1:
        types = 'click'
        record_click(types, combo_order, delay)
    if var == 2:
        types = 'text'
        settings = ['', 0]
    if var == 3:
        types = 'key'
        settings = ['Enter', 0]
        
    if not var == 1:
        Auto_System.NewAction(types, combo_order, settings, delay, int(var_delay.get()), 1)
        actionTypes = Auto_System.actionTypes
        window.after(5, insert_settings)

    showMore(types, defaultsize, addedoffset)
    btn_undo.config(state = 'enabled')
    btn_redo.config(state = 'disabled')

def preset():
    update_actions(None)
    Preset_Window.preset(combo_preset, combo_repeat)

def preset_loop():
    global actionTypes, order_list
    file = open('system/function.txt', 'r')
    file.readline()
    txt = file.readline()
    file.close()
    if txt == 'Done':
        file = open('system/function.txt', 'w')
        file.write('None\n')
        file.write('None')
        file.close()
        actionTypes = Auto_System.actionTypes
        order_list = []
        for x in range(1, len(actionTypes) + 1):
            order_list.append(x)
        combo_order.config(values = order_list)
        combo_order.current(len(order_list) - 1)
        Auto_System.send_order_list(order_list)
        showMore(actionTypes[int(combo_order.get())], defaultsize, addedoffset)
        canvas_prompt.place_forget()
        combo_repeat.delete(0, 'end')
        combo_repeat.insert(0, Auto_System.preset_repeat)
        btn_undo['state'] = 'enabled'
        var_delay.set(2)
        entry_delay['state'] = 'disabled'
        lbl_delay['state'] = 'disabled'
        action_delay()
        window.after(5, insert_settings)
    else:
        window.after(5, preset_loop)

def import_preset():
    if not combo_preset.get() == '':
        Preset_Window.ask_preset(combo_preset)
        preset_loop()

def reset(resetbtn):
    global order_list
    order_list = []
    combo_order.config(values = order_list)
    combo_order.set('')
    lbl_prompt.config(text = 'Create a new Action!')
    canvas_prompt.place(x = 220, y = 180)
    radio2_delay.config(state = 'disabled')
    btn_undo.config(state = 'disabled')
    window.after(10, lambda: update_scroll(0))
    if resetbtn:
        btn_redo.config(state = 'disabled')

def undo():
    global actionTypes, last_selectedAction
    actionTypes = Auto_System.actionTypes
    last_selectedAction = int(combo_order.get())
    if not len(actionTypes) <= 1:
        pass
        #update_actions('undo')
    Auto_System.undo(combo_order, btn_redo)
    actionTypes = Auto_System.actionTypes
    if actionTypes == {}:
        reset(False)
        return
    
    showMore(actionTypes[len(actionTypes)], defaultsize, addedoffset)
    window.after(5, insert_settings())

def redo():
    global actionTypes, last_selectedAction
    #update_actions('redo')
    Auto_System.redo(combo_order, btn_undo, btn_redo)
    actionTypes = Auto_System.actionTypes
    canvas_prompt.place_forget()
    showMore(actionTypes[len(actionTypes)], defaultsize, addedoffset)
    window.after(10, insert_settings())

def validate(value_if_allowed):
    if value_if_allowed == '':
        return True
    if value_if_allowed:
        try:
            float(value_if_allowed)
            return True
        except:
            return False
    else:
        return False
        
#Defining the tkinter window
window = Tk()

height = 280
width = 430
def windowgeo(h, w):
    wh = str(w) + 'x' + str(h)
    window.geometry(wh)
windowgeo(height, width)

window.title('Auto Actions 3.0')
window.resizable(0, 0)
window.attributes('-topmost', True)

window.iconbitmap('system/assets/aa_logo.ico')

vcmd = (window.register(validate), '%P')
# Create A Main Frame
main_frame = Frame(window, width = width + 17, height = height)
main_frame.place(x = 0, y = 0)

# Create A Canvas
canvas = Canvas(main_frame, width = width + 5, height = height + 5)
canvas.place(x = -5, y = -5)

# Add A Scrollbar To The Canvas
scrollbar = Scrollbar(main_frame, orient = VERTICAL, command = canvas.yview)
scrollbar.place(x = width, y = 0, height = height)
scrollbar.place_forget()

# Configure The Canvas
canvas.configure(yscrollcommand = scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

def _on_mouse_wheel(event):
    canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

# Create ANOTHER Frame INSIDE the Canvas
frame_height = height + 5
second_frame = Frame(canvas, width = width + 5, height = frame_height)

# Add that New frame To a Window In The Canvas
canvas.create_window(0, 0, window = second_frame, anchor = "nw")

#Preset part GUI (Concept/temporary)
lblf_preset = LabelFrame(window, text = 'Preset:', width = 205, height = 55)
lblf_preset.place(x = 10, y = 10)

values_preset = ['']

combo_preset = Combobox(lblf_preset, width = 17, values = values_preset, state = 'readonly')
combo_preset.place(x = 10, y = 6)
combo_preset.bind('<<ComboboxSelected>>', lambda e: import_preset())

values_preset = Auto_System.update_presets(combo_preset, '')

btn_preset = Button(lblf_preset, text = 'Add...', width = 6, command = preset)
btn_preset.place(x = 145, y = 4)

#Delay part GUI
lblf_delay = LabelFrame(window, text = 'Delay Time: ', width = 205, height = 70)
lblf_delay.place(x = 10, y = 70)

var_delay = IntVar()
radio_delay = Radiobutton(lblf_delay, variable = var_delay, text = 'For sequence:', value = 1, command = lambda: (entry_delay.config(state = 'enabled'), lbl_delay.config(state = 'enabled'), sequence_delay()))
radio_delay.place(x = 10,  y = 5)
radio2_delay = Radiobutton(lblf_delay, variable = var_delay, text = 'Per Action.', value = 2, command = lambda: (entry_delay.config(state = 'disabled'), lbl_delay.config(state = 'disabled'), action_delay()), state = 'disabled')
radio2_delay.place(x = 10,  y = 25)
var_delay.set(1)

entry_delay = Entry(lblf_delay, width = 4, validate = 'key', validatecommand = vcmd)
entry_delay.place(x = 110, y = 6)
entry_delay.insert(0, "0.5")

lbl_delay = Label(lblf_delay, text = "seconds")
lbl_delay.place(x = 145, y = 6)

#Repeat part GUI
lblf_repeat = LabelFrame(window, text = 'Repeat: ', width = 205, height = 55)
lblf_repeat.place(x = 10, y = 145)

lbl_repeat = Label(lblf_repeat, text = 'Repeat                                      times')
lbl_repeat.place(x = 10, y = 5)

combo_repeat = Combobox(lblf_repeat, width = 12, values = ('1', '2', '3', '5', '10', '20', '50', '100', 'Unlimited'))#, validate = 'key', validatecommand = vcmd)
combo_repeat.current(0)
combo_repeat.place(x = 57, y = 5)

#App control buttons (default state)
#button play: set command to also trigger update_actions
btn_play = Button(window, text = f"Play ({Hotkey_Window.hotkey_start})", width = 14, command = play)
btn_play.place(x = 9, y = 210)

btn_stop = Button(window, text = f'Stop ({Hotkey_Window.hotkey_stop})', width = 14, state = 'disabled', command = stop)
btn_stop.place(x = 121, y = 210)

btn_reset = Button(window, text = "Set Hotkeys", width = 14, command = Hotkey_Window.hotkey)
btn_reset.place(x = 9, y = 245)

btn_help = Button(window, text = 'Help', width = 14, command = Help_Function.help)
btn_help.place(x = 121, y = 245)

#Action Selection (from click, to text input, to key input) GUI
lblf_actionSelect = LabelFrame(second_frame, text = 'Choose Action Type:', width = 185, height = 140)
lblf_actionSelect.place(x = 230, y = 13)

var_actionSelect = IntVar()
#Text definition needs work
radio_actionSelect = Radiobutton(lblf_actionSelect, variable = var_actionSelect, text = 'Mouse Click', value = 1)
radio_actionSelect.place(x = 10, y = 5)

radio2_actionSelect = Radiobutton(lblf_actionSelect, variable = var_actionSelect, text = 'Text Typing', value = 2)
radio2_actionSelect.place(x = 10, y = 27)

radio3_actionSelect = Radiobutton(lblf_actionSelect, variable = var_actionSelect, text = 'Key Input', value = 3)
radio3_actionSelect.place(x = 10, y = 49)
var_actionSelect.set(1)

btn_undo = Button(lblf_actionSelect, text = 'Undo', width = 5, state = 'disabled', command = undo)
btn_undo.place(x = 5, y = 85)

btn_actionSelect = Button(lblf_actionSelect, text = 'Add Action', command = NewAction)
btn_actionSelect.place(x = 52, y = 85)

btn_redo = Button(lblf_actionSelect, text = 'Redo', width = 5, state = 'disabled', command = redo)
btn_redo.place(x = 135, y = 85)

#Action to modify selection (combobox selec.)
lbl_order = Label(second_frame, text = 'For Action')
lbl_order.place(x = 270, y = 160)

order_list = []
combo_order = Combobox(second_frame, width = 3, values = order_list, state = 'readonly')
combo_order.place(x = 335, y = 160)
combo_order.bind('<<ComboboxSelected>>', lambda e: (Auto_System.update_delay(entry_delay.get(), int(var_delay.get())), update_actions(None), window.after(2, showMore(actionTypes[int(combo_order.get())], defaultsize, addedoffset)), window.after(5, insert_settings)))

lbl2_order = Label(second_frame, text = ':', font = ('TkDefaultFont', 9, 'bold'))
lbl2_order.place(x = 380, y = 160)

#Click settings large GUI; large = 145
lblf_click = LabelFrame(second_frame, text = 'Mouse Click Settings:', width = 185, height = 55)
lblf_click.place(x = 230, y = 188)
  
lbl_click = Label(lblf_click, text = 'Mouse Click:')
lbl_click.place(x = 10, y = 5)

combo_click = Combobox(lblf_click, values = ('Left', 'Middle', 'Right'), state = 'readonly', width = 7)
combo_click.current(0)
combo_click.place(x = 90, y = 5)

lbl2_click = Label(lblf_click, text = 'Press:  x:              y:')
lbl2_click.place(x = 10, y = 35)

entryx_click = Entry(lblf_click, width = 4, validate = 'key', validatecommand = vcmd)
entryx_click.place(x = 62, y = 35)

entryy_click = Entry(lblf_click, width = 4, validate = 'key', validatecommand = vcmd)
entryy_click.place(x = 112, y = 35)

lbl3_click = Label(lblf_click, text = 'Release:  x:              y:')
lbl3_click.place(x = 10, y = 65)

entryx2_click = Entry(lblf_click, width = 4, validate = 'key', validatecommand = vcmd)
entryx2_click.place(x = 74, y = 65)

entryy2_click = Entry(lblf_click, width = 4, validate = 'key', validatecommand = vcmd)
entryy2_click.place(x = 124, y = 65)

lbl4_click = Label(lblf_click, text = 'Release Delay:')
lbl4_click.place(x = 10, y = 95)

entrys_click = Entry(lblf_click, width = 4, validate = 'key', validatecommand = vcmd)
entrys_click.place(x = 95, y = 95)

lbl5_click = Label(lblf_click, text = 'seconds')
lbl5_click.place(x = 130, y = 95)

lblf_click.place_forget()

#Text input settings large GUI; large = 85
lblf_text = LabelFrame(second_frame, text = 'Text Typing Settings:', width = 185, height = 55)
lblf_text.place(x = 230, y = 188)

lbl_text = Label(lblf_text, text = 'Text:')
lbl_text.place(x = 10, y = 5)

entry_text = Entry(lblf_text, width = 20)
entry_text.place(x = 45, y = 5)

lbl2_text = Label(lblf_text, text = 'Typing Delay:')
lbl2_text.place(x = 10, y = 35)

entrys_text = Entry(lblf_text, width = 4, validate = 'key', validatecommand = vcmd)
entrys_text.place(x = 93, y = 35)

lbl5_text = Label(lblf_text, text = 'seconds')
lbl5_text.place(x = 130, y = 35)

lblf_text.place_forget()

#Key input settings large GUI; large = 85
lblf_key = LabelFrame(second_frame, text = 'Key Input Settings:', width = 185, height = 55)
lblf_key.place(x = 230, y = 188)

lbl_key = Label(lblf_key, text = 'Key Input:')
lbl_key.place(x = 10, y = 5)

combo_key_values = ('Enter', 'Backspace', 'Tab', 'Esc', 'Ctrl + C', 'Ctrl + V', 'Left Shift', 'Right Shift', 'Caps Lock', 'Menu', 'Left Alt', 'Alt Gr', 'Left Ctrl', 'Right Ctrl', 'Delete', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'Left Windows') #Right Alt, Fn, Numpad Lock
combo_key = Combobox(lblf_key, width = 13, values = combo_key_values)
combo_key.current(0)
combo_key.place(x = 70, y = 5)

lbl2_key = Label(lblf_key, text = 'Release Delay:')
lbl2_key.place(x = 10, y = 35)

entrys_key = Entry(lblf_key, width = 4)
entrys_key.place(x = 95, y = 35)

lbl3_key = Label(lblf_key, text = 'seconds')
lbl3_key.place(x = 130, y = 35)

lblf_key.place_forget()

#More for actions settings GUI
lblf_action = LabelFrame(second_frame, text = 'Action Settings (Advanced):', width = 185, height = 25)
lblf_action.place(x = 230, y = 248)

lbl_action = Label(lblf_action, text = 'Action Delay:')
lbl_action.place(x = 10, y = 5)

entrys_action = Entry(lblf_action, width = 4, validate = 'key', validatecommand = vcmd)
entrys_action.place(x = 93, y = 5)

lbl2_action = Label(lblf_action, text = 'seconds')
lbl2_action.place(x = 130, y = 5)

var_action = IntVar()
radio_action = Radiobutton(lblf_action, variable = var_action, text = 'Wait until Action Finished', value = 1)
radio_action.place(x = 10,  y = 30)
radio2_action = Radiobutton(lblf_action, variable = var_action, text = "Action won't hold up others", value = 2)
radio2_action.place(x = 10,  y = 50)
var_action.set(1)

#Action GUI defaults
lbl_action.place_forget()
entrys_action.place_forget()
lbl2_action.place_forget()

radio_action.place_forget()
radio2_action.place_forget()

#Button => Expanding for advanced settings
def changeImage1():
    global frame_height
    if btn_moreSettings['image'] == ('pyimage1',):
        btn_moreSettings['image'] = minus_icon
        size = 'large'
    else:
        btn_moreSettings['image'] = plus_icon
        size = 'small'

    showMore(actionTypes[int(combo_order.get())], size, None)

def changeImage2():
    if btn_actionMore['image'] == ('pyimage1',):
        btn_actionMore['image'] = minus_icon
        showMore(defaulttype, defaultsize, addedoffset + 45)
    else:
        btn_actionMore['image'] = plus_icon
        showMore(defaulttype, defaultsize, addedoffset - 45)
    MoreActionSettings()

image = Image.open('system/assets/plus.png')
image = image.resize((10, 10), Image.LANCZOS)
plus_icon = ImageTk.PhotoImage(image)

image = Image.open('system/assets/minus.png')
image = image.resize((10, 10), Image.LANCZOS)
minus_icon = ImageTk.PhotoImage(image)

btn_moreSettings = Button(second_frame, image = plus_icon, command = changeImage1)
btn_moreSettings.place(x = 405, y = 188)

btn_actionMore = Button(second_frame, image = plus_icon, command = changeImage2)
btn_actionMore.place(x = 405, y = 247)
btn_actionMore.place(x = 405, y = 247)

#Label Frames defaults
forgetTypes()
lblf_action.place_forget()

#Button defaults
btn_moreSettings.place_forget()
btn_actionMore.place_forget()

#Starting label => prompting to create a new action (fill empty space)
canvas_prompt = Canvas(window, width = 200, height = 100)
canvas_prompt.place(x = 220, y = 180)
lbl_prompt = Label(canvas_prompt, text = 'Create a new Action!', font = ('TkDefaultFont', 11, 'bold'))
lbl_prompt.place(x = 30, y = 30)

window.after(20, play_key)
window.mainloop()