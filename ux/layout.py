#!/usr/bin/env python
"""layout.py - """
import urwid

# Taken from http://www.mail-archive.com/urwid@lists.excess.org/msg00515.html
class OffsetOverlay(urwid.Overlay):
    def calculate_padding_filler(self, size, focus):
        l, r, t, b = self.__super.calculate_padding_filler(size, focus)
        return l+1, max(0, r-1), t+1, max(0, b-1)

# A flow widget version of urwid.Frame.
class SizedFrame (urwid.BoxAdapter):
    def __init__ (self, height, body, header=None, footer=None, focus_part='body'):
        urwid.BoxAdapter.__init__(self, urwid.Frame(body, header, footer, focus_part), height)
