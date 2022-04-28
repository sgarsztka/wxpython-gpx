import wx
import LoginDialog
import gpxParse
import sqlAlch
import wx.html2
import wx.html
import pathlib2
import os
from datetime import datetime

class MyBrowser(wx.Frame):
    loggedUser = ""
    def __init__(self, *args, **kwargs):
        super(MyBrowser, self).__init__(*args, **kwargs)
        dlg = LoginDialog.LoginDialog()
        dlg.ShowModal()
        authenticated = dlg.logged_in
        self.username = dlg.username
        MyBrowser.loggedUser = dlg.username
        if not authenticated:
            self.Close()
        self.initUI()

    def initUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        absPath = os.getcwd()
        a = pathlib2.Path(absPath + "/" + "maparea.html").as_uri()
        usedBackend = wx.html2.WebViewBackendIE
        wx.html2.WebView.MSWSetEmulationLevel(wx.html2.WEBVIEWIE_EMU_IE11)
        self.browser = wx.html2.WebView.New(self, backend=usedBackend)
        self.browser.LoadURL(a)

        self.toolbar1 = self.CreateToolBar()
        tLoad = self.toolbar1.AddTool(wx.ID_ANY, 'Load', wx.Bitmap('ico/download.png'))
        tSettings = self.toolbar1.AddTool(wx.ID_ANY, 'Settings', wx.Bitmap('ico/settings.png'))
        tQuit = self.toolbar1.AddTool(wx.ID_ANY, 'Quit', wx.Bitmap('ico/cancel.png'))
        self.toolbar1.Realize()
        vbox.Add(self.toolbar1, 0, wx.EXPAND)
        self.Bind(wx.EVT_TOOL, self.quit, tQuit)
        self.Bind(wx.EVT_TOOL, self.gpxLoad, tLoad)

        datesListTemp = self.getUserTracksDates()
        dateList = []
        for index in range(len(datesListTemp)):
            for key in datesListTemp[index]:
                print(datesListTemp[index][key])
                dateList.append(datesListTemp[index][key].strftime("%m/%d/%Y, %H:%M:%S"))

        tracksList = self.getUserTracks()
        # print(tracksList)

        self.lst = wx.ListBox(self, size=(150, -1), choices=dateList, style=wx.LB_SINGLE)
        hbox.Add(self.lst, 0, wx.ALIGN_LEFT | wx.EXPAND, 10)
        hbox.Add(self.browser, 1, wx.EXPAND, 10)
        self.lst.Bind(wx.EVT_LISTBOX, self.getUserTracks)

        # self.SetSizer(vbox)
        self.SetSizer(hbox)
        self.SetTitle('GPX')
        self.Center()
        self.SetSize((1280, 720))


    def quit(self, e):
        # self.Close()
        self.Destroy()


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

    def getUserTracksDates(self):
        return sqlAlch.getTrackDates(MyBrowser.loggedUser)

    def getUserTracks(self):
        print('event!')

        return sqlAlch.getTracks(MyBrowser.loggedUser)


def main():
    app = wx.App(False)
    dialog = MyBrowser(None)
    dialog.Show()
    app.MainLoop()





