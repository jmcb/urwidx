#!/usr/bin/env python

# for app.py
BIND_TEXT_DEFAULT = True

# for button.py
BUTTON_INFO = {
    "yes": {"label": [('underline', 'Y'), 'es'], "result": 'y', "hotkey": ['y', 'Y']},
    "no": {"label": [('underline', 'N'), 'o'], "result": 'n', "hotkey": ['n', 'N']},
    "ok": {"label": [('underline', 'O'), 'kay'], "result": 'ok', "hotkey": ['k', 'K', 'O', 'o']},
    "cancel": {"label": [('underline', 'C'), 'ancel'], "result": 'cancel', "hotkey": ['c', 'C']},
    }
BUTTON_INFO["okay"] = BUTTON_INFO["ok"]
