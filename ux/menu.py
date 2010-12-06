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

class MenuItem (BaseMenuStructure):
    text = None
    function = None
    hotkey = None
    def __init__ (self, text, function=None, hotkey=None):
        if text is None:
            raise ValueError, "MenuItem text cannot be None."

        self.text = text
        self.function = function
        self.hotkey = hotkey

class BaseMenu:
    text = None
    contents = None
    function = None
    hotkey = None
    expanded = None
    expandable = None
    def __init__ (self, text, contents, function, hotkey, expanded, expandable):
        self.text = text
        self.contents = contents
        self.function = function
        self.hotkey = hotkey
        self.expanded = expanded
        self.expandable = expandable

class Menu (BaseMenu, BaseMenuStructure):
    def __init__(self, text, contents, function=None, hotkey=None, expanded=True, expandable=False):
        if contents is None:
            raise ValueError, "Menu contents cannot be None."
        return BaseMenu.__init__(self, text, contents, function, hotkey, expanded, expandable)

class SubMenu (BaseMenu, BaseMenuStructure):
    def __init__(self, text, contents, function=None, hotkey=None, expanded=False, expandable=True):
        if contents is None:
            raise ValueError, "SubMenu contents cannot be None."
        return BaseMenu.__init__(self, text, contents, function, hotkey, expanded, expandable)

# Widgets used for representing MenuItem, Menu and SubMenu on screen.
class MenuWidget (urwid.SelectableIcon):
    signals = ["click"]
    def __init__(self, item, callback=None, cursor_position=0, depth=0):
        text = item

        if hasattr(item, "function"):
            if callback == None:
                callback = item.function
            text = item.text

        if callback:
            urwid.connect_signal(self, "click", callback)

        if depth > 1:
            text = " " * (depth-1) + text

        urwid.SelectableIcon.__init__(self, text, cursor_position)
    def keypress(self, size, key):
        if urwid.command_map[key] != 'activate':
            return key

        self._emit('click')

# Stuff that combines MenuWidget and Menu* into something that urwid can deal with.
class MenuWalker (urwid.SimpleListWalker):
    def __init__(self, menu):
        self.menu = menu

        urwid.SimpleListWalker.__init__(self, self._parse_menu(self.menu))

    def _parse_menu (self, menu, menu_depth=0):
        menu_depth = menu_depth + 1

        menu_list = []
        for item in menu.contents:
            if item.is_menu_item():
                menu_list.append(MenuWidget(item, depth=menu_depth))
            elif item.is_submenu():
                widget = MenuWidget(item, depth=menu_depth)
                urwid.connect_signal(widget, "click", self._expand_fn(item))
                menu_list.append(widget)
                if item.is_expanded():
                    menu_list.extend(self._parse_menu(item, menu_depth))
        return menu_list

    def _expand_fn (self, item):
        def _expander (*args, **kwargs):
            item.expanded = not item.expanded
            if item.function:
                item.function(*args, **kwargs)
            self.update_menu()
        return _expander

    def update_menu (self):
        self.contents[:] = self._parse_menu(self.menu)
