# src/form_wx_play.py
import os
import wx
import pygame
from player import AudioPlayer
from buttons import create_buttons
from labels import START_TEXT_LABEL
from context_menu import show_context_menu
from settings import SettingsDialog
from labels import DEFAULT_FOLDER_LABEL, CHOIS_FOLDER_LABEL


class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        panel = wx.Panel(self)
        self.player = AudioPlayer()
        self.sizer = wx.BoxSizer(wx.VERTICAL)
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
        self.label = wx.StaticText(panel, label=START_TEXT_LABEL)
        self.sizer.Add(self.label, 0, wx.ALL | wx.CENTER, 5)
        self.listbox = wx.ListBox(panel)
        self.sizer.Add(self.listbox, 1, wx.ALL | wx.EXPAND, 10)
        self.sizer.Add(self.browse_button, 0, wx.ALL | wx.CENTER, 5)
        panel.SetSizer(self.sizer)
        pygame.mixer.init()
        self.folder_path = ""
        self.current_file = None
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_press)
        self.load_default_folder()

    def load_default_folder(self):
        try:
            with open("default_folder.txt", "r") as file:
                self.folder_path = file.read().strip()
                self.label.SetLabel(DEFAULT_FOLDER_LABEL + self.folder_path)
                self.populate_listbox()
        except FileNotFoundError:
            pass

    def populate_listbox(self):
        self.listbox.Clear()
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith(('.mp3', '.wav', '.ogg')):
                self.listbox.Append(file_name)
        if self.listbox.GetCount() > 0:
            self.listbox.SetSelection(0)
        self.play_button.Enable()
        self.play_button.Show()
        self.listbox.SetFocus()
        self.Layout()

    def on_browse_folder(self, event):
        with wx.DirDialog(self, CHOIS_FOLDER_LABEL, style=wx.DD_DEFAULT_STYLE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.folder_path = dialog.GetPath()
                self.label.SetLabel(f"Выбрана папка: {self.folder_path}")
                self.listbox.Clear()
                for file_name in os.listdir(self.folder_path):
                    if file_name.endswith(('.mp3', '.wav', '.ogg')):
                        self.listbox.Append(file_name)
                if self.listbox.GetCount() > 0:
                    self.listbox.SetSelection(0)
                self.play_button.Enable()
                self.play_button.Show()
                self.listbox.SetFocus()
                self.Layout()

    def on_play_file(self, event):
        selection = self.listbox.GetSelection()
        if selection != wx.NOT_FOUND:
            file_name = self.listbox.GetString(selection)
            self.current_file = os.path.join(self.folder_path, file_name)
            self.player.play(self.current_file)
            self.play_button.Hide()
            self.pause_button.Show()
            self.stop_button.Enable()
            self.volume_up_button.Enable()
            self.volume_down_button.Enable()
            self.seek_forward_button.Enable()
            self.seek_backward_button.Enable()
            self.prev_track_button.Enable()
            self.next_track_button.Enable()
            self.mute_button.Enable()
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
        self.stop_button.Disable()
        self.volume_up_button.Disable()
        self.volume_down_button.Disable()
        self.seek_forward_button.Disable()
        self.seek_backward_button.Disable()
        self.prev_track_button.Disable()
        self.next_track_button.Disable()
        self.mute_button.Disable()
        self.Layout()

    def on_volume_up(self, event):
        self.player.volume_up()

    def on_volume_down(self, event):
        self.player.volume_down()

    def on_seek_forward(self, event, seconds=2):
        self.player.seek(seconds)

    def on_seek_backward(self, event, seconds=-2):
        self.player.seek(seconds)

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
        elif keycode == ord('M') and event.ControlDown():
            show_context_menu(self, self.listbox, self.folder_path)
        elif keycode == ord('P') and event.ControlDown():
            self.open_settings()
        else:
            event.Skip()

    def open_settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.ShowModal()
        settings_dialog.Destroy()

def create_window():
    app = wx.App(False)
    frame = MyFrame(None, title="TihonPlayer v1.0", size=(400, 400))
    frame.Show(True)
    frame.listbox.SetFocus()
    app.MainLoop()

create_window()