import pyautogui as pag

def xmouse(coordinates: str) -> str:
    return "mouse " + coordinates

ALLOWABLE_HOTKEYS = ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
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

def toprint(string: str) -> str:
    return f"""print('''{string}''')"""

# turn commands into file text
def xform(commands: str) -> str:
    builder = ["""\
import time
import pyautogui as pag
pag.FAILSAFE = True
"""]

    commands = commands.splitlines()
    for i, line in enumerate(commands):
        words = line.split()
        if not words: continue

        if words[0] == '#':
            builder.append(" ".join(words))

        elif words[0] == 'mouse':
            if len(words) < 3:
                print("Invalid mouse command on line", i+1)
                return None
            if not words[1].endswith(','):
                print("Invalid mouse command on line", i+1, "Missing ','")
                return None

            x = words[1] # contains a trailing comma
            y = words[2]
            builder.append(toprint(line))
            builder.append(f"pag.moveTo({x} {y})")

        elif words[0] == 'click':
            builder.append(toprint(line))
            builder.append("pag.click()")
        elif words[0] == 'click2':
            builder.append(toprint(line))
            builder.append("pag.doubleClick()")
        elif words[0] == 'click3':
            builder.append(toprint(line))
            builder.append("pag.tripleClick()")
        elif words[0] == 'rclick':
            builder.append(toprint(line))
            builder.append("pag.rightClick()")

        elif words[0] == 'pause':
            builder.append("input('Press <Enter> to continue...')")
        
        elif words[0] == 'hotkey':
            if len(words) < 2:
                print("Hotkey on line", i+1, "is missing hotkeys")
                return None
            if not all(word in ALLOWABLE_HOTKEYS for word in words[1:]):
                print("Hotkey on line", i+1, "has an invalid hotkey")
                return None

            tmp = "pag.hotkey("
            for j, word in enumerate(words[1:]):
                tmp += f"'{word}'"
                if j + 1 < len(words[1:]):
                    tmp += ', '
            tmp += ")"
            builder.append(toprint(line))
            builder.append(tmp)
        
        elif words[0] == 'type' or words[0] == 'typeln':
            if len(words) < 2:
                print("Type on line", i+1, "is missing words")
                return None

            newline = " ".join(words[1:])
            builder.append(toprint(line))
            builder.append(f'''pag.write("""{newline}""")''')
            if words[0] == 'typeln':
                builder.append("pag.hotkey('enter')")
        
        elif words[0] == 'enter':
            builder.append("pag.hotkey('enter')")

        elif words[0] == 'sleep':
            if len(words) < 2:
                print("Sleep on line", i+1, "is missing a time")
                return None
            builder.append(f"time.sleep({words[1]})")

        else:
            print("Unknown command on line", i+1)
            return None

    transformed = "\n".join(builder)
    return transformed
