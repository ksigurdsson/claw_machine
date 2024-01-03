rshell: https://github.com/dhylands/rshell/blob/master/README.rst

relay HAT: https://github.com/sbcshop/Pico-Single-channel-Relay-HAT
Motor HAT: https://github.com/sbcshop/Pico-Motor-Driver

make .venv
rshell cp main.py /pyboard
rshell "repl ~ import machine ~ machine.soft_reset() ~"
screen /dev/tty.usbmodem1124301
ctrl-A d to detach from screen
