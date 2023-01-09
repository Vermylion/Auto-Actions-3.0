import mouse
import keyboard
import time as wait
from time import time
import os
from screeninfo import get_monitors
import ast
import system.Hotkey_Window as Hotkey_Window

actionTypes = {}
totalActionTypes = {}
currentActions = {}
totalActions = {}
actionDelay = {}
totalDelay = {}
actionWait = {}
totalActionWait = {}

order_list = []

start_press, end_press = 0, 0
check = 0
start, end = 0, 0
tactions = 0
start_timer, end_timer = 0, 0
preset_repeat = 0
preset_width, preset_height = 0, 0

playing = False
stop_down = False
change_res = False

nbrmonitors = get_monitors()
for x in range(len(nbrmonitors)):
    monitor = nbrmonitors[x]
    if monitor.is_primary == True:
        width = monitor.width
        height = monitor.height

def send_order_list(list):
    global order_list
    order_list = list

def stop():
    global repeat_done
    repeat_done = tactions + 10

def play(combo_repeat, window, btn_play, btn_stop):
    global repeat_done, action_done, tactions, start_timer, playing
    window.after(30, lambda: set_playing(True))
    print(combo_repeat.get())
    if combo_repeat.get().lower() != 'unlimited':
        tactions = len(actionWait) * (int(combo_repeat.get()))
    else:
        tactions = len(actionWait) * 2
    repeat_done = 0
    action_done = 0

    print('Types:', actionTypes)
    print('Delay:', actionDelay)
    print('Actions:', currentActions)
    print('Wait:', actionWait)

    def set_playing(set):
        global playing
        playing = set

    def setup(repeat_times):
        global check, currentActions, end_timer, playing

        delay = float(actionDelay[repeat_times]) * 1000
        check = delay
        if not repeat_done >= tactions:
            timer()
        else:
            end_timer = time()
            print(round(end_timer - start_timer, 3))
            btn_play.config(state = 'enabled')
            btn_stop.config(state = 'disabled')
            window.after(30, lambda: set_playing(False))

    def timer():
        global check
        if action_done != 0:
            return
        if check != 0:
            check -= 1
            window.after(1, timer)
        else:
            system()
            
    def system():
        global repeat_done, action_done, tactions

        action_nbr = (repeat_done % len(actionWait)) + 1

        repeat_done += 1
        if combo_repeat.get().lower() == 'unlimited':
            tactions += 1

        if actionWait == 3:
            setup((repeat_done % len(currentActions)) + 1)
            return
        else:
            if actionWait[action_nbr] == 1:
                action_done += 1
            if actionWait[action_nbr] == 2:
                actionWait[action_nbr] = 3

            if actionTypes[action_nbr] == 'click':
                window.after(0, click)
            if actionTypes[action_nbr] == 'text':
                window.after(0, text)
            if actionTypes[action_nbr] == 'key':
                window.after(0, key)

            setup((repeat_done % len(currentActions)) + 1)

    def stop_key():
        global stop_down
        if keyboard.is_pressed(Hotkey_Window.hotkey_stop.lower()) and playing == True and stop_down == False:
            stop()
            stop_down = True
        if not keyboard.is_pressed(Hotkey_Window.hotkey_stop.lower()):
            stop_down = False

        if not repeat_done >= tactions:
            window.after(20, stop_key)

    def click_release(use_action, action_nbr):
        global action_done, actionWait
        mouse_button, mousex_release, mousey_release = use_action[2], use_action[4], use_action[5]

        if change_res:
            mousex_release = round(mousex_release / preset_width * width)
            mousey_release = round(mousey_release / preset_height * height)

        mouse.move(mousex_release, mousey_release)
        wait.sleep(0.002)
        mouse.release(button = mouse_button)
        print(mouse_button, 'click released')

        if actionWait[action_nbr] == 1:
            action_done -= 1
        if actionWait[action_nbr] == 3:
            actionWait[action_nbr] = 2
    
        setup((repeat_done % len(currentActions)) + 1)

    def click():
        global change_res
        action_nbr = ((repeat_done - 1) % len(currentActions)) + 1
        use_action = currentActions[action_nbr]

        mousex, mousey, mouse_button, click_delay = use_action[0], use_action[1], use_action[2], use_action[3]

        if change_res:
            mousex = round(mousex / preset_width * width)
            mousey = round(mousey / preset_height * height)

        mouse.move(mousex, mousey)
        mouse.press(button = mouse_button)
        print(mouse_button, 'click pressed')
        window.after(int(click_delay * 1000), lambda: click_release(use_action, action_nbr))

    def progressive_typing(action_nbr, use_action, lttr_index):
        global action_done, actionWait
        keyboard.write(use_action[0][lttr_index])
        print(use_action[0][lttr_index], 'text')

        if lttr_index + 1 != len(use_action[0]):
            window.after(int(use_action[1] * 1000), lambda: progressive_typing(action_nbr, use_action, lttr_index + 1))
        else:
            if actionWait[action_nbr] == 1:
                action_done -= 1
            if actionWait[action_nbr] == 3:
                actionWait[action_nbr] = 2
        
            setup((repeat_done % len(currentActions)) + 1)

    def text():
        global action_done, actionWait
        action_nbr = ((repeat_done - 1) % len(currentActions)) + 1
        use_action = currentActions[action_nbr]

        if use_action[1] == 0:
            keyboard.write(use_action[0])
            print(use_action[0], 'text')

            if actionWait[action_nbr] == 1:
                action_done -= 1
            if actionWait[action_nbr] == 3:
                actionWait[action_nbr] = 2
        
            setup((repeat_done % len(currentActions)) + 1)
        else:
            window.after(0, lambda: progressive_typing(action_nbr, use_action, 0))

    def release_key(use_action, action_nbr):
        global action_done, actionWait
        keyboard.release(use_action[0].lower())
        print(use_action[0].lower(), 'click released')

        if actionWait[action_nbr] == 1:
            action_done -= 1
        if actionWait[action_nbr] == 3:
            actionWait[action_nbr] = 2
    
        setup((repeat_done % len(currentActions)) + 1)

    def key():
        action_nbr = ((repeat_done - 1) % len(currentActions)) + 1
        use_action = currentActions[action_nbr]

        keyboard.press(use_action[0].lower())
        print(use_action[0].lower(), 'click pressed')
        window.after(int(use_action[1] * 1000), lambda: release_key(use_action, action_nbr))

    start_timer = time()

    stop_key()
    setup(1)

