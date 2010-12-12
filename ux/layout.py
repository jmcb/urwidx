#!/usr/bin/env python
"""layout.py - """
import urwid

# Taken from http://www.mail-archive.com/urwid@lists.excess.org/msg00515.html
class OffsetOverlay(urwid.Overlay):
    def calculate_padding_filler(self, size, focus):
        l, r, t, b = self.__super.calculate_padding_filler(size, focus)
        return l+1, max(0, r-1), t+1, max(0, b-1)

# A flow widget version of urwid.Frame.
class SizedFrame (urwid.BoxAdapter):
    def __init__ (self, height, body, header=None, footer=None, focus_part='body'):
        urwid.BoxAdapter.__init__(self, urwid.Frame(body, header, footer, focus_part), height)
    def get_cursor_coords (self, size):
        return self.render(size, focus=True).cursor

# Walker that interfaces on a list of string values, providing editors for them.
# Support in-place editing by setting in_place=True.
class ListEditorWalker (urwid.SimpleListWalker):
    def __init__ (self, contents, editor=urwid.Edit, in_place=True):
        self.to_update = contents
        self.editors = [None for i in contents]
        self.editor = editor
        self.focus = 0

        urwid.MonitoredList.__init__(self, contents)

        if in_place:
            urwid.connect_signal(self, "modified", self.update_list)

    def update_list (self):
        self.to_update[:] = list(self)

    def wipe_editors (self):
        self.editors = [None for i in self.contents]

    def _get_focus (self, pos):
        if pos < 0: return None, None
        if len(self.contents) <= pos: return None, None

        return self._get_focus_editor(pos), pos

    def _get_focus_editor (self, pos):
        if self.editors[pos]:
            return self.editors[pos]

        def update_list (pos):
            def f (editor, new_value):
                if not self.editors[pos]:
                    self.editors[pos] = None
                self.contents[pos] = new_value
                self._modified()
            return f

        editor = self.editor(edit_text=self.contents[pos])
        urwid.connect_signal(editor, 'change', update_list(pos))
        self.editors[pos] = editor

        return editor

    def set_focus (self, focus):
        assert isinstance(focus, int)
        self.focus = focus
        self._modified()

    def get_next (self, pos):
        return self._get_focus(pos+1)

    def get_prev (self, pos):
        return self._get_focus(pos-1)

    def get_focus (self):
        if len(self.contents) == 0: return None, None
        return self._get_focus_editor(self.focus), self.focus

    def new (self, end=True):
        if end == True:
            self.contents.append("")
            self.editors.append(None)
            self.focus = len(self.contents)-1
        else:
            self.contents.insert(self.focus, "")
            self.editors.append(None)
            self.wipe_editors()

    def snip (self):
        del self.contents[self.focus]
        self.wipe_editors()

# An interface to ListEditorWalker.
class ListBoxEditor (urwid.ListBox):
    def __init__ (self, to_edit, editor=urwid.Edit, walker=ListEditorWalker, meta_key="ctrl e", del_key="-", append_key="+", insert_key="insert"):
        self.to_edit = to_edit
        self.meta_key = meta_key
        self.append_key = append_key
        self.insert_key = insert_key
        self.delete_key = del_key
        self.looking_meta = False
        self.walker = walker(self.to_edit, editor)
        urwid.ListBox.__init__(self, self.walker)

    def keypress (self, size, key):
        if self.looking_meta:
            self.looking_meta = False
            if key == self.append_key or key == self.insert_key:
                self.walker.new(key == self.append_key)
                return
            elif key == self.delete_key:
                self.walker.snip()
                return

        self.looking_meta = (key == self.meta_key)

        return urwid.ListBox.keypress(self, size, key)
