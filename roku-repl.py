#!/usr/bin/env python3

import requests

ip = '192.168.1.1'  # this is your roku's IP
base_url = 'http://{}:8060/'.format(ip)

key_map = { 'play': 'keypress/play',
            'pause': 'keypress/play',
            'up': 'keypress/up',
            'down': 'keypress/down',
            'left': 'keypress/left',
            'right': 'keypress/right',
            'back': 'keypress/back',
            'home': 'keypress/home',
            'ok': 'keypress/select',
            'enter': 'keypress/select'
        }

def do_command(cmd):
    request_url = base_url + key_map.get(cmd)
    requests.post(request_url)

def active_roku():
    request_url = base_url + 'query/device-info'
    try:
        out = requests.get(request_url)
    except ConnectionRefusedError:
        return False

    if out.status_code == 200:
        return True
    else:
        return False

def main():

    if not active_roku():
        print("invalid roku IP :(")
        exit()

    print("~*~*~ roku remote ~*~*~\ntype '?' for help")
    while True:
        command = input("roku > ")

        # quit, if asked
        if command in ('q', 'quit', 'exit'):
            break
        elif command  in ('?', 'help'):
            print('  '.join(key_map.keys()))

        if command in key_map.keys():
            do_command(command)
            

if __name__ == "__main__":
    main()
