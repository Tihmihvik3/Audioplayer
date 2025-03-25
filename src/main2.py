import wx
from tabs import Tabs

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.notebook = Tabs(panel)
        sizer.Add(self.notebook, 1, wx.EXPAND)
        panel.SetSizer(sizer)

        # Activate the first tab and set focus to the listbox
        self.notebook.SetSelection(0)
        self.notebook.tab1.listbox.SetFocus()

def create_window():
    app = wx.App(False)
    frame = MyFrame(None, title="TihonPlayer v1.1", size=(400, 400))
    frame.Show(True)
    app.MainLoop()

create_window()
