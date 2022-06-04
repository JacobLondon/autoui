Auto GUI Software
=================
Tool to automatically write pyautogui scripts.

Hotkeys
-------
<Ctrl+s>        Save text to the file in the URL bar
<Ctrl+o>        Open the file in the URL bar
<Ctrl+Alt>      Insert the mouse coordinates into the text

Commands
--------
mouse X, Y      Move the mouse to this position
click           Left click once
click2          Double left click
click3          Triple left click
rclick          Right click once

sleep NUMBER    Wait for a number of seconds, like 1.5 or 2...
pause           Wait for the user to press <Enter> to continue
hotkey SEQ      Perform a sequence of hotkeys
                ie.
                    hotkey ctrl f
                    hotkey win d
                    hotkey ctrl v
                    hotkey ctrl shift c
                    hotkey enter
                    hotkey alt tab
type WORDS      Type a sequence of words
                ie.
                    type How's it going?
typeln WORDS    Type a sequence of words an press <Enter> after
enter           Press the <Enter> key

# comment       If a line starts with a #, ignore it


Installing
----------
Visit: https://www.python.org/downloads/
Download Python
Run the installer -- Check ADD TO PATH during install's first window!!!!!!!!
Once installed, run the following in a cmd window:
    python -m pip install pyautogui

Running
-------
Run autogui.py
- Top left is where you are
- Line under top is a place to say the names of files
    - scripts/runstuff.txt
- You can write a file name, then press Save to save changes to that file
- You can open existing files with Open after typing in a name
- Play will run the currently opened file.
    - Play also saves to the text file in the URL bar

Tricks
------
1. Position a window so that you can make an alt tab hotkey to do stuff
2. Once you have clicked on AutoGUI, you can move your mouse without clicking, and press Ctrl+Alt to save the mouse command at that spot
3. Ensure all your windows are set up before running a macro with the Play button
4. If you are using the pause command, try doing alt tabbing back to AutoGUI / the command window before pausing so you just have to press Enter to continue


Allowable Hotkey Names
----------------------
['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
'browserback', 'browserfavorites', 'browserforward', 'browserhome',
'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
'command', 'option', 'optionleft', 'optionright']
