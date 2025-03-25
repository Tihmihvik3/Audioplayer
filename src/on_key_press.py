import wx
from settings import SettingsDialog
from context_menu import ShowContextMenu


class OnKeyPress:
    def __init__(self, tab):
        self.tab = tab

    def on_key_press(self, event):
        keycode = event.GetKeyCode()
        notebook = self.tab.GetParent()  # Get the notebook directly
        if keycode == wx.WXK_UP or keycode == wx.WXK_DOWN:
            if not self.tab.listbox.HasFocus():
                self.tab.listbox.SetFocus()
                return
        if keycode == wx.WXK_SPACE and event.ControlDown():
            if self.tab.stop_button.IsEnabled():
                self.tab.on_stop(None)
        elif keycode == wx.WXK_SPACE:
            if self.tab.play_button.IsShown():
                self.tab.on_play(None)
            elif self.tab.pause_button.IsShown():
                self.tab.on_pause(None)
            elif self.tab.resume_button.IsShown():
                self.tab.on_resume(None)
        elif keycode == wx.WXK_RIGHT and event.ControlDown():
            self.tab.on_seek_forward(None, seconds=10)
        elif keycode == wx.WXK_LEFT and event.ControlDown():
            self.tab.on_seek_backward(None, seconds=-10)
        elif keycode == wx.WXK_RIGHT and event.AltDown():
            self.tab.on_seek_forward(None, seconds=30)
        elif keycode == wx.WXK_LEFT and event.AltDown():
            self.tab.on_seek_backward(None, seconds=-30)
        elif keycode == wx.WXK_LEFT:
            self.tab.on_seek_backward(None)
        elif keycode == wx.WXK_RIGHT:
            self.tab.on_seek_forward(None)
        elif keycode == wx.WXK_UP and event.ControlDown():
            self.tab.on_volume_up(None)
        elif keycode == wx.WXK_DOWN and event.ControlDown():
            self.tab.on_volume_down(None)
        elif keycode == wx.WXK_PAGEUP:
            self.tab.on_prev_track(None)
        elif keycode == wx.WXK_PAGEDOWN:
            self.tab.on_next_track(None)
        elif keycode in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            self.tab.on_play(None)
        elif keycode == ord('B'):
            self.tab.on_browse_folder(None)
        elif keycode == ord('P'):
            settings_dialog = SettingsDialog(self.tab)
            settings_dialog.ShowModal()
            settings_dialog.Destroy()
        elif keycode == wx.WXK_ESCAPE:
            self.tab.on_mute(None)
        elif keycode == ord('M'):
            context_menu = ShowContextMenu(self.tab, self.tab.listbox, self.tab.folder_path)
            context_menu.show()
        elif keycode == ord('1'):
            notebook.SetSelection(0)
        elif keycode == ord('2'):
            notebook.SetSelection(1)
        elif keycode == ord('3'):
            notebook.SetSelection(2)
        elif keycode == wx.WXK_F1:
            self.tab.on_show_info(None)

        # Запуск семплов.
        elif keycode == ord('Q') and event.ShiftDown():
            self.tab.on_play_sample(None, "01.mp3")
        elif keycode == ord('W') and event.ShiftDown():
            self.tab.on_play_sample(None, "02.mp3")
        elif keycode == ord('E') and event.ShiftDown():
            self.tab.on_play_sample(None, "03.mp3")
        else:
            event.Skip()
