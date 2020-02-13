#!/usr/bin/env python3

import requests
import time
import curses
from curses import wrapper

class RemoteKey:

    def __init__(self, hotkey, label, endpoint, y, x):
        self.hotkey = hotkey
        self.label = label
        self.endpoint = endpoint
        self.y = y
        self.x = x

ip = '192.168.1.1' # this is the ip of your roku
base_url = 'http://' + ip + ':8060/keypress/'
keys = {}

def populate_keys():
    keys['B'] = RemoteKey('X', 'Back', 'back', 1, 1)
    keys['H'] = RemoteKey('H', 'Home', 'home', 1, 10)

    # draw second row of keys
    keys['R'] = RemoteKey('R', 'Repl', 'instantreplay', 4, 1)
    keys['*'] = RemoteKey('*', 'Star', 'info', 4, 10)

    # draw arrow keys
    keys['KEY_UP'] = RemoteKey('KEY_UP', '^', 'up', 7, 7)
    keys['KEY_LEFT'] = RemoteKey('KEY_LEFT', '<', 'left', 10, 1)
    keys['\n'] = RemoteKey('\n', 'OK!', 'select', 10, 6)
    keys['KEY_RIGHT'] = RemoteKey('KEY_RIGHT', '>', 'right', 10, 13)
    keys['KEY_DOWN'] = RemoteKey('KEY_DOWN', 'v', 'down', 13, 7)

    # draw third row of keys
    keys['<'] = RemoteKey('<', '<<', 'rev', 16, 1)
    keys['P'] = RemoteKey('P', 'P', 'play', 16, 7)
    keys['>'] = RemoteKey('>', '>>', 'fwd', 16, 12)

def draw_key(stdscr, key, pressed=False):
    color = 1 if not pressed else 2
    draw_rect_key(stdscr, key.y, key.x, key.label, color)

def press_key(stdscr, key):
    draw_key(stdscr, key, True)
    stdscr.refresh()
    request_url = base_url + key.endpoint
    requests.post(request_url)
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
    stdscr.addstr(y + 1, x + 1, iwf.format(text), curses.color_pair(colors))

def status(stdscr):
    stdscr.addstr(20, 1, "~*~ roku-cli ~*~")

def main(stdscr):

    # clear the screen and hide the cursor
    stdscr.clear()
    curses.curs_set(False)

    # set the colors
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # populate the keys
    populate_keys()

    status(stdscr)

    # loop forever
    while 1:

        # draw all the keys
        for k in keys:
            draw_key(stdscr, keys[k])

        # listen for an input
        c = stdscr.getkey().upper()

        # if the input is in the mapped keys, press the key
        if c in keys:
            press_key(stdscr, keys[c])
        elif c == 'Q':
            break
            
# main wrapper
wrapper(main)
