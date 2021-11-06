import wx
import os

class LoadGpxDialog(wx.Frame):
    def __init__(self):
        super(LoadGpxDialog, self).__init__(*args, **kwargs)

    def open(self):
        openFileDialog = wx.FileDialog(self, "Open", "", "",
                                       "Python files (*.py)|*.py",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        print(openFileDialog.GetPath())
        openFileDialog.Destroy()