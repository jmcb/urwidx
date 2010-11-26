#!/usr/bin/env python

from _uxconf import *
import form, app, urwid

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
        assert isinstance(parent, app.UrwidApp)
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

    def ShowPrevious (self, *args):
        """

        A short function for lambdas.

        """
        self.GetParent().ShowPreviousForm()
