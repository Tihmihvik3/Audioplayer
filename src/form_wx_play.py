import os
import wx
import pygame
from player import AudioPlayer

class MyFrame(wx.Frame):
    """
    Class to create the main application window.
    """
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        panel = wx.Panel(self)

        self.player = AudioPlayer()

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Load icons for buttons
        stop_icon = wx.Bitmap("icons/stop.png", wx.BITMAP_TYPE_PNG)
        browse_icon = wx.Bitmap("icons/browse.png", wx.BITMAP_TYPE_PNG)
        play_icon = wx.Bitmap("icons/play.png", wx.BITMAP_TYPE_PNG)
        pause_icon = wx.Bitmap("icons/pause.png", wx.BITMAP_TYPE_PNG)
        resume_icon = wx.Bitmap("icons/resume.png", wx.BITMAP_TYPE_PNG)
        volume_up_icon = wx.Bitmap("icons/volume_up.png", wx.BITMAP_TYPE_PNG)
        volume_down_icon = wx.Bitmap("icons/volume_down.png", wx.BITMAP_TYPE_PNG)
        seek_forward_icon = wx.Bitmap("icons/seek_forward.png", wx.BITMAP_TYPE_PNG)
        seek_backward_icon = wx.Bitmap("icons/seek_backward.png", wx.BITMAP_TYPE_PNG)
        prev_track_icon = wx.Bitmap("icons/prev_track.png", wx.BITMAP_TYPE_PNG)
        next_track_icon = wx.Bitmap("icons/next_track.png", wx.BITMAP_TYPE_PNG)

        self.play_button = wx.BitmapButton(panel, bitmap=play_icon)
        self.play_button.SetToolTip("Play (Ctrl + Enter)")
        self.play_button.SetName("play_button")
        self.play_button.SetLabel("Play (Space)")
        self.play_button.Bind(wx.EVT_BUTTON, self.on_play_file)
        self.play_button.Disable()  # Deactivate the "Play" button

        self.pause_button = wx.BitmapButton(panel, bitmap=pause_icon)
        self.pause_button.SetToolTip("Pause (Space)")
        self.pause_button.SetName("pause_button")
        self.pause_button.SetLabel("Pause (Space)")
        self.pause_button.Bind(wx.EVT_BUTTON, self.on_pause_file)
        self.pause_button.Hide()

        self.resume_button = wx.BitmapButton(panel, bitmap=resume_icon)
        self.resume_button.SetToolTip("Resume (Space)")
        self.resume_button.SetName("resume_button")
        self.resume_button.SetLabel("Resume (Space)")
        self.resume_button.Bind(wx.EVT_BUTTON, self.on_resume_file)
        self.resume_button.Hide()

        self.stop_button = wx.BitmapButton(panel, bitmap=stop_icon)
        self.stop_button.SetToolTip("Stop (Ctrl + Space)")
        self.stop_button.SetName("stop_button")
        self.stop_button.SetLabel("Stop (Ctrl + Space)")
        self.stop_button.Bind(wx.EVT_BUTTON, self.on_stop_file)
        self.stop_button.Disable()  # Deactivate the "Stop" button

        self.volume_up_button = wx.BitmapButton(panel, bitmap=volume_up_icon)
        self.volume_up_button.SetToolTip("Volume Up (Ctrl + Up)")
        self.volume_up_button.SetName("volume_up_button")
        self.volume_up_button.SetLabel("Volume Up (Ctrl + Up)")
        self.volume_up_button.Bind(wx.EVT_BUTTON, self.on_volume_up)
        self.volume_up_button.Disable()  # Deactivate the "Volume Up" button

        self.volume_down_button = wx.BitmapButton(panel, bitmap=volume_down_icon)
        self.volume_down_button.SetToolTip("Volume Down (Ctrl + Down)")
        self.volume_down_button.SetName("volume_down_button")
        self.volume_down_button.SetLabel("Volume Down (Ctrl + Down)")
        self.volume_down_button.Bind(wx.EVT_BUTTON, self.on_volume_down)
        self.volume_down_button.Disable()  # Deactivate the "Volume Down" button

        self.seek_forward_button = wx.BitmapButton(panel, bitmap=seek_forward_icon)
        self.seek_forward_button.SetToolTip("Seek Forward (Ctrl + Right)")
        self.seek_forward_button.SetName("seek_forward_button")
        self.seek_forward_button.SetLabel("Seek Forward (Ctrl + Right)")
        self.seek_forward_button.Bind(wx.EVT_BUTTON, self.on_seek_forward)
        self.seek_forward_button.Disable()  # Deactivate the "Seek Forward" button

        self.seek_backward_button = wx.BitmapButton(panel, bitmap=seek_backward_icon)
        self.seek_backward_button.SetToolTip("Seek Backward (Ctrl + Left)")
        self.seek_backward_button.SetName("seek_backward_button")
        self.seek_backward_button.SetLabel("Seek Backward (Ctrl + Left)")
        self.seek_backward_button.Bind(wx.EVT_BUTTON, self.on_seek_backward)
        self.seek_backward_button.Disable()  # Deactivate the "Seek Backward" button

        self.prev_track_button = wx.BitmapButton(panel, bitmap=prev_track_icon)
        self.prev_track_button.SetToolTip("Previous Track (Page Up)")
        self.prev_track_button.SetName("prev_track_button")
        self.prev_track_button.SetLabel("Previous Track (Page Up)")
        self.prev_track_button.Bind(wx.EVT_BUTTON, self.on_prev_track)
        self.prev_track_button.Disable()  # Deactivate the "Previous Track" button

        self.next_track_button = wx.BitmapButton(panel, bitmap=next_track_icon)
        self.next_track_button.SetToolTip("Next Track (Page Down)")
        self.next_track_button.SetName("next_track_button")
        self.next_track_button.SetLabel("Next Track (Page Down)")
        self.next_track_button.Bind(wx.EVT_BUTTON, self.on_next_track)
        self.next_track_button.Disable()  # Deactivate the "Next Track" button

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(self.play_button, 0, wx.LEFT, 2)
        button_sizer.Add(self.pause_button, 0, wx.ALL, 2)
        button_sizer.Add(self.resume_button, 0, wx.ALL, 2)
        button_sizer.Add(self.stop_button, 0, wx.ALL, 2)
        button_sizer.Add(self.seek_forward_button, 0, wx.ALL, 2)
        button_sizer.Add(self.seek_backward_button, 0, wx.ALL, 2)
        button_sizer.Add(self.prev_track_button, 0, wx.ALL, 2)
        button_sizer.Add(self.next_track_button, 0, wx.ALL, 2)
        button_sizer.Add(self.volume_up_button, 0, wx.ALL, 2)
        button_sizer.Add(self.volume_down_button, 0, wx.ALL, 2)

        self.sizer.Add(button_sizer, 0, wx.ALL | wx.LEFT, 5)

        self.label = wx.StaticText(
            panel,
            label="Press the button to select a folder or play a file"
        )
        self.sizer.Add(self.label, 0, wx.ALL | wx.CENTER, 40)  # Place text 40 pixels below

        self.listbox = wx.ListBox(panel)
        self.sizer.Add(self.listbox, 1, wx.ALL | wx.EXPAND, 10)

        self.browse_button = wx.BitmapButton(panel, bitmap=browse_icon)
        self.browse_button.SetToolTip("Browse (Ctrl + B)")
        self.browse_button.SetName("browse_button")
        self.browse_button.SetLabel("Browse (Ctrl + B)")
        self.browse_button.Bind(wx.EVT_BUTTON, self.on_browse_folder)
        self.sizer.Add(self.browse_button, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(self.sizer)

        # Initialize pygame for audio playback
        pygame.mixer.init()

        self.folder_path = ""
        self.current_file = None

        # Bind hotkeys "Space", "Ctrl + Enter", "Ctrl + Space", "Ctrl + Up", "Ctrl + Down", "Ctrl + Right", "Ctrl + Left", "Page Up" and "Page Down" to buttons
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_press)

    def on_browse_folder(self, event):
        """
        Event handler for the button to open the folder selection dialog.
        """
        with wx.DirDialog(self, "Select a folder", style=wx.DD_DEFAULT_STYLE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.folder_path = dialog.GetPath()
                self.label.SetLabel(f"Selected folder: {self.folder_path}")
                self.listbox.Clear()
                for file_name in os.listdir(self.folder_path):
                    if file_name.endswith(('.mp3', '.wav', '.ogg')):  # Audio file filter
                        self.listbox.Append(file_name)
                if self.listbox.GetCount() > 0:
                    self.listbox.SetSelection(0)  # Focus on the first file in the list
                self.play_button.Enable()  # Activate the "Play" button
                self.play_button.Show()  # Show the "Play" button
                self.listbox.SetFocus()  # Focus on the listbox
                self.Layout()

    def on_play_file(self, event):
        """
        Event handler for the button to play the selected audio file.
        """
        selection = self.listbox.GetSelection()
        if selection != wx.NOT_FOUND:
            file_name = self.listbox.GetString(selection)
            self.current_file = os.path.join(self.folder_path, file_name)
            self.player.play(self.current_file)
            self.play_button.Hide()
            self.pause_button.Show()
            self.stop_button.Enable()  # Activate the "Stop" button
            self.volume_up_button.Enable()  # Activate the "Volume Up" button
            self.volume_down_button.Enable()  # Activate the "Volume Down" button
            self.seek_forward_button.Enable()  # Activate the "Seek Forward" button
            self.seek_backward_button.Enable()  # Activate the "Seek Backward" button
            self.prev_track_button.Enable()  # Activate the "Previous Track" button
            self.next_track_button.Enable()  # Activate the "Next Track" button
            self.Layout()

    def on_pause_file(self, event):
        """
        Event handler for the button to pause audio playback.
        """
        self.player.pause()
        self.pause_button.Hide()
        self.resume_button.Show()
        self.Layout()

    def on_resume_file(self, event):
        """
        Event handler for the button to resume audio playback.
        """
        self.player.pause()
        self.resume_button.Hide()
        self.pause_button.Show()
        self.Layout()

    def on_stop_file(self, event):
        """
        Event handler for the button to stop audio playback.
        """
        self.player.stop()
        self.play_button.Show()
        self.pause_button.Hide()
        self.resume_button.Hide()
        self.stop_button.Disable()  # Deactivate the "Stop" button
        self.volume_up_button.Disable()  # Deactivate the "Volume Up" button
        self.volume_down_button.Disable()  # Deactivate the "Volume Down" button
        self.seek_forward_button.Disable()  # Deactivate the "Seek Forward" button
        self.seek_backward_button.Disable()  # Deactivate the "Seek Backward" button
        self.prev_track_button.Disable()  # Deactivate the "Previous Track" button
        self.next_track_button.Disable()  # Deactivate the "Next Track" button
        self.Layout()

    def on_volume_up(self, event):
        """
        Event handler for the button to increase the volume level.
        """
        self.player.volume_up()

    def on_volume_down(self, event):
        """
        Event handler for the button to decrease the volume level.
        """
        self.player.volume_down()

    def on_seek_forward(self, event):
        """
        Event handler for the button to seek forward.
        """
        self.player.seek(2)  # Seek forward by 2 seconds

    def on_seek_backward(self, event):
        """
        Event handler for the button to seek backward.
        """
        self.player.seek(-2)  # Seek backward by 2 seconds

    def on_prev_track(self, event):
        """
        Event handler for the button to go to the previous track.
        """
        selection = self.listbox.GetSelection()
        if selection > 0:
            self.listbox.SetSelection(selection - 1)
            self.on_play_file(None)

    def on_next_track(self, event):
        """
        Event handler for the button to go to the next track.
        """
        selection = self.listbox.GetSelection()
        if selection < self.listbox.GetCount() - 1:
            self.listbox.SetSelection(selection + 1)
            self.on_play_file(None)

    def on_key_press(self, event):
        """
        Event handler for key press.
        """
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_SPACE and not event.ControlDown():
            if self.play_button.IsShown():
                self.on_play_file(None)
            elif self.pause_button.IsShown():
                self.on_pause_file(None)
            elif self.resume_button.IsShown():
                self.on_resume_file(None)
        elif keycode in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER) and event.ControlDown():
            self.on_play_file(None)
        elif keycode == ord('B') and event.ControlDown():
            self.on_browse_folder(None)
        elif keycode == wx.WXK_SPACE and event.ControlDown():
            if self.stop_button.IsEnabled():
                self.on_stop_file(None)
        elif keycode == wx.WXK_UP and event.ControlDown():
            self.on_volume_up(None)
        elif keycode == wx.WXK_DOWN and event.ControlDown():
            self.on_volume_down(None)
        elif keycode == wx.WXK_RIGHT and event.ControlDown():
            self.on_seek_forward(None)
        elif keycode == wx.WXK_LEFT and event.ControlDown():
            self.on_seek_backward(None)
        elif keycode == wx.WXK_PAGEUP:
            self.on_prev_track(None)
        elif keycode == wx.WXK_PAGEDOWN:
            self.on_next_track(None)
        else:
            event.Skip()

def create_window():
    """
    Function to create and run the main application window.
    """
    app = wx.App(False)
    frame = MyFrame(None, title="TihonPlayer", size=(400, 400))
    frame.Show(True)
    frame.listbox.SetFocus()  # Focus on the listbox after the window starts
    app.MainLoop()

# Run the form window
create_window()