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

        # Bind the close event to the on_close method
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        # Stop all processes and clear the player
        for tab in [self.notebook.tab1, self.notebook.tab2, self.notebook.tab3]:
            tab.player.stop()
        self.Destroy()

def create_window():
    app = wx.App(False)
    frame = MyFrame(None, title="TihonPlayer v1.1", size=(400, 400))
    frame.Show(True)

    app.MainLoop()

create_window()