def get_actions():
    return currentActions

def record(window, types, combo_order, delay, btn_actionSelect, canvas_prompt, var_delay, wait):
    global start_press
    mouse_click = []

    def release():
        global end_press
        if mouse.is_pressed(button = mouse_click[2]) == False:
            end_press = time()
            x, y = mouse.get_position()
            mouse_click.append(round(end_press - start_press, 2))
            mouse_click.append(x)
            mouse_click.append(y)
            print(mouse_click)
            btn_actionSelect.config(state = 'enabled')
            canvas_prompt.place_forget()
            file = open('system/function.txt', 'w')
            file.write('Done\n')
            file.write('None')
            file.close()
            NewAction(types, combo_order, mouse_click, delay, var_delay, wait)
            return
        else:
            window.after(10, release)
    
    if mouse.is_pressed(button = 'left'):
        x, y = mouse.get_position()
        mouse_click.append(x)
        mouse_click.append(y)
        mouse_click.append('left')
        start_press = time()
        release()
        return False

    elif mouse.is_pressed(button = 'right'):
        x, y = mouse.get_position()
        mouse_click.append(x)
        mouse_click.append(y)
        mouse_click.append('right')
        start_press = time()
        release()
        return False
    
    elif mouse.is_pressed(button = 'middle'):
        x, y = mouse.get_position()
        mouse_click.append(x)
        mouse_click.append(y)
        mouse_click.append('middle')
        start_press = time()
        release()
        return False
    else:
        window.after(20, lambda: record(window, types, combo_order, delay, btn_actionSelect, canvas_prompt, var_delay, wait))

def update_delay(delay, var_delay):
    global actionDelay, totalDelay
    if var_delay == 1:
        for x in range(len(actionTypes)):
            actionDelay[x + 1] = delay
            totalDelay = actionDelay.copy()

