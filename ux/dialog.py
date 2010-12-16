#!/usr/bin/env python

import form, app, urwid, layout, button

class Dialog (form.Form):
    """

    A modular Form designed to be displayed over the top of other forms.

    """
    def __init__ (self, parent, width, height, align='center', valign='middle', shadow=u'\u2592', top_widget=None):
        """

        Initialise a dialog. Requires the same parameters as a Form, in addition:

        parent: the UrwidApp parent.
        width: the width of the dialog.
        height: the height of the dialog.
        align: where the dialog should be displayed horizontally.
        valign: where the dialog should be displayed vertically.
        shadow: the character to be used as a "drop shadow".
        top_widget: the top widget of the form.

        """
        self.width = width
        self.height = height
        self.align = align
        self.valign = valign
        self.shadow = shadow
        self.result = None
        self.showing_modal = False

        form.Form.__init__(self, parent, top_widget)

    def MakeShadow (self):
        """

        Create a box widget that is displayed as the "shadow" of the dialog.

        """

        return urwid.SolidFill(self.shadow)

    def MakeOverlay (self):
        """

        Builds a series of overlays: overlay1 consists of the shadow on top of the currently displayed widget. overlay2 consists of the dialog on top of the shadow.

        """
        self.overlay1 = layout.OffsetOverlay(self.MakeShadow(), self.GetParent().GetCurrentWidget(), self.align, self.width, self.valign, self.height)
        self.overlay2 = urwid.Overlay(self.GetTopWidget(), self.overlay1, self.align, self.width, self.valign, self.height)
        return self.overlay2

    def Show (self, discard_current=False):
        """

        Shows the dialog on top of the currently displayed widget.

        """
        assert self.GetTopWidget() is not None
        self.GetParent().SetTopForm(self, not discard_current)
        self.GetParent().Show(self.MakeOverlay())

    def GotResult (self, result):
        """

        A convenience function for parsing the "result" of a dialog. For modally displayed dialogs it merely stores the result. For non-modal dialogs, it dismisses the dialog as well as storing the result.

        """
        if self.showing_modal:
            def f (*args):
                self.result = result
        else:
            def f (*args):
                self.result = result
                self.ShowPrevious()
        return f

    def ShowModal (self):
        """

        Enter into a sub-loop to display the dialog. All key inputs will be based to the relevant sub-widgets. The function will block until a "result" is gathered from the dialog (pressing a key, selecting a button, providing a relevant value, etc), at which point the result will be returned to the calling thread.

        """
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

        self.showing_modal = False
        return self.result

class ButtonDialog (Dialog):
    """

    A sub-dialog consisting of a displayed string (passed via 'caption') and a series of buttons (as defined in _uxconf.BUTTON_LIST).

    """
    def __init__ (self, parent, width, height, align='center', valign='middle', shadow=u'\u2592', caption="", **buttons):
        """

        Initiliases the ButtonDialog. Extra parameters:

        caption: the text caption to be displayed.
        **buttons: a series of keyword arguments with a boolean true value for the button in question to be displayed (or false for it not to be displayed0.

        """
        self.caption_text = caption
        self.buttons = buttons

        # NB: Width and height increased by two to compensate for LineBox.
        Dialog.__init__ (self, parent, width+2, height+2, align, valign, shadow, None)

    def OnInit (self):
        """

        Dynamically builds the dialog based on the supplied variables.

        """
        self.caption = urwid.Text(self.caption_text)
        self.button_list = []

        for btype, bval in self.buttons.iteritems():
            if not bval:
                continue
            if not button.has_button(btype):
                raise IndexError, btype
            btn = button.get_button(btype)
            self.button_list.append(urwid.Button(label=btn.label, on_press=self.GotResult(btn.result)))
            self.BindText(btn.hotkey, self.GotResult(btn.result))

        if self.button_list:
            self.columns = urwid.Columns(self.button_list, dividechars=1)

            self.pile = urwid.Pile([('fixed', self.height-3, urwid.Filler(self.caption, 'top')), self.columns])

            self.layout = urwid.LineBox(urwid.Filler(self.pile))
        else:
            self.layout = urwid.LineBox(urwid.Filler(self.caption))

        self.layout2 = urwid.AttrMap(self.layout, 'dialog')

        self.SetTopWidget(self.layout2)


