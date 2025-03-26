import wx
import os
import wx.adv
from buttons import create_buttons
from labels import CHOIS_FOLDER_LABEL
from player import AudioPlayer
from settings import SettingsDialog
from context_menu import ShowContextMenu
from on_key_press import OnKeyPress  # Import the new OnKeyPress class

class Tab1(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.player = AudioPlayer()

        # Initialize OnKeyPress class
        self.on_key_press = OnKeyPress(self)

        # Create a horizontal BoxSizer for the buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create buttons and add them to the horizontal BoxSizer
        buttons = create_buttons(self)
        self.play_button = buttons["play_button"]
        self.stop_button = buttons["stop_button"]
        self.seek_backward_button = buttons["seek_backward_button"]
        self.seek_forward_button = buttons["seek_forward_button"]
        self.prev_track_button = buttons["prev_track_button"]
        self.next_track_button = buttons["next_track_button"]
        self.volume_up_button = buttons["volume_up_button"]
        self.volume_down_button = buttons["volume_down_button"]
        self.browse_button = buttons["browse_button"]
        self.pause_button = buttons["pause_button"]
        self.resume_button = buttons["resume_button"]
        self.mute_button = buttons["mute_button"]

        button_sizer.Add(self.play_button, 0, wx.ALL, 1)
        button_sizer.Add(self.pause_button, 0, wx.ALL, 1)
        button_sizer.Add(self.resume_button, 0, wx.ALL, 1)
        button_sizer.Add(self.stop_button, 0, wx.ALL, 1)
        button_sizer.Add(self.seek_backward_button, 0, wx.ALL, 1)
        button_sizer.Add(self.seek_forward_button, 0, wx.ALL, 1)
        button_sizer.Add(self.prev_track_button, 0, wx.ALL, 1)
        button_sizer.Add(self.next_track_button, 0, wx.ALL, 1)
        button_sizer.Add(self.volume_down_button, 0, wx.ALL, 1)
        button_sizer.Add(self.volume_up_button, 0, wx.ALL, 1)
        button_sizer.Add(self.mute_button, 0, wx.ALL, 1)

        # Hide pause and resume buttons initially
        self.pause_button.Hide()
        self.resume_button.Hide()

        # Bind button events
        self.play_button.Bind(wx.EVT_BUTTON, self.on_play)
        self.stop_button.Bind(wx.EVT_BUTTON, self.on_stop)
        self.seek_backward_button.Bind(wx.EVT_BUTTON, self.on_seek_backward)
        self.seek_forward_button.Bind(wx.EVT_BUTTON, self.on_seek_forward)
        self.prev_track_button.Bind(wx.EVT_BUTTON, self.on_prev_track)
        self.next_track_button.Bind(wx.EVT_BUTTON, self.on_next_track)
        self.volume_up_button.Bind(wx.EVT_BUTTON, self.on_volume_up)
        self.volume_down_button.Bind(wx.EVT_BUTTON, self.on_volume_down)
        self.pause_button.Bind(wx.EVT_BUTTON, self.on_pause)
        self.resume_button.Bind(wx.EVT_BUTTON, self.on_resume)
        self.mute_button.Bind(wx.EVT_BUTTON, self.on_mute)

        # Add the horizontal BoxSizer to the vertical BoxSizer
        self.sizer.Add(button_sizer, 0, wx.ALL, 5)

        # Add a label to the panel between buttons and listbox
        self.label = wx.StaticText(self, label="Плеер 1")
        self.sizer.Add(self.label, 0, wx.ALL, 5)

        # Create a ListBox and add it to the vertical BoxSizer
        self.listbox = wx.ListBox(self)
        self.sizer.Add(self.listbox, 1, wx.EXPAND | wx.ALL, 5)

        # Create the Browse button and add it to the vertical BoxSizer
        self.browse_button.Bind(wx.EVT_BUTTON, self.on_browse_folder)
        self.sizer.Add(self.browse_button, 0, wx.ALL, 5)

        # Add a label to display the active tab information
        self.active_tab_label = wx.StaticText(self, label="")
        self.sizer.Add(self.active_tab_label, 0, wx.ALL, 5)

        self.SetSizer(self.sizer)

        self.folder_path = ""
        self.current_file = None

        # Define the accelerator table for keyboard shortcuts
        browse_id = wx.NewIdRef()
        show_info_id = wx.NewIdRef()
        refresh_listbox_id = wx.NewIdRef()  # Add ID for refresh listbox
        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('B'), browse_id),  # Ctrl+B for Browse
            (wx.ACCEL_NORMAL, wx.WXK_F1, show_info_id),  # F1 for showing info
            (wx.ACCEL_NORMAL, wx.WXK_F5, refresh_listbox_id)  # F5 for refreshing listbox
        ])
        self.SetAcceleratorTable(accel_tbl)

        # Bind the accelerator table event to the on_browse_folder method
        self.Bind(wx.EVT_MENU, self.on_browse_folder, id=browse_id)
        self.Bind(wx.EVT_MENU, self.on_show_info, id=show_info_id)
        self.Bind(wx.EVT_MENU, self.on_refresh_listbox, id=refresh_listbox_id)  # Bind refresh listbox event

        # Bind listbox selection event
        self.listbox.Bind(wx.EVT_LISTBOX, self.on_listbox_selection)

        # Bind key press event
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_press.on_key_press)  # Update binding

        # Load default folder and populate listbox
        self.load_default_folder()

        # Update button states initially
        self.update_button_states()

    def load_default_folder(self):
        try:
            with open("default_folder.txt", "r") as file:
                self.folder_path = file.read().strip()
                self.populate_listbox()
                self.listbox.SetFocus()  # Set focus to the listbox after loading
        except FileNotFoundError:
            pass

    def populate_listbox(self):
        self.listbox.Clear()
        if os.path.isdir(self.folder_path):
            for file_name in os.listdir(self.folder_path):
                if file_name.endswith(('.mp3', '.wav', '.ogg')):
                    self.listbox.Append(file_name)
            if self.listbox.GetCount() > 0:
                self.listbox.SetSelection(0)
        self.update_button_states()

    def on_browse_folder(self, event):
        try:
            with open("default_folder.txt", "r") as file:
                default_path = file.read().strip()
        except FileNotFoundError:
            default_path = ""

        with wx.DirDialog(self, CHOIS_FOLDER_LABEL, defaultPath=default_path, style=wx.DD_DEFAULT_STYLE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.folder_path = dialog.GetPath()
                self.populate_listbox()
                self.listbox.SetFocus()  # Set focus to the listbox
    def on_play(self, event):
        selection = self.listbox.GetSelection()
        if selection != wx.NOT_FOUND:
            file_name = self.listbox.GetString(selection)
            self.current_file = os.path.join(self.folder_path, file_name)
            print(f"Playing file: {self.current_file}")  # Debug print
            self.player.play(self.current_file)
            self.play_button.Hide()
            self.pause_button.Show()
            self.Layout()

    def on_stop(self, event):
        print("Stopping playback")  # Debug print
        self.player.stop()
        self.play_button.Show()
        self.pause_button.Hide()
        self.resume_button.Hide()
        self.Layout()

    def on_seek_backward(self, event, seconds=-2):
        print(f"seconds = {seconds}")  # Debug print
        self.player.seek(seconds)  # Seek backward by 10 seconds

    def on_seek_forward(self, event, seconds=2):
        print(f"seconds = {seconds}")  # Debug print
        self.player.seek(seconds)  # Seek forward by 10 seconds

    def on_prev_track(self, event):
        selection = self.listbox.GetSelection()
        if selection > 0:
            self.listbox.SetSelection(selection - 1)
            self.on_play(None)

    def on_next_track(self, event):
        selection = self.listbox.GetSelection()
        if selection < self.listbox.GetCount() - 1:
            self.listbox.SetSelection(selection + 1)
            self.on_play(None)

    def on_volume_up(self, event):
        print("Volume up")  # Debug print
        self.player.volume_up()

    def on_volume_down(self, event):
        print("Volume down")  # Debug print
        self.player.volume_down()

    def on_pause(self, event):
        print("Pausing playback")  # Debug print
        self.player.pause()
        self.pause_button.Hide()
        self.resume_button.Show()
        self.Layout()

    def on_resume(self, event):
        print("Resuming playback")  # Debug print
        self.player.pause()
        self.resume_button.Hide()
        self.pause_button.Show()
        self.Layout()

    def on_mute(self, event):
        print("Muting playback")  # Debug print
        self.player.mute()

    def on_listbox_selection(self, event):
        self.update_button_states()

    def update_button_states(self):
        selection = self.listbox.GetSelection()
        enable = selection != wx.NOT_FOUND
        self.play_button.Enable(enable)
        self.stop_button.Enable(enable)
        self.seek_backward_button.Enable(enable)
        self.seek_forward_button.Enable(enable)
        self.prev_track_button.Enable(enable)
        self.next_track_button.Enable(enable)
        self.volume_up_button.Enable(enable)
        self.volume_down_button.Enable(enable)
        self.pause_button.Enable(enable)
        self.resume_button.Enable(enable)
        self.mute_button.Enable(enable)

    def on_show_info(self, event):
        notebook = self.GetParent()
        active_tab_index = notebook.GetSelection()
        active_tab_label = ""
        active_tab_info = notebook.GetPageText(active_tab_index)
        if active_tab_info == "Tab 1":
            active_tab_label = "Плеер 1"
        elif active_tab_info == "Tab 2":
            active_tab_label = "Плеер 2"
        elif active_tab_info == "Tab 3":
            active_tab_label = "Плеер 3"
        self.active_tab_label.SetLabel(f"Активна вкладка: {active_tab_label}")
        message = f"Активна вкладка: {active_tab_label}\nОткрыта папка: {self.folder_path}"
        wx.adv.NotificationMessage("Информация:", message).Show(timeout=wx.adv.NotificationMessage.Timeout_Auto)

    def on_play_sample(self, event, file_name_sample):
        sample_file = os.path.join("sample", file_name_sample)
        if os.path.exists(sample_file):
            print(f"Playing sample file: {sample_file}")  # Debug print
            self.player.on_play_sample(sample_file)
        else:
            wx.MessageBox("Sample file not found!", "Error", wx.OK | wx.ICON_ERROR)

    def on_refresh_listbox(self, event):
        self.populate_listbox()
