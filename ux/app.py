#!/usr/bin/env python
"""app.py - some convenience classes around urwid."""

import urwid

BIND_TEXT_DEFAULT = True

class Form:
    """

    Form: a collection of widgets and associated functions.

    """
    def __init__ (self, parent, top_widget=None):
        """

        Build a new form. Expects to be passed an instance of UrwidApp as its parent.

        parent: an intance of UrwidApp
        top_widget: a "top" widget. Not required.

        """
        assert isinstance(parent, UrwidApp)
        self._parent = parent
        self._top_widget = top_widget
        self._binds = {}

        if hasattr(self, "OnInit"):
            self.OnInit()

    def OnInit (self):
        """

        Do various initialisations of the form. Can be subclassed and used to build the form with widgets and so-on.

        No arguments.

        """
        pass

    def Bind (self, widget=None, signal="", function=lambda *a: a, *user_data):
        """

        Bind functions to a widget's signal. If BIND_TEXT_DEFAULT is true and a signal is not contained in widget.signals (or no widget is passed), it will attempt to bind the signal into the Uhandled Input handler.

        widget: an Urwid widget or None.
        signal: a string or list of strings.
        function: a function accepting at least two parameters. (widget, this Form, any user data)
        *user_data: any other relevant user data to be passed to the callback.

        NB: No checks are performed to ensure that the function accepts the correct number of arguments.

        """
        if widget and signal in widget.signals:
            return urwid.connect_signal(widget, signal, function, (self, ) + tuple(user_data))
        elif BIND_TEXT_DEFAULT:
            return self.BindText(self, signal, function, *user_data)
        else:
            return False

    def BindText (self, text, function, *user_data):
        """

        Binds a function to any unhandled text. Can be passed a list of strings.

        text: a string or list o strings to bind function to.
        function: a function accepting at least one parameter. (this Form)
        *user_data: any other relevant user data to be passed to the callback.

        NB: No checks are performed to ensure that the function accepts the correct number of arguments.

        """
        if not hasattr(text, "__iter__"):
            text = (text, )
        for text2 in text:
            self._binds.setdefault(text2, [])
            self._binds[text2].append((function, user_data))
        return True

    def UnhandledInput (self, input):
        """

        Handles any input that is not handled by the top widget (or subwidgets) by urwid. This function is primarily used to handle bound text to functions. Any subclassing should either reference this function, if you wish text binds to continue to function, or use the virtual function 'Input', which is called from this function.

        input: input as passed from the urwid main_loop.

        """
        if input in self._binds.keys():
            for function, user_data in self._binds[input]:
                function(self, *user_data)
        if hasattr(self, "Input"):
            return self.Input(input)
        return input

    def Input (self, input):
        """

        A virtual function to handle unhandled input that is not picked up as a text bind.

        input: input passed from urwid's main loop.

        """
        return input

    def FilterInput (self, input, raw):
        """

        An option for input to be filtered before being passed to relevant widgets. Return a blank string to "block" input.

        input: input as passed from urwid's main loop.
        raw: raw input as passed from urwid's main loop.

        """
        return input

    def GetParent (self):
        """

        Returns the parent of this Form, an UrwidApp.

        """
        return self._parent

    def SetTopWidget (self, widget):
        """

        Marks the specified widget as being the "top" widget of this form. When the form is shown, this widget will be drawn to the screen.

        widget: the urwid widget in question.

        """
        self._top_widget = widget

    def GetTopWidget (self):
        """

        Returns the "top" widget of this form.

        """
        return self._top_widget

    def Show (self):
        """

        Displays the Form, pushing it to the front of the "Form" queue in the parent application, and displaying the current top widget.

        """
        assert self.GetTopWidget() is not None
        self.GetParent().SetTopForm(self)
        self.GetParent().Show(self.GetTopWidget())

class Dialog (Form):
    def ShowModal (self):
        pass

class UrwidApp:
    def __init__ (self, palette=None, screen=None):
        """

        Initialise the UrwidApplication, setting up a main loop, a form queue, and  then calling the OnInit function.

        """
        self.main_loop = urwid.MainLoop(None, palette, screen, handle_mouse=False, input_filter=self.input_filter, unhandled_input=self.unhandled_input)
        self._top_form = None
        self._previous_form = []

        if hasattr(self, "OnInit"):
            self.OnInit()

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

        self.SetTopForm(new_form, not discard_current)
        new_form.Show()

    def Show (self, widget):
        """

        Should never be called directly; instead, create a Form, pass it this application, and then call its Show method.

        """
        assert self.GetTopForm() is not None

        self.SetCurrentWidget(widget)
        try:
            self.main_loop.draw_screen()
        except AssertionError:
            return False
        else:
            return True
