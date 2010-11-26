#!/usr/bin/env python
import collections

button_type = collections.namedtuple('ButtonInfo', 'label result hotkey')

_BUTTON_INFO = {}
_BUTTON_INFO['yes'] = button_type(label=[('underline', 'Y'), 'es'], result='y', hotkey=['y', 'Y'])
_BUTTON_INFO['no'] = button_type(label=[('underline', 'N'), 'o'], result='n', hotkey=['n', 'N'])
_BUTTON_INFO['ok'] = _BUTTON_INFO['okay'] = button_type(label=[('underline', 'O'), 'kay'], result='ok', hotkey=['k', 'K', 'O', 'o'])
_BUTTON_INFO['cancel'] = button_type(label=[('underline', 'C'), 'ancel'], result='cancel', hotkey=['c', 'C'])

def has_button (button):
    return _BUTTON_INFO.has_key(button)

def get_button (button):
    return _BUTTON_INFO[button]

def add_button (button, *args, **kwargs):
    if has_button (button):
        raise IndexError
    if len(args) == 3:
        bt = button_type(*args)
    else:
        bt = button_type(**kwargs)
    _BUTTON_INFO[button] = bt
