#!/usr/bin/env python
import app, urwid, weakref

class PrettyForm (app.Form):
    def OnInit (self):
        self.fill = urwid.SolidFill('y')
        self.SetTopWidget(self.fill)
        self.BindText(['q', 'Q', 'enter'], lambda *a: self.Quit())
        self.BindText(['d', 'D'], self.ShowDialog)

    def ShowDialog (self, *a):
        dialog = PrettyDialog(self.GetParent(), 10, 10)
        dialog.ShowModal()

    def Quit (self):
        raise urwid.ExitMainLoop()

class PrettyDialog (app.Dialog):
    def OnInit (self):
        self.fill = urwid.AttrMap(urwid.Filler(urwid.Text('THIS IS A TEST')), 'test')
        self.SetTopWidget(self.fill)
        self.BindText(['p', 'P'], lambda *a: self.GetParent().ShowPreviousForm())

    def MakeShadow (self):
        return urwid.AttrMap(app.Dialog.MakeShadow(self), 'shadow')

class TestApp (app.UrwidApp):
    def OnInit (self):
        form = PrettyForm(self)
        form.Show()

def main():
    palette = [
        ('test', 'black', 'dark blue'),
        ('shadow', 'black', 'dark blue'),
    ]

    app = TestApp(palette=palette)

    try:
        app.MainLoop()
    except KeyboardInterrupt:
        pass

if __name__=="__main__":
    main()
