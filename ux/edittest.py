#!/usr/bin/env python
import app, form, urwid, layout, edit

class EditTestForm (form.Form):
    def OnInit (self):
        global header
        header = urwid.Text("Header")
        self.footer = urwid.Text("Footer")

        self.data_list = [str(("%s " % x) * 15).strip() for x in xrange(10)]

        self.frame = urwid.Frame(body=urwid.LineBox(urwid.Filler(
        urwid.AttrMap(edit.ListEditor("This is a test:", self.data_list, 10), None)
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