def NewAction(types, combo_order, settings, delay, var_delay, wait):
    global totalActionTypes, actionTypes, currentActions, totalActions, actionDelay, totalDelay, actionWait, totalActionWait

    actionTypes[len(actionTypes) + 1] = types
    totalActionTypes = actionTypes.copy()

    currentActions[len(currentActions) + 1] = settings
    totalActions = currentActions.copy()

    actionWait[len(actionWait) + 1] = wait
    totalActionWait = actionWait.copy()

    if var_delay == 1:
        update_delay(delay, var_delay)
    else:
        actionDelay[len(actionDelay) + 1] = delay
        totalDelay = actionDelay.copy()
    
    order_list.append(len(actionTypes))
    combo_order.config(values = order_list)
    combo_order.current(len(actionTypes) - 1)

def undo(combo_order, btn_redo):
    global actionTypes, currentActions, actionDelay, actionWait, order_list

    del actionTypes[len(actionTypes)]
    del currentActions[len(currentActions)]
    del actionDelay[len(actionDelay)]
    del actionWait[len(actionWait)]
    del order_list[len(actionTypes)]

    btn_redo.config(state = 'enabled')
    if actionTypes != {}:
        combo_order.config(values = order_list)
        combo_order.current(len(actionTypes) - 1)

def redo(combo_order, btn_undo, btn_redo):
    global totalActionTypes, actionTypes, currentActions, totalActions, actionDelay, totalDelay, actionWait, totalActionWait

    actionTypes[len(actionTypes) + 1] = totalActionTypes[len(actionTypes) + 1]
    currentActions[len(currentActions) + 1] = totalActions[len(currentActions) + 1]
    actionDelay[len(actionDelay) + 1] = totalDelay[len(actionDelay) + 1]
    actionWait[len(actionWait) + 1] = totalActionWait[len(actionWait) + 1]
    order_list.append(len(currentActions))

    btn_undo.config(state = 'enabled')
    combo_order.config(values = order_list)
    combo_order.current(len(currentActions) - 1)

    if actionTypes == totalActionTypes:
        btn_redo.config(state = 'disabled')

def update_presets(combo_preset, config_current):
    values_preset = ['']
    path = "presets"
    dir_list = os.listdir(path)
    for file in dir_list:
        print(values_preset.append(file.replace('.txt', '')))

    combo_preset.config(values = values_preset)
    combo_preset.current(values_preset.index(config_current))

    return values_preset

def import_preset(name, res):
    global totalActionTypes, actionTypes, currentActions, totalActions, actionDelay, totalDelay, actionWait, totalActionWait, preset_repeat, change_res, preset_width, preset_height

    change_res = res
    preset = open(f'presets/{name}.txt', 'r')
    preset_res = preset.readline()
    preset_width, preset_height = preset_res.split('x')
    preset_width, preset_height = int(preset_width), int(preset_height)
    print(preset_width, preset_height)

    dicti = preset.readline().removesuffix('\n').replace("'", '"')
    actionTypes = ast.literal_eval(dicti)
    totalActionTypes = actionTypes.copy()

    dicti = preset.readline().removesuffix('\n').replace("'", '"')
    currentActions = ast.literal_eval(dicti)
    totalActions = currentActions.copy()

    dicti = preset.readline().removesuffix('\n').replace("'", '"')
    actionDelay = ast.literal_eval(dicti)
    totalDelay = actionDelay.copy()

    dicti = preset.readline().removesuffix('\n').replace("'", '"')
    actionWait = ast.literal_eval(dicti)
    totalActionWait = actionWait.copy()

    preset_repeat = preset.readline().removesuffix('\n').replace("'", '"')

    print(actionTypes)
    print(actionDelay)
    print(currentActions)
    print(actionWait)
    print(preset_repeat)

    preset.close()

    funcfile = open('system/function.txt', 'w')
    funcfile.write('None\n')
    funcfile.write('Done')
    funcfile.close()

def create_preset(combo_preset, name, combo_repeat):
    global width, height

    print(name + '.txt')
    preset = open(f'presets/{name}.txt', 'w')

    print(str(width) + ' ' + str(height))
    res = str(width) + 'x' + str(height) + '\n'
    preset.write(res)

    preset.write(str(actionTypes) + '\n')
    preset.write(str(currentActions) + '\n')
    preset.write(str(actionDelay) + '\n')
    preset.write(str(actionWait) + '\n')
    preset.write(str(combo_repeat.get()))

    preset.close()

    update_presets(combo_preset, name)