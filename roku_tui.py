#!/usr/bin/env python3

import urllib.request
import time
import curses
from configparser import ConfigParser
from pathlib import Path
import xml.etree.ElementTree as ET

class RokuConfig:

    def __init__(self, config_file):
        config = ConfigParser()
        config.read(config_file)
        self.ip = config['general']['roku_ip']

class RemoteKey:

    def __init__(self, hotkey, label, endpoint, y, x):
        self.hotkey = hotkey
        self.label = label
        self.endpoint = endpoint
        self.y = y
        self.x = x

class RokuRemote:

    def __init__(self, ip):
        self.base_url = 'http://{}:8060/'.format(ip)
        self.setup_keys()

    def setup_keys(self):
        self.keys = {}

        # first row
        self.keys['b'] = RemoteKey('b', 'Back', 'keypress/back', 1, 1)
        self.keys['h'] = RemoteKey('h', 'Home', 'keypress/home', 1, 10)

        # second row
        self.keys['r'] = RemoteKey('r', 'Repl', 'keypress/instantreplay', 13, 1)
        self.keys['*'] = RemoteKey('*', 'Star', 'keypress/info', 13, 10)

        # arrow keys
        self.keys['KEY_UP'] = RemoteKey('KEY_UP', '^', 'keypress/up', 4, 7)
        self.keys['KEY_LEFT'] = RemoteKey('KEY_LEFT', '<', 'keypress/left', 7, 1)
        self.keys['\n'] = RemoteKey('\n', 'OK!', 'keypress/select', 7, 6)
        self.keys['KEY_RIGHT'] = RemoteKey('KEY_RIGHT', '>', 'keypress/right', 7, 13)
        self.keys['KEY_DOWN'] = RemoteKey('KEY_DOWN', 'v', 'keypress/down', 10, 7)

        # third row
        self.keys['<'] = RemoteKey('<', '<<', 'keypress/rev', 16, 1)
        self.keys['p'] = RemoteKey('p', 'P', 'keypress/play', 16, 7)
        self.keys['>'] = RemoteKey('>', '>>', 'keypress/fwd', 16, 12)

def draw_key(stdscr, key, pressed=False):
    color = 1 if not pressed else 2
    draw_rect_key(stdscr, key.y, key.x, key.label, color)

def press_key(stdscr, key, base_url):
    draw_key(stdscr, key, True)
    stdscr.refresh()
    request_url = base_url + key.endpoint
    urllib.request.urlopen(request_url, b'')
    time.sleep(0.1)

def draw_rect_key(stdscr, y, x, text, colors):
    iw = len(text) + 2
    ow = iw + 2

    owf = "{:^" + str(ow) + "}"
    iwf = "{:^" + str(iw) + "}"

    # draw the box
    stdscr.addstr(y, x, owf.format('-' * iw))
    stdscr.addstr(y + 1, x, "|")
    stdscr.addstr(y + 1, x + ow - 1, "|")
    stdscr.addstr(y + 2, x, owf.format('-' * iw))

    # draw the inside
    if colors == 1:
        stdscr.addstr(y + 1, x + 1, iwf.format(text))
    elif colors == 2:
        stdscr.addstr(y + 1, x + 1, iwf.format(text), curses.A_STANDOUT)
        

def status(stdscr):
    stdscr.addstr(20, 1, "~*~ roku-cli ~*~")

def search_loop(stdscr, base_url):
    # setup for search
    stdscr.addstr(22, 1, '/')
    min_x = 2
    cur_x = min_x
    stdscr.move(22, cur_x)
    curses.curs_set(True)
    while 1:
        stdscr.refresh()
        letter = stdscr.getkey()
        if letter in ('\n', 'KEY_ESC'):
            stdscr.move(22, 0)
            stdscr.clrtoeol()
            curses.curs_set(False)
            return
        elif letter == '\x7f':
            if cur_x > min_x:
                cur_x -= 1
                stdscr.addstr(22, cur_x, " ")
                stdscr.move(22, cur_x)
                request_url = base_url + 'keypress/Backspace'
        else:
            stdscr.addstr(22, cur_x, letter)
            cur_x += 1
            if letter == ' ':
                letter = '%20'
            request_url = base_url + 'keypress/Lit_' + letter
        urllib.request.urlopen(request_url, b'')

def help_toggle(stdscr):
    
    help_lines = ["'h' -> Home",
                    "'b' -> Back",
                    "'p' -> Play/Pause",
                    "'r' -> Replay",
                    "'*' -> Options (star key)",
                    "arrow keys -> navigation",
                    "ENTER -> OK",
                    "'<' -> Rewind",
                    "'>' -> Fast-Forward",
                    "'/' -> Toggle typing mode (ENTER or ESC to leave)",
                    "'?' -> Show this help screen",
                    "'q' -> Quit",
                    "",
                    "Press any key to return to remote"]

    stdscr.clear()
    status(stdscr)
    for i in range(1,len(help_lines)+1):
        stdscr.addstr(i, 1, help_lines[i - 1])
    stdscr.getch()  # wait for keypress
    stdscr.clear()
    status(stdscr)

def remote_loop(stdscr, remote):
    while 1:
        # draw all the keys
        for k in remote.keys:
            draw_key(stdscr, remote.keys[k])

        # listen for an input
        c = stdscr.getkey()

        # if the input is in the mapped keys, press the key
        if c in remote.keys:
            press_key(stdscr, remote.keys[c], remote.base_url)
        elif c == '/':
            search_loop(stdscr, remote.base_url)
        elif c == '?':
            help_toggle(stdscr)
        elif c == 'q':
            break

def main(stdscr, config):

    init_curses()
    stdscr.clear()

    # create the remote
    remote = RokuRemote(config.ip)

    status(stdscr)

    remote_loop(stdscr, remote)

def init_curses():
    # set up colors
    curses.use_default_colors()

    # clear the screen and hide the cursor
    curses.curs_set(False)

def get_device_name(base_url):
    request_url = base_url + "query/device-info"
    out = urllib.request.urlopen(request_url)
    response = out.read().decode()
    root = ET.fromstring(response)
    return root.findall("model-name")[0].text

def init_run(config_file):
        print("Welcome to roku-cli!")
        print("Please enter the IP address of the Roku device you wish to control.")
        print("This can be found in the Settings > Network > About menu, ")
        print("or via your router.")
        print("You will only need to do this once.")
        print("If you wish to change the IP, modify the file at ~/.config/roku/roku.config")
        print()
        ip = input("IP Address: ")
        remote = RokuRemote(ip)

        # if this returns, the IP is valid
        device_name = get_device_name(remote.base_url)

        # write the config, create the directory if necessary
        if not config_file.parent.exists():
            config_file.parent.mkdir()
        config = ConfigParser()
        config["general"] = {"roku_ip": ip}
        with open(str(config_file), 'w') as cf:
            config.write(cf)
            
def startup():
    config_file = Path('~/.config/roku/roku.config').expanduser()
    if not config_file.exists():
        init_run(config_file)
    config = RokuConfig(config_file)
    curses.wrapper(main, config)

if __name__ == '__main__':
    startup()
