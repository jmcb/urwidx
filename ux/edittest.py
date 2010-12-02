#!/usr/bin/env python
import app, form, urwid, layout

import time
header = None

# Editor for in-place list alteration.
class ListEditorWalker (urwid.SimpleListWalker):
    def __init__ (self, contents, editor=urwid.Edit):
        self.editors = [None for i in contents]
        self.editor = editor
        self.focus = 0

        urwid.MonitoredList.__init__(self, contents)

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

    def snip (self):
        del self.contents[self.focus]
        self.wipe_editors()

class ListEditor (urwid.ListBox):
    def __init__ (self, to_edit, editor=urwid.Edit, walker=ListEditorWalker, meta_key="ctrl e", del_key="-", append_key="+", insert_key="insert"):
        self.meta_key = meta_key
        self.append_key = append_key
        self.insert_key = insert_key
        self.delete_key = del_key
        self.looking_meta = False
        self.walker = walker(to_edit, editor)
        urwid.ListBox.__init__(self, self.walker)

    def keypress (self, size, key):
        if self.looking_meta and (key == self.append_key or key == self.append_key):
            self.walker.new(key == self.append_key)
            return
        elif self.looking_meta and key == self.delete_key:
            self.walker.snip()
            return
        else:
            self.looking_meta = (key == self.meta_key)

        return urwid.ListBox.keypress(self, size, key)

class EditTestForm (form.Form):
    def OnInit (self):
        global header
        header = urwid.Text("Header")
        self.footer = urwid.Text("Footer")

        capt=urwid.Text("This is the edit caption: ")
        self.data_list = [str(("%s " % x) * 15).strip() for x in xrange(10)]
        edit=ListEditor(self.data_list)

        col=urwid.Columns([('fixed', len(capt.text)+1, capt), urwid.BoxAdapter(edit, 10)])

        self.body = urwid.Filler(col)

        self.frame = urwid.Frame(body=urwid.LineBox(urwid.Filler(
        urwid.AttrMap(
        layout.SizedFrame(body=self.body, height=10), None)
        )), header=header, footer=self.footer)
        self.SetTopWidget(self.frame)

class EditTestApp (app.UrwidApp):
    def OnInit (self):
        form = EditTestForm(self)
        form.Show()

def main ():
    palette = [('stand', 'black', 'dark blue'),
               ('understand', 'black', 'dark green')]

    app = EditTestApp(palette=palette)
    app.MainLoop()

if __name__=="__main__":
    main ()
