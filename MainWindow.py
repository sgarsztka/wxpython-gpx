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
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import matplotlib.pyplot as plt




class MatplotPanel(wx.Panel):
    def __init__(self, parent):
        plt.rcParams["figure.figsize"] = [3, 2]
        plt.rcParams["figure.autolayout"] = True
        plt.rcParams["ytick.labelright"]= False
        plt.rcParams["ytick.labelleft"] = False
        plt.rcParams["ytick.left"] = False

        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.axes.get_xaxis().set_visible(False)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

    def draw(self,x,y):
        self.figure.clear()
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.axes.get_xaxis().set_visible(False)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()
        self.axes.plot(x, y)

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
        self.elevationPanel = MatplotPanel(self)
        self.hrPanel = MatplotPanel(self)

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
        self.box = wx.StaticBox( self, wx.ID_ANY, "GPX Track Data", size=(200, -1))
        self.SetBackgroundColour(wx.WHITE)
        self.trackData = wx.StaticBoxSizer(self.box, wx.VERTICAL )
        self.dateSizer = wx.BoxSizer( wx.HORIZONTAL)
        self.dateLabel = wx.StaticText(self, -1, "Date:")
        self.dateSpacer = wx.StaticText(self, -1, "    ")
        self.dateLabel2 = wx.StaticText(self, -1, "")
        self.dateSizer.Add(self.dateLabel)
        self.dateSizer.Add(self.dateSpacer)
        self.dateSizer.Add(self.dateLabel2)

        self.avgSpeedSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.avgSpeedLabel1 = wx.StaticText(self, -1, "AVG Speed:")
        self.avgSpeedSpacer = wx.StaticText(self, -1, "    ")
        self.avgSpeedLabel2 = wx.StaticText(self, -1, "")
        self.avgSpeedSizer.Add(self.avgSpeedLabel1)
        self.avgSpeedSizer.Add(self.avgSpeedSpacer)
        self.avgSpeedSizer.Add(self.avgSpeedLabel2)

        self.distanceSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.distanceLabel1 = wx.StaticText(self, -1, "Distance:")
        self.distanceSpacer = wx.StaticText(self, -1, "    ")
        self.distanceLabel2 = wx.StaticText(self, -1, "")
        self.distanceSizer.Add(self.distanceLabel1)
        self.distanceSizer.Add(self.distanceSpacer)
        self.distanceSizer.Add(self.distanceLabel2)

        self.hrSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hrLabel1 = wx.StaticText(self, -1, "AVG Heartrate:")
        self.hrSpacer = wx.StaticText(self, -1, "    ")
        self.hrLabel2 = wx.StaticText(self, -1, "")
        self.hrSizer.Add(self.hrLabel1)
        self.hrSizer.Add(self.hrSpacer)
        self.hrSizer.Add(self.hrLabel2)

        self.rideTimeSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.rideTimeLabel1 = wx.StaticText(self, -1, "Ride time:")
        self.rideTimeSpacer = wx.StaticText(self, -1, "    ")
        self.rideTimeLabel2 = wx.StaticText(self, -1, "")
        self.rideTimeSizer.Add(self.rideTimeLabel1)
        self.rideTimeSizer.Add(self.rideTimeSpacer)
        self.rideTimeSizer.Add(self.rideTimeLabel2)

        self.pointsNumberSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.pointsNumberLabel1 = wx.StaticText(self, -1, "Number of points:")
        self.pointsNumberSpacer = wx.StaticText(self, -1, "    ")
        self.pointsNumberLabel2 = wx.StaticText(self, -1, "")
        self.pointsNumberSizer.Add(self.pointsNumberLabel1)
        self.pointsNumberSizer.Add(self.pointsNumberSpacer)
        self.pointsNumberSizer.Add(self.pointsNumberLabel2)

        hbox.Add(self.lst, 0, wx.ALIGN_LEFT | wx.EXPAND, 10)
        hbox.Add(self.browser, 1, wx.EXPAND, 10)
        hbox.Add(self.trackData, 0, wx.EXPAND, 10)



        self.trackData.Add(self.dateSizer, 0 ,wx.EXPAND, 10)
        self.trackData.Add(self.avgSpeedSizer, 0 ,wx.EXPAND, 10)
        self.trackData.Add(self.distanceSizer, 0, wx.EXPAND, 10)
        self.trackData.Add(self.hrSizer, 0, wx.EXPAND, 10)
        self.trackData.Add(self.rideTimeSizer, 0, wx.EXPAND, 10)
        self.trackData.Add(self.pointsNumberSizer, 0, wx.EXPAND, 10)
        self.trackData.Add(self.elevationPanel, 0, wx.EXPAND, 10)
        self.trackData.Add(self.hrPanel, 0, wx.EXPAND, 10)
        self.lst.Bind(wx.EVT_LISTBOX, self.getUserPoints, self.lst)
        self.lst.Bind(wx.EVT_RIGHT_DOWN, self.rightClickMenu, self.lst)

        self.SetSizer(vbox)
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

        formPointsList = [(latPointsList[i], lonPointsList[i]) for i in range(0, len(latPointsList))]
        map.updateMap(formPointsList)
        absPath = os.getcwd()
        self.browser.LoadURL(pathlib2.Path(absPath + "/" + "maparea.html").as_uri())
        self.dateLabel2.SetLabel(positionSelected)
        self.avgSpeedLabel2.SetLabel(str(gpxPointsList[2])[:5])
        self.distanceLabel2.SetLabel(str(gpxPointsList[3])[:6])
        self.hrLabel2.SetLabel(str(gpxPointsList[4])[:5])
        self.rideTimeLabel2.SetLabel(str(gpxPointsList[6]))
        self.pointsNumberLabel2.SetLabel(str(len(gpxPointsList[7])))
        elevationTempList = gpxPointsList[9].replace("[","")
        elevationList = list(elevationTempList.split(","))
        elevationListSize = []
        for i in range(0, (len(elevationList))):
            elevationListSize.append(i)

        hrTempList = gpxPointsList[8].replace("[", "")
        hrTempList.replace("0.0","")
        hrList = list(hrTempList.split(","))
        hrListSize = []
        for i in range(0, (len(hrList))):
            hrListSize.append(i)

        self.elevationPanel.draw(elevationListSize,elevationList)
        self.hrPanel.draw(hrListSize,hrList)
        trackId = gpxPointsList[0]
        return trackId

    def rightClickMenu(self, event):
        self.popupID1 = wx.NewId()
        self.Bind(wx.EVT_MENU, self.onPopup, id=self.popupID1)
        menu = wx.Menu()
        menu.Append(self.popupID1, "Delete")
        self.PopupMenu(menu)

    def onPopup(self, event):
        trkId = self.getUserPoints(event)
        sqlAlch.deleteSelectedTrack(trkId)
        self.updateUserTracksDates()


def main():
    app = wx.App(False)
    dialog = MyBrowser(None)
    dialog.Show()
    app.MainLoop()





