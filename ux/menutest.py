#!/usr/bin/env python
import app, form, urwid, layout, edit, menu

def q (*a):
    raise urwid.ExitMainLoop()

m = menu.Menu(text=None, contents=[
        menu.MenuDivider(),
        menu.MenuItem(text="Exit", function=q),
        menu.MenuDivider(),
        menu.MenuItem(text="Test 1"),
        menu.SubMenu(text="Sub-menu test", contents=[
            menu.MenuItem(text="Sub-test 1"),
            menu.MenuItem(text="Sub-test 2")]),
        menu.MenuItem(text="Test 2")
        ], focus_attr='stand', main_attr='understand')

class Menu (urwid.ListBox):
    def __init__ (self, menu_list):
        walker = menu.MenuWalker(menu_list, menu.NumberedMenuWidget)
        urwid.ListBox.__init__(self, walker)

class MenuTestForm (form.Form):
    def OnInit (self):
        menu = Menu(m)
        self.SetTopWidget(menu)

class MenuTestApp (app.UrwidApp):
    def OnInit (self):
        form = MenuTestForm(self)
        form.Show()

def main ():
    palette = [('stand', 'black', 'dark blue'),
               ('understand', 'black', 'dark green')]

    app = MenuTestApp(palette=palette, handle_mouse=True)
    app.MainLoop()

if __name__=="__main__":
    main ()
