#!/usr/bin/env python
"""edit.py - a selection of custom editors. """

import urwid, layout

class MaskedEdit (urwid.Edit):
    def __init__ (self, caption='', edit_text='', mask_char=' ', multiline=False, align='left', wrap='space', allow_tab=False, edit_pos=None, layout=None):
        assert len(mask_char) == 1
        self.mask_char = mask_char

        urwid.Edit.__init__(self, caption, edit_text, multiline, align, wrap, allow_tab, edit_pos, layout)

    def render(self, *args, **kwargs):
        edit_text = self.edit_text

        self.edit_text = self.mask_char * len(self.edit_text)

        rv = urwid.Edit.render(self, *args, **kwargs)

        self.edit_text = edit_text

        return rv

class PasswordEdit (MaskedEdit):
    def __init__ (self, *args, **kwargs):
        kwargs["mask_char"] = "*"
        MaskedEdit.__init__(self, *args, **kwargs)

class BoolEdit (urwid.Edit):
    def __init__ (self, caption='', initially=True, align='left', true_value="X", false_value="-"):
        edit_text = true_value
        self.cur_value = initially
        if not initially:
            edit_text = false_value
        self.true_value = true_value
        self.false_value = false_value
        urwid.Edit.__init__(self, caption=caption, edit_text=edit_text, align=align)

    def get_value (self):
        return self.cur_value

    def get_value_as_int (self):
        return int(self.get_value())

    def set_value (self, value):
        self.cur_value = value
        if value == True:
            self.edit_text = self.true_value
        else:
            self.edit_text = self.false_value

    def keypress (self, size, key):
        if key in ('enter', ' '):
            self.set_value(not self.get_value())
        else:
            return key

class ListEditor (layout.SizedFrame):
    def __init__ (self, caption, edit_list, height=10, editor=urwid.Edit):
        self.caption = urwid.Text(caption)
        self.edit_list = edit_list
        self.list_editor = layout.ListBoxEditor(self.edit_list)
        self.columns = urwid.Columns([('fixed', len(caption)+1, self.caption), urwid.BoxAdapter(self.list_editor, height)])
        self.body = urwid.Filler(self.columns)

        layout.SizedFrame.__init__(self, body=self.body, height=height)

