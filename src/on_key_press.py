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
        elif keycode == ord('P') and event.ShiftDown():
            self.tab.on_play_sample(None, "10.mp3")
        elif keycode == ord('B') and event.ShiftDown():
            self.tab.on_play_sample(None, "24.mp3")
        elif keycode == ord('M') and event.ShiftDown():
            self.tab.on_play_sample(None, "26.mp3")
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
        elif keycode == ord('P') and event.ControlDown():
            settings_dialog = SettingsDialog(self.tab)
            settings_dialog.ShowModal()
            settings_dialog.Destroy()
        elif keycode == wx.WXK_ESCAPE:
            self.tab.on_mute(None)
        elif keycode == ord('M') and event.ControlDown():
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
        elif keycode == wx.WXK_DELETE:
            context_menu = ShowContextMenu(self.tab, self.tab.listbox, self.tab.folder_path)
            context_menu.on_delete(None)
        elif keycode == ord('C') and event.ControlDown():
            context_menu = ShowContextMenu(self.tab, self.tab.listbox, self.tab.folder_path)
            context_menu.on_copy(None)
        elif keycode == ord('V') and event.ControlDown():
            context_menu = ShowContextMenu(self.tab, self.tab.listbox, self.tab.folder_path)
            context_menu.on_paste(None)
        elif keycode == wx.WXK_F2:
            context_menu = ShowContextMenu(self.tab, self.tab.listbox, self.tab.folder_path)
            context_menu.on_rename(None)
        elif keycode == wx.WXK_F5:
            self.tab.on_refresh_listbox(None)

        # Запуск семплов.
        elif keycode == ord('Q') and event.ShiftDown():
            self.tab.on_play_sample(None, "01.mp3")
        elif keycode == ord('W') and event.ShiftDown():
            self.tab.on_play_sample(None, "02.mp3")
        elif keycode == ord('E') and event.ShiftDown():
            self.tab.on_play_sample(None, "03.mp3")
        elif keycode == ord('R') and event.ShiftDown():
            self.tab.on_play_sample(None, "04.mp3")
        elif keycode == ord('T') and event.ShiftDown():
            self.tab.on_play_sample(None, "05.mp3")
        elif keycode == ord('Y') and event.ShiftDown():
            self.tab.on_play_sample(None, "06.mp3")
        elif keycode == ord('U') and event.ShiftDown():
            self.tab.on_play_sample(None, "07.mp3")
        elif keycode == ord('I') and event.ShiftDown():
            self.tab.on_play_sample(None, "08.mp3")
        elif keycode == ord('O') and event.ShiftDown():
            self.tab.on_play_sample(None, "09.mp3")
        elif keycode == ord('A') and event.ShiftDown():
            self.tab.on_play_sample(None, "11.mp3")
        elif keycode == ord('S') and event.ShiftDown():
            self.tab.on_play_sample(None, "12.mp3")
        elif keycode == ord('D') and event.ShiftDown():
            self.tab.on_play_sample(None, "13.mp3")
        elif keycode == ord('F') and event.ShiftDown():
            self.tab.on_play_sample(None, "14.mp3")
        elif keycode == ord('G') and event.ShiftDown():
            self.tab.on_play_sample(None, "15.mp3")
        elif keycode == ord('H') and event.ShiftDown():
            self.tab.on_play_sample(None, "16.mp3")
        elif keycode == ord('J') and event.ShiftDown():
            self.tab.on_play_sample(None, "17.mp3")
        elif keycode == ord('K') and event.ShiftDown():
            self.tab.on_play_sample(None, "18.mp3")
        elif keycode == ord('L') and event.ShiftDown():
            self.tab.on_play_sample(None, "19.mp3")
        elif keycode == ord('Z') and event.ShiftDown():
            self.tab.on_play_sample(None, "20.mp3")
        elif keycode == ord('X') and event.ShiftDown():
            self.tab.on_play_sample(None, "21.mp3")
        elif keycode == ord('C') and event.ShiftDown():
            self.tab.on_play_sample(None, "22.mp3")
        elif keycode == ord('V') and event.ShiftDown():
            self.tab.on_play_sample(None, "23.mp3")
        elif keycode == ord('N') and event.ShiftDown():
            self.tab.on_play_sample(None, "25.mp3")
        elif keycode == ord('M') and event.ShiftDown():
            self.tab.on_play_sample(None, "26.mp3")

        else:
            event.Skip()
