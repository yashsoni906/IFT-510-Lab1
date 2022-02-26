import os
import sys
import pprint
import re
from pynput import keyboard as ky

print(f"Welcome to My terminal")


stat = False


def pause():
    print('Application paused.')

    def on_press(key):
        if key == ky.Key.enter:
            return False

    def on_release(key):
        try:
            print('Press Enter key to Resume'.format(key.char))
        except AttributeError:
            print('Press Enter key to start'.format(key))

    with ky.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def file_return(cmd):
    if re.search(' > ', cmd):
        stat = True
        f = open(cmd.split()[-1], 'w')
    elif re.search(' >> ', cmd):
        stat = True
        f = open(cmd.split()[-1], 'a')
        print(file=f)
    return f


while (True):
    PATH = os.getcwd()
    cmd = input(f"{PATH}>")
    stat = False

    if re.search("^(cd)", cmd):
        if re.search(' > ', cmd):
            stat = True

        s = cmd.split()
        fd = s[1]
        try:
            os.chdir(fd)
        except:
            print("Exception thrown")
            print(sys.exc_info()[1])

    elif re.search('^(clr)', cmd):
        os.system('cls' if os.name == 'nt' else 'clear')

    elif re.search('^(dir)', cmd):
        if re.search(' > | >> ', cmd):
            f = file_return(cmd)
            stat = True
        print(stat)
        for p in os.listdir(PATH):
            print(p, file=f if stat else None)

    elif re.search('^(environ)', cmd):
        if re.search(' > | >> ', cmd):
            f = file_return(cmd)
            stat = True
        pprint.pprint(dict(os.environ), width=1, stream=f if stat else None)
        f.close() if stat else None

    elif re.search('^(echo)', cmd):
        if re.search(' > | >> ', cmd):
            f = file_return(cmd)
            stat = True

        e = cmd.split()
        [print(i, end=" ", file=f if stat else None) for i in (e[1:-2] if stat else e[1:])]
        print('\n')

        f.close() if stat else None



    elif re.search('^(help)', cmd):
        if re.search(' > | >> ', cmd):
            f = file_return(cmd)
            stat = True
        print("""\n 'cd' <directory> : change the current default directory to <directory>.\n
        \n 'clr' : clear the screen. \n
        \n 'dir' <directory> : list the contents of directory. \n
        \n 'environ' : list all the environment strings. \n
        \n 'echo' <comment> :display <comment> on the display followed by a new line.  \n
        \n 'help' : display a list of all commands and their inputs/behaviors. \n""", file=f if stat else None)
        print("\n 'pause : pause")
        

    elif re.search('^(pause)', cmd):
        pause()

    elif re.search('^(exit|quit)', cmd):
        break


    elif re.search('\S*\s*', cmd):
        try:
            d = cmd.split()[0]

        except:
            continue

        print(f"'{d}' is not recognized as an internal or external command,\noperable program or batch file.")
        continue
