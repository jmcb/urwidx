#!/usr/bin/env python
import app, form, urwid, layout, edit, menu

men = [("Test", None),
       ("Test 2", None),
       ("Test 3", [
                   ("Test 4", None),
                   ("Test 5", None),
                  ])
      ]

class Menu (urwid.ListBox):
    def __init__ (self, menu_list):
        menu_stuff = []
        for caption, extra in menu_list:
            if isinstance(extra, list):
                menu_stuff.append(urwid.BoxAdapter(Menu(extra), height=len(extra)))
            else:
                menu_stuff.append(menu.MenuWidget(caption, extra))
        walker = urwid.SimpleListWalker(menu_stuff)
        urwid.ListBox.__init__(self, walker)

class MenuTestForm (form.Form):
    def OnInit (self):
        menu = Menu(men)
        print menu
        self.SetTopWidget(menu)

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
