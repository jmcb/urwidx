#!/usr/bin/env python
import app, form, urwid, layout, edit

class MenuItem (urwid.Button):
    button_left = urwid.Text("")
    button_right = urwid.Text("")

class MenuTestForm (form.Form):
    def OnInit (self):
        button = MenuItem("This is a test")

        self.SetTopWidget(button)

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
