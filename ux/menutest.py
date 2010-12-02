#!/usr/bin/env python
import app, form, urwid, layout, edit

class MenuItem (urwid.Button):
    button_left = urwid.Text("")
    button_right = urwid.Text("")

class MenuTestForm (form.Form):
    def OnInit (self):
        button = urwid.AttrMap(MenuItem("This is a test"), None, "understand")
        button2 = urwid.AttrMap(MenuItem("This is another test."), None, "understand")
        self.pile = urwid.Pile([button, button2])

        self.SetTopWidget(urwid.Filler(self.pile))

class MenuTestApp (app.UrwidApp):
    def OnInit (self):
        form = MenuTestForm(self)
        form.Show()

def main ():
    palette = [('stand', 'black', 'dark blue'),
               ('understand', 'black', 'dark green')]

    app = MenuTestApp(palette=palette)
    app.MainLoop()

if __name__=="__main__":
    main ()
