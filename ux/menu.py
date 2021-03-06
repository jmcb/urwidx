#!/usr/bin/env python
""" menu.py """

import urwid, collections

# Flat structures for Menus.
class BaseMenuStructure:
    def is_divider (self):
        return self.text == "---"
    def is_menu_item (self):
        return isinstance(self, MenuItem) and not self.is_divider()
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

class MenuDivider (MenuItem):
    text = "---"
    function = None
    hotkey = None
    def __init__ (self):
        pass

class BaseMenu:
    text = None
    contents = None
    function = None
    hotkey = None
    expanded = None
    expandable = None
    main_attr = None
    focus_attr = None
    def __init__ (self, text, contents, function, hotkey, expanded, expandable, main_attr, focus_attr):
        self.text = text
        self.contents = contents
        self.function = function
        self.hotkey = hotkey
        self.expanded = expanded
        self.expandable = expandable
        self.main_attr = main_attr
        self.focus_attr = focus_attr

class Menu (BaseMenu, BaseMenuStructure):
    def __init__(self, text, contents, function=None, hotkey=None, expanded=True, expandable=False, main_attr=None, focus_attr=None):
        if contents is None:
            raise ValueError, "Menu contents cannot be None."
        return BaseMenu.__init__(self, text, contents, function, hotkey, expanded, expandable, main_attr, focus_attr)

class SubMenu (BaseMenu, BaseMenuStructure):
    def __init__(self, text, contents, function=None, hotkey=None, expanded=False, expandable=True, main_attr=None, focus_attr=None):
        if contents is None:
            raise ValueError, "SubMenu contents cannot be None."
        return BaseMenu.__init__(self, text, contents, function, hotkey, expanded, expandable, main_attr, focus_attr)

# Widgets used for representing MenuItem, Menu and SubMenu on screen.
class MenuWidget (urwid.SelectableIcon):
    signals = ["click"]
    def __init__(self, item, callback=None, cursor_position=0, depth=0, num=False, numbered=False):
        text = item

        if hasattr(item, "function"):
            if callback == None:
                callback = item.function
            text = item.text

        if callback:
            urwid.connect_signal(self, "click", callback)

        if numbered:
            text = "%s. %s" % (num, text)

        if depth > 1:
            text = " " * (depth-1) + text

        urwid.SelectableIcon.__init__(self, text, cursor_position)

    # Following functionality duplicated from urwid's Buttons.
    # see urwid/wimp.py.
    def keypress(self, size, key):
        if urwid.command_map[key] != 'activate':
            return key

        self._emit('click')

    def mouse_event (self, size, event, button, x, y, focus):
        if button != 1 or not urwid.is_mouse_press(event):
            return False

        self._emit('click')
        return True

class NumberedMenuWidget (MenuWidget):
    def __init__(self, item, callback=None, cursor_position=0, depth=0, num=None):
        if num is not None:
            numbered = True
        else:
            numbered = False

        MenuWidget.__init__(self, item, callback, cursor_position, depth, num, numbered)

# Stuff that combines MenuWidget and Menu* into something that urwid can deal with.
class MenuWalker (urwid.SimpleListWalker):
    def __init__(self, menu, widget_type=MenuWidget):
        self.menu = menu
        self.widget_type = widget_type

        urwid.SimpleListWalker.__init__(self, self._parse_menu(self.menu))

    def _parse_menu (self, menu, menu_depth=0):
        menu_depth = menu_depth + 1

        current = 0

        menu_list = []
        for item in menu.contents:
            if item.is_divider():
                menu_list.append(urwid.AttrMap(urwid.Divider(), self.menu.main_attr, self.menu.focus_attr))
                continue

            current = current + 1
            if item.is_menu_item():
                menu_list.append(urwid.AttrMap(self.widget_type(item, depth=menu_depth, num=current), self.menu.main_attr, self.menu.focus_attr))
            elif item.is_submenu():
                widget = self.widget_type(item, depth=menu_depth, num=current)
                urwid.connect_signal(widget, "click", self._expand_fn(item))
                menu_list.append(urwid.AttrMap(widget, self.menu.main_attr, self.menu.focus_attr))
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
