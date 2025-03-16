import os
import wx
import pygame
from player import AudioPlayer
from buttons import create_buttons

class MyFrame(wx.Frame):
    """
    Class to create the main application window.
    """
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        panel = wx.Panel(self)

        self.player = AudioPlayer()

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Create buttons
        buttons = create_buttons(panel)

        self.play_button = buttons["play_button"]
        self.pause_button = buttons["pause_button"]
        self.resume_button = buttons["resume_button"]
        self.stop_button = buttons["stop_button"]
        self.volume_up_button = buttons["volume_up_button"]
        self.volume_down_button = buttons["volume_down_button"]
        self.seek_forward_button = buttons["seek_forward_button"]
        self.seek_backward_button = buttons["seek_backward_button"]
        self.prev_track_button = buttons["prev_track_button"]
        self.next_track_button = buttons["next_track_button"]
        self.mute_button = buttons["mute_button"]
        self.browse_button = buttons["browse_button"]

        # Bind buttons to event handlers
        self.play_button.Bind(wx.EVT_BUTTON, self.on_play_file)
        self.pause_button.Bind(wx.EVT_BUTTON, self.on_pause_file)
        self.resume_button.Bind(wx.EVT_BUTTON, self.on_resume_file)
        self.stop_button.Bind(wx.EVT_BUTTON, self.on_stop_file)
        self.volume_up_button.Bind(wx.EVT_BUTTON, self.on_volume_up)
        self.volume_down_button.Bind(wx.EVT_BUTTON, self.on_volume_down)
        self.seek_forward_button.Bind(wx.EVT_BUTTON, self.on_seek_forward)
        self.seek_backward_button.Bind(wx.EVT_BUTTON, self.on_seek_backward)
        self.prev_track_button.Bind(wx.EVT_BUTTON, self.on_prev_track)
        self.next_track_button.Bind(wx.EVT_BUTTON, self.on_next_track)
        self.mute_button.Bind(wx.EVT_BUTTON, self.on_mute)
        self.browse_button.Bind(wx.EVT_BUTTON, self.on_browse_folder)

        # Deactivate buttons initially
        self.play_button.Disable()
        self.pause_button.Hide()
        self.resume_button.Hide()
        self.stop_button.Disable()
        self.volume_up_button.Disable()
        self.volume_down_button.Disable()
        self.seek_forward_button.Disable()
        self.seek_backward_button.Disable()
        self.prev_track_button.Disable()
        self.next_track_button.Disable()
        self.mute_button.Disable()

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

        button_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer2.Add(self.mute_button, 0, wx.ALL, 2)

        self.sizer.Add(button_sizer, 0, wx.ALL | wx.LEFT, 5)
        self.sizer.Add(button_sizer2, 0, wx.ALL | wx.LEFT, 5)

        self.label = wx.StaticText(
            panel,
            label="Press the button to select a folder or play a file"
        )
        self.sizer.Add(self.label, 0, wx.ALL | wx.CENTER, 40)  # Place text 40 pixels below

        self.listbox = wx.ListBox(panel)
        self.sizer.Add(self.listbox, 1, wx.ALL | wx.EXPAND, 10)

        self.sizer.Add(self.browse_button, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(self.sizer)

        # Initialize pygame for audio playback
        pygame.mixer.init()

        self.folder_path = ""
        self.current_file = None

        # Bind hotkeys "Space", "Ctrl + Enter", "Ctrl + Space", "Ctrl + Up", "Ctrl + Down", "Ctrl + Right", "Ctrl + Left", "Page Up" and "Page Down" to buttons
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_press)

    def on_browse_folder(self, event):
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
            self.mute_button.Enable()  # Activate the "Mute" button
            self.Layout()

    def on_pause_file(self, event):
        self.player.pause()
        self.pause_button.Hide()
        self.resume_button.Show()
        self.Layout()

    def on_resume_file(self, event):
        self.player.pause()
        self.resume_button.Hide()
        self.pause_button.Show()
        self.Layout()

    def on_stop_file(self, event):
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
        self.mute_button.Disable()  # Deactivate the "Mute" button
        self.Layout()

    def on_volume_up(self, event):
        self.player.volume_up()

    def on_volume_down(self, event):
        self.player.volume_down()

    def on_seek_forward(self, event, seconds=2):
        self.player.seek(seconds)  # Seek forward

    def on_seek_backward(self, even, seconds=-2):
        self.player.seek(seconds)  # Seek backward

    def on_prev_track(self, event):
        selection = self.listbox.GetSelection()
        if selection > 0:
            self.listbox.SetSelection(selection - 1)
            self.on_play_file(None)

    def on_next_track(self, event):
        selection = self.listbox.GetSelection()
        if selection < self.listbox.GetCount() - 1:
            self.listbox.SetSelection(selection + 1)
            self.on_play_file(None)

    def on_mute(self, event):
        self.player.mute()

    def on_key_press(self, event):
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
            self.on_seek_forward(None, seconds=10)
        elif keycode == wx.WXK_LEFT and event.ControlDown():
            self.on_seek_backward(None, seconds=-10)
        elif keycode == wx.WXK_RIGHT and event.AltDown():
            self.on_seek_forward(None, seconds=30)
        elif keycode == wx.WXK_LEFT and event.AltDown():
            self.on_seek_backward(None, seconds=-30)
        elif keycode == wx.WXK_RIGHT:
            self.on_seek_forward(None)
        elif keycode == wx.WXK_LEFT:
            self.on_seek_backward(None)
        elif keycode == wx.WXK_PAGEUP:
            self.on_prev_track(None)
        elif keycode == wx.WXK_PAGEDOWN:
            self.on_next_track(None)
        elif keycode == wx.WXK_ESCAPE:
            self.on_mute(None)
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