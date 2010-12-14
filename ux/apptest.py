#!/usr/bin/env python
import app, urwid, weakref, dialog, form
import random, string

class PrettyForm (form.Form):
    def OnInit (self):
        self.fill = urwid.SolidFill('y')
        self.SetTopWidget(self.fill)
        self.BindText(['q', 'Q', 'enter'], self.Quit)
        self.BindText(['d', 'D'], self.ShowDialog)
        def caller (*args):
            char = ""
            while True:
                char = chr(random.randint(1, 255))
                if char in string.ascii_letters:
                    break
            self.fill = urwid.SolidFill(char)
            self.SetTopWidget(self.fill)
            self.Show()
        self.GetParent().CallEvery(caller, 1)

    def ShowDialog (self, *a):
        dialog = PrettyDialog(self.GetParent(), 20, 5)
        result = dialog.ShowModal()

        dialog = DisplayResult(self.GetParent(), 20, 3, caption="Result is: %s" % result, okay=True)
        dialog.Show()

    def Quit (self, *args):
        raise urwid.ExitMainLoop()

class DisplayResult (dialog.ButtonDialog):
    def MakeShadow (self):
        return urwid.AttrMap(dialog.Dialog.MakeShadow(self), 'shadow')

class PrettyDialog (dialog.Dialog):
    def OnInit (self):
        self.fill = urwid.AttrMap(urwid.LineBox(urwid.Filler(urwid.Pile([urwid.Text('Press Y or N.'),
            urwid.Button("Test (q)", self.GotResult('q')),
            urwid.Button("Test 2 (m)", self.GotResult('m'))]))), 'test')
        self.SetTopWidget(self.fill)
        self.BindText(['p', 'P'], self.ShowPrevious)
        self.BindText(['y', 'Y'], self.GotResult('y'))
        self.BindText(['n', 'N'], self.GotResult('n'))

    def MakeShadow (self):
        return urwid.AttrMap(dialog.Dialog.MakeShadow(self), 'shadow')

class TestApp (app.UrwidApp):
    def OnInit (self):
        form = PrettyForm(self)
        form.Show()

def main():
    palette = [
        ('test', 'black', 'dark blue'),
        ('shadow', 'dark blue', 'default'),
        ('dialog', 'black', 'dark blue'),
        ('underline', 'black,underline', 'dark blue'),
    ]

    app = TestApp(palette=palette, handle_mouse=True)

    try:
        app.MainLoop()
    except KeyboardInterrupt:
        pass
    except AttributeError, e:
        if "'mouse_event'" in e.message:
            app.MainLoop()
        else:
            raise e

if __name__=="__main__":
    main()
