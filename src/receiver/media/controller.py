import subprocess

from media.KeyCodes import Next, Prev, Play, VolumeDown, VolumeUp, Mute


def next():
    _process_key(Next)


def previous():
    _process_key(Prev)


def play():
    _process_key(Play)


def volume_up():
    _process_key(VolumeUp)


def volume_down():
    _process_key(VolumeDown)


def mute():
    _process_key(Mute)


def _process_key(keycode):
    args = ['xdotool', 'key', keycode]
    subprocess.run(args)
