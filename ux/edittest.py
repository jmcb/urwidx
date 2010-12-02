#!/usr/bin/env python
import app, form, urwid, layout

import time
header = None

class EditTestForm (form.Form):
    def OnInit (self):
        global header
        header = urwid.Text("Header")
        self.footer = urwid.Text("Footer")

        capt=urwid.Text("This is the edit caption: ")
        self.data_list = [str(("%s " % x) * 15).strip() for x in xrange(10)]
        self.edit=layout.ListEditor(self.data_list)

        col=urwid.Columns([('fixed', len(capt.text)+1, capt), urwid.BoxAdapter(self.edit, 10)])

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
    try:
        app.MainLoop()
    except KeyboardInterrupt:
        print app.GetTopForm().data_list

if __name__=="__main__":
    main ()
