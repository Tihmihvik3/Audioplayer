import wx
import os
from labels import COPY_LABEL, CUT_LABEL, PASTE_LABEL, DELETE_LABEL

clipboard = None

def show_context_menu(parent, listbox, folder_path):
    selection = listbox.GetSelection()
    if selection != wx.NOT_FOUND:
        file_name = listbox.GetString(selection)
        menu = wx.Menu()
        menu.Append(wx.ID_COPY, COPY_LABEL)
        menu.Append(wx.ID_CUT, CUT_LABEL)
        menu.Append(wx.ID_PASTE, PASTE_LABEL)
        menu.Append(wx.ID_DELETE, DELETE_LABEL)
        parent.Bind(wx.EVT_MENU, lambda event: on_copy(event, listbox), id=wx.ID_COPY)
        parent.Bind(wx.EVT_MENU, lambda event: on_cut(event, listbox, folder_path), id=wx.ID_CUT)
        parent.Bind(wx.EVT_MENU, lambda event: on_paste(event, listbox, folder_path), id=wx.ID_PASTE)
        parent.Bind(wx.EVT_MENU, lambda event: on_delete(event, listbox, folder_path), id=wx.ID_DELETE)
        parent.PopupMenu(menu)
        menu.Destroy()

def on_copy(event, listbox):
    global clipboard
    selection = listbox.GetSelection()
    if selection != wx.NOT_FOUND:
        clipboard = listbox.GetString(selection)

def on_cut(event, listbox, folder_path):
    global clipboard
    selection = listbox.GetSelection()
    if selection != wx.NOT_FOUND:
        clipboard = listbox.GetString(selection)
        os.remove(os.path.join(folder_path, clipboard))
        listbox.Delete(selection)

def on_paste(event, listbox, folder_path):
    global clipboard
    if clipboard:
        destination = os.path.join(folder_path, clipboard)
        if not os.path.exists(destination):
            with open(clipboard, 'rb') as src_file:
                with open(destination, 'wb') as dest_file:
                    dest_file.write(src_file.read())
            listbox.Append(clipboard)
            clipboard = None

def on_delete(event, listbox, folder_path):
    selection = listbox.GetSelection()
    if selection != wx.NOT_FOUND:
        file_name = listbox.GetString(selection)
        os.remove(os.path.join(folder_path, file_name))
        listbox.Delete(selection)