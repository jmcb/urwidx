#!/usr/bin/env python
"""loop.py - some tweaks to urwid.MainLoop."""
import urwid

class CanvasLoop (urwid.MainLoop):
    canvas = None
    def get_canvas (self):
        return self.canvas
    def draw_screen(self):
        if not self.screen_size:
            self.screen_size = self.screen.get_cols_rows()

        self.canvas = self.widget.render(self.screen_size, focus=True)
        self.screen.draw_screen(self.screen_size, self.canvas)

