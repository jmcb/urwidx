#!/usr/bin/env python
import app, urwid, weakref

class PrettyForm (app.Form):
    def OnInit (self):
        self.fill = urwid.SolidFill('y')
        self.box = urwid.AttrMap(urwid.Filler(urwid.Text("Test", align='center'), 'middle'), 'test')
        self.overlay = urwid.Overlay(self.box, self.fill, 'center', 12, 'middle', 7)
        self.SetTopWidget(self.overlay)
        self.BindText(['q', 'Q', 'enter'], lambda a: self.Quit())

    def Quit (self):
        raise urwid.ExitMainLoop()

class TestApp (app.UrwidApp):
    def OnInit (self):
        form = PrettyForm(self)
        form.Show()

def main():
    palette = [
        ('test', 'black', 'dark blue')
    ]

    app = TestApp(palette=palette)

    try:
        app.MainLoop()
    except KeyboardInterrupt:
        pass

if __name__=="__main__":
    main()
