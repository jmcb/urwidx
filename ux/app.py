#!/usr/bin/env python
#!/usr/bin/env python
"""app.py - some convenience classes around urwid."""

import urwid

class Form:
    """
    A blank "form", basically a container for a variety of widgets.
    """
    def __init__ (self, parent, top_widget=None):
        self._parent = parent
        self._top_widget = top_widget
        self._binds = {}

        if hasattr(self, "OnInit"):
            self.OnInit()

    def Bind (self, widget, signal, function, *user_data):
        if signal in widget.signals:
            return urwid.connect_signal(widget, signal, function, (self, ) + tuple(user_data))
        else:
            return False

    def BindText (self, text, function, *user_data):
        if not hasattr(text, "__iter__"):
            text = (text, )
        for text2 in text:
            self._binds.setdefault(text2, [])
            self._binds[text2].append((function, user_data))

    def UnhandledInput (self, input):
        if input in self._binds.keys():
            for function, user_data in self._binds[input]:
                function(self, *user_data)
        return input

    def GetParent (self):
        return self._parent

    def SetTopWidget (self, widget):
        self._top_widget = widget

    def GetTopWidget (self):
        return self._top_widget

    def Show (self):
        self.GetParent().SetTopWindow(self)
        self.GetParent().Show(self.GetTopWidget())

class Dialog (Form):
    pass

class UrwidApp:
    def __init__ (self, palette=None, screen=None):
        self.main_loop = urwid.MainLoop(None, palette, screen, handle_mouse=False, input_filter=self.input_filter, unhandled_input=self.unhandled_input)
        self._top_window = None

        if hasattr(self, "OnInit"):
            self.OnInit()

    def input_filter (self, input, raw):
        return input

    def unhandled_input (self, input):
        return self.GetTopWindow().UnhandledInput(input)

    def MainLoop (self):
        return self.main_loop.run()

    def GetCurrentWidget (self):
        return self.main_loop.widget

    def SetCurrentWidget (self, widget):
        self.main_loop.widget = widget

    def SetTopWindow (self, window):
        self._top_window = window

    def GetTopWindow (self):
        return self._top_window

    def Show (self, widget):
        self.SetCurrentWidget(widget)
        try:
            self.main_loop.draw_screen()
        except AssertionError:
            return False
        else:
            return True
