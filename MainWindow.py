import wx
import LoginDialog
import gpxParse
import sqlAlch
import wx.html2
import wx.html
import pathlib2
import os
from datetime import datetime
import sys
import MapMaker as map

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
        self.Bind(wx.EVT_CLOSE, self.quit)

        datesListTemp = self.getUserTracksDates()
        dateList = []
        for index in range(len(datesListTemp)):
            for key in datesListTemp[index]:
                dateList.append(datesListTemp[index][key].strftime("%Y-%m-%d %H:%M:%S"))

        # tracksList = self.getUserTracks()

        self.lst = wx.ListBox(self, size=(150, -1), choices=dateList, style=wx.LB_SINGLE)
        hbox.Add(self.lst, 0, wx.ALIGN_LEFT | wx.EXPAND, 10)
        hbox.Add(self.browser, 1, wx.EXPAND, 10)
        self.lst.Bind(wx.EVT_LISTBOX, self.getUserPoints, self.lst)
        # self.SetSizer(vbox)
        self.SetSizer(hbox)
        self.SetTitle('GPX')
        self.Center()
        self.SetSize((1280, 720))


    def quit(self, e):
        # self.Close()
        self.Destroy()
        sys.exit(0)


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
            self.updateUserTracksDates()
        except Exception as e:
            wx.MessageBox("File not added!", "Message", wx.OK | wx.ICON_ERROR)
            print(e)
            pass

    def getUserTracksDates(self):
        return sqlAlch.getTrackDates(MyBrowser.loggedUser)

    def updateUserTracksDates(self):
        datesListTemp = self.getUserTracksDates()
        dateList = []
        for index in range(len(datesListTemp)):
            for key in datesListTemp[index]:
                dateList.append(datesListTemp[index][key].strftime("%Y-%m-%d %H:%M:%S"))
        self.lst.Clear()
        self.lst.AppendItems(dateList)


    def getUserTracks(self):
        return sqlAlch.getTracks(MyBrowser.loggedUser)

    def getSelectedTrack(self, trackDate):
        return sqlAlch.getSelectedTrack(MyBrowser.loggedUser, trackDate)

    def getUserPoints(self, event):
        print("event")
        positionSelected = self.lst.GetStringSelection()
        a_object = datetime.strptime(positionSelected, '%Y-%m-%d %H:%M:%S')

        gpxPointsListTemp = self.getSelectedTrack(a_object)
        gpxPointsList = []
        for index in range(len(gpxPointsListTemp)):
            for key in gpxPointsListTemp[index]:
                gpxPointsList.append(gpxPointsListTemp[index][key])
        print(len(gpxPointsList[7]))
        xtemp = gpxPointsList[7]
        xtemp = xtemp.translate({ord('['): None}).translate({ord(']'): None})
        splittedList= xtemp.split(",")
        latPointsList = []
        lonPointsList = []
        for i in range(0, len(splittedList)):
            if i % 2:
                lonPointsList.append(splittedList[i])
            else:
                latPointsList.append(splittedList[i])
        print(latPointsList)
        print(lonPointsList)
        formPointsList = []
        formPointsList = [(latPointsList[i], lonPointsList[i]) for i in range(0, len(latPointsList))]
        print(formPointsList[3])
        map.updateMap(formPointsList)
        absPath = os.getcwd()
        self.browser.LoadURL(pathlib2.Path(absPath + "/" + "maparea.html").as_uri())

def main():
    app = wx.App(False)
    dialog = MyBrowser(None)
    dialog.Show()
    app.MainLoop()





