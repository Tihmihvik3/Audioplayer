import wx
from player import AudioPlayer

class MyApp(wx.App):
    def OnInit(self):
        self.frame = wx.Frame(None, title="Audio Player", size=(400, 300))
        self.panel = wx.Panel(self.frame)

        self.player = AudioPlayer()

        self.play_button = wx.Button(self.panel, label="Play")
        self.pause_button = wx.Button(self.panel, label="Pause")
        self.stop_button = wx.Button(self.panel, label="Stop")
        self.seek_forward_button = wx.Button(self.panel, label="Seek Forward")
        self.seek_backward_button = wx.Button(self.panel, label="Seek Backward")
        self.volume_up_button = wx.Button(self.panel, label="Volume Up")
        self.volume_down_button = wx.Button(self.panel, label="Volume Down")
        self.time_label = wx.StaticText(self.panel, label="Current Time: 0:0.0")

        self.play_button.Bind(wx.EVT_BUTTON, self.on_play)
        self.pause_button.Bind(wx.EVT_BUTTON, self.on_pause)
        self.stop_button.Bind(wx.EVT_BUTTON, self.on_stop)
        self.seek_forward_button.Bind(wx.EVT_BUTTON, self.on_seek_forward)
        self.seek_backward_button.Bind(wx.EVT_BUTTON, self.on_seek_backward)
        self.volume_up_button.Bind(wx.EVT_BUTTON, self.on_volume_up)
        self.volume_down_button.Bind(wx.EVT_BUTTON, self.on_volume_down)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.play_button, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.pause_button, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.stop_button, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.seek_forward_button, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.seek_backward_button, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.volume_up_button, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.volume_down_button, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.time_label, 0, wx.ALL | wx.CENTER, 5)

        self.panel.SetSizer(sizer)
        self.frame.Show()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_time, self.timer)
        self.timer.Start(100)  # Обновление каждые 100 миллисекунд

        return True

    def on_play(self, event):
        self.player.play("d:/Python/MyPython2/audio-player/src/1.mp3")

    def on_pause(self, event):
        self.player.pause()

    def on_stop(self, event):
        self.player.stop()

    def on_seek_forward(self, event):
        self.player.seek(2)  # Перемотка на 2 секунды вперед

    def on_seek_backward(self, event):
        self.player.seek(-2)  # Перемотка на 2 секунды назад

    def on_volume_up(self, event):
        self.player.volume_up()

    def on_volume_down(self, event):
        self.player.volume_down()

    def update_time(self, event):
        current_time = self.player.get_current_time()
        self.time_label.SetLabel(f"Current Time: {current_time}")

    def OnExit(self):
        self.player.stop()
        return 0

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()