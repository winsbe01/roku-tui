# roku-tui
a command line TUI remote for Roku

## install and run
`me@computer ~$ python3 -m pip install roku-tui`
`me@computer ~$ roku-tui`

## basic usage
Keys on the left map to standard Roku remote buttons on the right
* `h` -> Home
* `b` -> Back
* `p` -> Play/Pause
* `r` -> Replay
* `*` -> Options (star key)
* arrow keys -> navigation
* `ENTER` -> OK
* `<` -> Rewind
* `>` -> Fast-Forward

For help inside the application, type '?'.
To quit the application, type `q`.

## typing mode
In some instances, you may need to type something into a Roku screen 
(when searching or logging into a service, for example). This can be 
incredibly cumbersome using the standard navigation.

To enter typing mode, press `/`, and you will see a cursor appear below 
the remote. At this point, all alphanumeric keys (and backspace) will 
be interpreted literally and sent to the Roku.

To exit typing mode, press `ENTER` or `ESC`.

NOTE: this doesn't work with all text interfaces.
