
"""app.py - some convenience classes around urwid."""

import urwid
import layout
import loop

class UrwidApp:
    def __init__ (self, palette=None, screen=None, my_loop=loop.CanvasLoop, handle_mouse=False):
        """

        Initialise the UrwidApplication, setting up a main loop, a form queue, and  then calling the OnInit function.

        """
        self.main_loop = my_loop(None, palette, screen, handle_mouse=handle_mouse, input_filter=self.input_filter, unhandled_input=self.unhandled_input)
        self._top_form = None
        self._previous_forms = []
        self._callbacks = {}

        if hasattr(self, "OnInit"):
            self.OnInit()

    def CallEvery (self, function, call_every, user_data=None):
        def wrapper (mainloop, user_data):
            self._callbacks[function.__name__] = self.main_loop.set_alarm_in(call_every, wrapper, user_data)
            function(mainloop, user_data)
        self._callbacks[function.__name__] = self.main_loop.set_alarm_in(call_every, wrapper, user_data)

    def UncallEvery (self, function):
        try:
            self.main_loop.remove_alarm(self._callbacks[function])
        except IndexError:
            return False
        else:
            return True

    def input_filter (self, input, raw):
        return self.GetTopForm().FilterInput(input, raw)

    def unhandled_input (self, input):
        return self.GetTopForm().UnhandledInput(input)

    def MainLoop (self):
        assert self.GetCurrentWidget() is not None
        assert self.GetTopForm() is not None
        return self.main_loop.run()

    def GetCurrentWidget (self):
        return self.main_loop.widget

    def SetCurrentWidget (self, widget):
        self.main_loop.widget = widget

    def SetTopForm (self, form, store_previous=True):
        if store_previous and self._top_form != None:
            self._previous_forms.append(self._top_form)
        self._top_form = form

    def GetTopForm (self):
        return self._top_form

    def ShowPreviousForm (self, discard_current=True):
        try:
            new_form = self._previous_forms.pop()
        except IndexError:
            return False

        current_form = self.GetTopForm()
        if current_form is not None and hasattr(current_form, "OnHide"):
            current_form.OnHide()

        self.SetTopForm(new_form, not discard_current)
        new_form.Show()

    def Show (self, widget):
        """

        Should never be called directly; instead, create a Form, pass it this application, and then call its Show method.

        """
        assert self.GetTopForm() is not None

        self.SetCurrentWidget(widget)
        if hasattr(self.GetTopForm(), "OnShow"):
            self.GetTopForm().OnShow()
        try:
            self.main_loop.draw_screen()
        except AssertionError:
            return False
        else:
            return True
