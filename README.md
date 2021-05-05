# roku-cli
a command line TUI remote for Roku

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

To quit the application, type `q`.

## typing mode
In some instances, you may need to type something into a Roku screen 
(when searching or logging into a service, for example). This can be 
incredibly cumbersome using the standard navigation.

To enter typing mode, press `/`, and you will see a cursor appear below 
the remote. At this point, all alphanumeric keys (and backspace) will 
be interpreted literally and sent to the Roku.

To exit typing mode, press `ENTER` or `ESC`.

## install
Replace the default IP address in `roku.config` with the IP address of 
the Roku, then run:

```
make
sudo make install
```

Program can be started using `roku`.
