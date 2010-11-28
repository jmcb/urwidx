#!/usr/bin/env python
import app, form, urwid, layout

class ListEditorWalker (urwid.SimpleListWalker):
    def __init__ (self, contents, editor):
        self.contents = contents
        self.editors = [None for i in self.contents]
        self.editor = editor
        self.focus = (0, 0)

    def get_focus (self):
        if len(self.contents) == 0: return None, None

        self._clamp_focus()


    def _get_focus_editor (self, pos):
        if self.editors[pos] is not None:
            return self.editors[pos]

        def update_list (pos):
            def f (editor, new_value):
                self.contents[pos] = value
            return f

        editor = self.editor(edit_text=self.contents[pos])
        urwid.connect_signal(editor, 'change', update_list(pos))
        self.editors[pos] = editor

        return editor


class ListEditor (urwid.ListBox):
    def __init__ (self, my_list, editor=urwid.Edit, walker=urwid.SimpleListWalker):
        self.my_list = urwid.my_list
        self.walker = walker
        self.editor = editor
    def get_walker (self):
        return self.walker([self.editor(x) for x in self.my_list])

class EditTestForm (form.Form):
    def OnInit (self):
        self.header = urwid.Text("Header")
        self.footer = urwid.Text("Footer")

        capt=urwid.Text("This is the edit caption: ")
        edit=urwid.ListBox(urwid.SimpleListWalker([urwid.AttrMap(urwid.Edit(edit_text=(" %s " % x) * 15), None, focus_map='understand') for x in xrange(10)]))

        col=urwid.Columns([('fixed', len(capt.text)+1, capt), urwid.BoxAdapter(edit, 10)])

        self.body = urwid.Filler(col)

        self.frame = urwid.Frame(body=urwid.LineBox(urwid.Filler(
        urwid.AttrMap(
        layout.SizedFrame(body=self.body, height=10), None)
        )), header=self.header, footer=self.footer)
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
