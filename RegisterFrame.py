import wx
import sqlAlch


class RegisterFrame(wx.Dialog):

    def __init__(self):
        wx.Dialog.__init__(self, None, id=wx.ID_ANY, title=u"Register new user", pos=wx.DefaultPosition,
                           size=wx.Size(363, 313), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        gSizer2 = wx.GridSizer(3, 2, 0, 0)

        self. userText= wx.StaticText(self, wx.ID_ANY, u"Username", wx.DefaultPosition, wx.DefaultSize, 0)
        self.userText.Wrap(-1)
        gSizer2.Add(self.userText, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.username = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.username, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.passText = wx.StaticText(self, wx.ID_ANY, u"Password", wx.DefaultPosition, wx.DefaultSize, 0)
        self.passText.Wrap(-1)
        gSizer2.Add(self.passText, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.password = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD)
        gSizer2.Add(self.password, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.repPassText = wx.StaticText(self, wx.ID_ANY, u"Repeat password", wx.DefaultPosition, wx.DefaultSize, 0)
        self.repPassText.Wrap(-1)
        gSizer2.Add(self.repPassText, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.repeat = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD)
        gSizer2.Add(self.repeat, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer4.Add(gSizer2, 1, wx.EXPAND, 5)

        gSizer6 = wx.GridSizer(0, 2, 0, 0)

        self.btnRegister = wx.Button(self, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.DefaultSize, 0)
        self.btnRegister.Enable(False)

        gSizer6.Add(self.btnRegister, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.btnCancel = wx.Button(self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer6.Add(self.btnCancel, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer4.Add(gSizer6, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer4)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.btnRegister.Bind(wx.EVT_BUTTON, self.onRegister)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.onCancel)
        self.repeat.Bind(wx.EVT_TEXT, self.onRepeatValidator)
        self.password.Bind(wx.EVT_TEXT, self.onRepeatValidator)

    def __del__(self):
        pass

    def onRepeatValidator(self, event):
        self.btnRegister.Enable(False)
        user_password = self.password.GetValue()
        user_password_repeat = self.repeat.GetValue()
        if len(user_password) == len(user_password_repeat):
            if user_password == user_password_repeat:
                self.btnRegister.Enable(True)

    def onRegister(self, event):
        user_password = self.password.GetValue()
        user_name = self.username.GetValue()
        if not sqlAlch.checkCreatedUser(user_name):
            sqlAlch.insertUser(user_name, user_password)
            if sqlAlch.checkUser(user_name, user_password):
                wx.MessageBox("User created!", "Message", wx.OK | wx.ICON_INFORMATION)
                self.Close()

            else:
                wx.MessageBox("User not created properly", "Message", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("User already exists", "Message", wx.OK | wx.ICON_ERROR)
    def onCancel(self, event):
        self.Close()

