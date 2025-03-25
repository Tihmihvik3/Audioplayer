# context_menu.py
import wx
import os
from labels import COPY_LABEL, CUT_LABEL, PASTE_LABEL, DELETE_LABEL

clipboard = None

class ShowContextMenu:
    def __init__(self, parent, listbox, folder_path):
        self.parent = parent
        self.listbox = listbox
        self.folder_path = folder_path

    def show(self):
        selection = self.listbox.GetSelection()
        if selection != wx.NOT_FOUND:
            file_name = self.listbox.GetString(selection)
            menu = wx.Menu()
            menu.Append(wx.ID_COPY, COPY_LABEL)
            menu.Append(wx.ID_CUT, CUT_LABEL)
            menu.Append(wx.ID_PASTE, PASTE_LABEL)
            menu.Append(wx.ID_DELETE, DELETE_LABEL)
            self.parent.Bind(wx.EVT_MENU, lambda event: self.on_copy(event), id=wx.ID_COPY)
            self.parent.Bind(wx.EVT_MENU, lambda event: self.on_cut(event), id=wx.ID_CUT)
            self.parent.Bind(wx.EVT_MENU, lambda event: self.on_paste(event), id=wx.ID_PASTE)
            self.parent.Bind(wx.EVT_MENU, lambda event: self.on_delete(event), id=wx.ID_DELETE)
            self.parent.PopupMenu(menu)
            menu.Destroy()

    def on_copy(self, event):
        global clipboard
        selection = self.listbox.GetSelection()
        if selection != wx.NOT_FOUND:
            clipboard = self.listbox.GetString(selection)

    def on_cut(self, event):
        global clipboard
        selection = self.listbox.GetSelection()
        if selection != wx.NOT_FOUND:
            clipboard = self.listbox.GetString(selection)
            os.remove(os.path.join(self.folder_path, clipboard))
            self.listbox.Delete(selection)

    def on_paste(self, event):
        global clipboard
        if clipboard:
            destination = os.path.join(self.folder_path, clipboard)
            if not os.path.exists(destination):
                with open(os.path.join(self.folder_path, clipboard), 'rb') as src_file:
                    with open(destination, 'wb') as dest_file:
                        dest_file.write(src_file.read())
                self.listbox.Append(clipboard)
                clipboard = None

    def on_delete(self, event):
        selection = self.listbox.GetSelection()
        if selection != wx.NOT_FOUND:
            file_name = self.listbox.GetString(selection)
            os.remove(os.path.join(self.folder_path, file_name))
            self.listbox.Delete(selection)

