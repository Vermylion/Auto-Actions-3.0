from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

def help():
    helpmsg1 = messagebox.askokcancel(title = 'General Use (1/4)', message = 
'''CREATE ACTION: To create a new action and start creating your sequence, simply press on the button 'Add Action', and you're good to go! In the case of selecting 'Mouse CLick' as an action type, it is needed to click on the screen to record the click position. Don't worry, you can change it later! To navigate from action to action, use the dropdown next to 'For Action'.

UNDO REDO: Undo allows you to delete the action you just made, and Redo to add it back. Be warned: if you create a new action, any action removed with Undo will not be saved, and will be gone forever.

ACTION TYPES: There are 3 action types; Mouse CLick, Text Typing and Key Input. the basic settings for Mouse lets you select which button to press, in Text you must write down what text you want it to type, and in Key what key to press (key combinations with '+' are possible).

DELAY: Default delay time (how long it will take for the action to execute) is set to 0.5 seconds, and can be changed manually. Default delay type is set for the whole sequence. If you want each individual action to have a different delay time, simply select 'Per Action' in the Delay Time section.

REPEAT: Select how many times the sequence will repeat itself. If you select 'Unlimited' in the Repeat dropdown, the sequence will not stop repeating until you stop it manually or using the stop key shortcut (default Alt + C).
'''
)
    if helpmsg1:
        helpmsg2 = messagebox.askokcancel(title = 'Advanced Action Settings (2/4)', message = 
'''INFO: Press down on the '+' icon next to the action settings for more advanced settings.

MOUSE CLICK SETTINGS: In the advanced settings, you have the possibility to manually change the press and release x and y coordinates (where the mouse clicks) as well as how long the button is pressed for (automatically imputed).

TEXT TYPING SETTINGS: The only advanced setting here is to modify how quickly the app will type the letters (if the delay is at 0, it will be typed automatically, otherwise the letters will be typed one by one).

KEY INPUT SETTINGS: The avanced settings for this action type corresponds to the key release delay.

ACTION SETTINGS (ADVANCED): This might be the most complicated setting to use correctly; if 'Wait until Action Finished' is selected, the upcoming action will wait until said action has finished, otherwise, the only delay will be the upcoming action's delay. Selecting 'Action won't hold up others' is like making the action transparent, with no added delay. Of course, it will still execute after it's own delay, and same thing applies for the upcoming action.
'''
)
        if helpmsg2:
            helpmsg3 = messagebox.askokcancel(title = 'Hotkeys (3/4)', message = 
'''USE HOTKEYS: Both 'Play' and 'Stop' are set to the same hotkey, 'Alt + C'. Pressing 'Alt + C' will start the sequence, and stop it in consequence. These Hotkeys can also be set manually, and each 'Play' and 'Stop' can have different hotkeys.

SET HOTKEYS: When pressing the button 'Set Hotkeys', a new window will open, allowing you to select either a pre-defined hotkey or type in your own (keys can be linked together for a hotkey using '+'). It should be noted that both 'Start' and 'Stop' can be set differently.
'''
)
            if helpmsg3:
                messagebox.askokcancel(title = 'Presets (4/4)', message =
'''USE PRESETS: To use presets, click on the dropdown in the 'Preset' section, and select which preset you wish to open up. Doing so will open up a series of warnings, as when a preset is selected, you can not go back. You also have the choice to resize the mouse clicking positions to your screen resolution, as they may not be the same as on the preset (in case of switched monitor or computer). The popup will always be present, even if the resolution is the same. WARNING: Clicking coordinates will only be resized for the main monitor. Any secondary monitors will not be taken into account.

CREATE PRESET: To create a new preset, click the button 'Add...' in the Preset section. A new window will appear, prompting for a preset name. When entered correctly (without \, /, :, *, ?, ", <, >, |, and name not already in use), the current sequence will automatically be saved and will become accessible. You can now reuse and reaccess this sequence whenever!
''' 
)
    return