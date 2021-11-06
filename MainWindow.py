import wx
import LoginDialog
import gpxParse
import sqlAlch


class MainWindow(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.initUI()
        dlg = LoginDialog.LoginDialog()
        dlg.ShowModal()
        authenticated = dlg.logged_in
        self.username = dlg.username
        if not authenticated:
            self.Close()

    def initUI(self):

        verticalBox = wx.BoxSizer(wx.VERTICAL)
        self.toolbar1 = self.CreateToolBar()
        tLoad = self.toolbar1.AddTool(wx.ID_ANY, 'Load', wx.Bitmap('ico/download.png'))
        tSettings = self.toolbar1.AddTool(wx.ID_ANY, 'Settings', wx.Bitmap('ico/settings.png'))
        tQuit = self.toolbar1.AddTool(wx.ID_ANY, 'Quit', wx.Bitmap('ico/cancel.png'))

        self.toolbar1.Realize()
        verticalBox.Add(self.toolbar1, 0, wx.EXPAND)
        self.Bind(wx.EVT_TOOL, self.quit, tQuit)
        self.Bind(wx.EVT_TOOL, self.gpxLoad, tLoad)
        self.SetSizer(verticalBox)
        self.SetSize((1350,750))
        self.SetTitle('GPX')
        self.Center()

    def quit(self, e):
        self.Close()

    def gpxLoad(self, e):
        try:
            openFileDialog = wx.FileDialog(self, "Open", "", "",
                                           "GPX Files (*.gpx)|*.gpx",
                                           wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

            openFileDialog.ShowModal()
            print(openFileDialog.GetPath())
            gpxPath = openFileDialog.GetPath()
            gpxObject = gpxParse.GpxRecord(self.username)
            gpxObject.parseFile(gpxPath)
            sqlAlch.insertGpxTrack(self.username, gpxObject.avgSpeed, gpxObject.distance, gpxObject.avgHr, gpxObject.rideDate,
                                   gpxObject.rideTime,
                                   gpxObject.serializedPointsArray, gpxObject.serializedHrArray,
                                   gpxObject.serializedElevationArray)
            openFileDialog.Destroy()
        except:
            wx.MessageBox("File not added!", "Message", wx.OK | wx.ICON_ERROR)
            pass


def main():
    app = wx.App(False)
    mw = MainWindow(None)
    mw.Show()
    app.MainLoop()




