import wx

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.notebook = self.create_tabs(panel)
        sizer.Add(self.notebook, 1, wx.EXPAND)
        panel.SetSizer(sizer)

    def create_tabs(self, parent):
        notebook = wx.Notebook(parent)

        # Tab 1: Three buttons
        tab1 = wx.Panel(notebook)
        tab1_sizer = wx.BoxSizer(wx.VERTICAL)
        button1 = wx.Button(tab1, label="Button 1")
        button2 = wx.Button(tab1, label="Button 2")
        button3 = wx.Button(tab1, label="Button 3")
        tab1_sizer.Add(button1, 0, wx.ALL | wx.CENTER, 5)
        tab1_sizer.Add(button2, 0, wx.ALL | wx.CENTER, 5)
        tab1_sizer.Add(button3, 0, wx.ALL | wx.CENTER, 5)
        tab1.SetSizer(tab1_sizer)
        notebook.AddPage(tab1, "Tab 1")

        # Tab 2: Static text
        tab2 = wx.Panel(notebook)
        tab2_sizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(tab2, label="This is some text in Tab 2.")
        tab2_sizer.Add(text, 0, wx.ALL | wx.CENTER, 5)
        tab2.SetSizer(tab2_sizer)
        notebook.AddPage(tab2, "Tab 2")

        # Tab 3: Text input
        tab3 = wx.Panel(notebook)
        tab3_sizer = wx.BoxSizer(wx.VERTICAL)
        text_ctrl = wx.TextCtrl(tab3, style=wx.TE_MULTILINE)
        tab3_sizer.Add(text_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        tab3.SetSizer(tab3_sizer)
        notebook.AddPage(tab3, "Tab 3")

        return notebook

def create_window():
    app = wx.App(False)
    frame = MyFrame(None, title="Three Tabs Example", size=(400, 300))
    frame.Show(True)
    app.MainLoop()

create_window()