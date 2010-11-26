#!/usr/bin/env python

from _uxconf import *
import form, app, urwid, layout

class Dialog (form.Form):
    def __init__ (self, parent, width, height, align='center', valign='middle', shadow=u'\u2592', top_widget=None):
        self.width = width
        self.height = height
        self.align = align
        self.valign = valign
        self.shadow = shadow
        self.result = None
        self.showing_modal = False

        form.Form.__init__(self, parent, top_widget)

    def MakeShadow (self):
        return urwid.SolidFill(self.shadow)

    def MakeOverlay (self):
        self.overlay1 = layout.OffsetOverlay(self.MakeShadow(), self.GetParent().GetCurrentWidget(), self.align, self.width, self.valign, self.height)
        self.overlay2 = urwid.Overlay(self.GetTopWidget(), self.overlay1, self.align, self.width, self.valign, self.height)
        return self.overlay2

    def Show (self):
        assert self.GetTopWidget() is not None
        self.GetParent().SetTopForm(self)
        self.GetParent().Show(self.MakeOverlay())

    def GotResult (self, result):
        if self.showing_modal:
            def f (*args):
                self.result = result
        else:
            def f (*args):
                self.result = result
                self.ShowPrevious()
        return f

    def ShowModal (self):
        self.showing_modal = True

        self.Show()
        self.result = None
        parent = self.GetParent().main_loop
        while not self.result:
            parent.draw_screen()

            keys = None

            while not keys:
                keys, raw = parent.screen.get_input(True)

            keys = parent.input_filter(keys, raw)

            if keys:
                parent.process_input(keys)

            if 'window resize' in keys:
                parent.screen_size = None

        self.GetParent().ShowPreviousForm()
        self.showing_modal = False
        return self.result

class ButtonDialog (Dialog):
    def __init__ (self, parent, width, height, align='center', valign='middle', shadow=u'\u2592', caption="", **buttons):
        self.caption_text = caption
        self.buttons = buttons

        # NB: Width and height increased by two to compensate for LineBox.
        Dialog.__init__ (self, parent, width+2, height+2, align, valign, shadow, None)

    def OnInit (self):
        self.caption = urwid.Text(self.caption_text)
        self.button_list = []

        for btype, bval in self.buttons.iteritems():
            if not bval:
                continue
            if not BUTTON_INFO.has_key(btype):
                raise IndexError, btype
            button = BUTTON_INFO[btype]
            self.button_list.append(urwid.Button(label=button['label'], on_press=self.GotResult(button['result'])))
            self.BindText(button['hotkey'], self.GotResult(button['result']))

        if self.button_list:
            self.columns = urwid.Columns(self.button_list, dividechars=1)

            self.pile = urwid.Pile([('fixed', self.height-3, urwid.Filler(self.caption, 'top')), self.columns])

            self.layout = urwid.LineBox(urwid.Filler(self.pile))
        else:
            self.layout = urwid.LineBox(urwid.Filler(self.caption))

        self.layout2 = urwid.AttrMap(self.layout, 'dialog')

        self.SetTopWidget(self.layout2)


