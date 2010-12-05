#!/usr/bin/env python
""" menu.py """

import urwid, collections

# Flat structures for Menus.
class BaseMenuStructure:
    def is_menu_item (self):
        return isinstance(self, MenuItem)
    def is_menu (self):
        return isinstance(self, Menu)
    def is_submenu (self):
        return isinstance(self, SubMenu)
    def is_expanded (self):
        if isinstance(self, Menu):
            return True
        else:
            return self.is_expandable() and self.expanded
    def is_expandable (self):
        return hasattr(self, 'expandable') and self.expandable

class MenuItem (collections.namedtuple("MenuItem", "text function hotkey"), BaseMenuStructure):
    def __new__ (_cls, text, function=None, hotkey=None):
        if text is None:
            raise ValueError, "MenuItem text cannot be None."
        return BaseMenuItem.__new__(_cls, text, function, hotkey)

class Menu (collections.namedtuple("Menu", "text contents function hotkey expanded expandable"), BaseMenuStructure):
    def __new__(_cls, text, contents, function=None, hotkey=None, expanded=True, expandable=False):
        if contents is None:
            raise ValueError, "Menu contents cannot be None."
        return BaseMenu.__new__(_cls, text, contents, function, hotkey, expanded, expandable)

class SubMenu (collections.namedtuple("Menu", "text contents function hotkey expanded expandable"), BaseMenuStructure):
    def __new__(_cls, text, contents, function=None, hotkey=None, expanded=False, expandable=True):
        if contents is None:
            raise ValueError, "SubMenu contents cannot be None."
        return BaseMenu.__new__(_cls, text, contents, function, hotkey, expanded, expandable)

# Widgets used for representing MenuItem, Menu and SubMenu on screen.
class MenuWidget (urwid.SelectableIcon):
    signals = ["click"]
    def __init__(self, item, callback=None, cursor_position=0):
        text = item

        if hasattr(item, "function"):
            if not callback:
                callback = item.function
            text = item.text

        if callback:
            urwid.connect_signal(self, "click", callback)

        urwid.SelectableIcon.__init__(self, text, cursor_position)

# Stuff that combines MenuWidget and Menu* into something that urwid can deal with.
class MenuWalker (urwid.SimpleListWalker):
    def __init__(self, menu):
        self.menu = menu

        urwid.SimpleListWalker.__init__(self, self.menu_as_list())

    def menu_as_list (self):
        menu_list = []

    def update_menu (self):
        self.contents[:] = self.menu_as_list()
