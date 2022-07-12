import wx
import sqlAlch
import RegisterFrame


class LoginDialog(wx.Dialog):

    def __init__(self):
        wx.Dialog.__init__(self, None, id=wx.ID_ANY, title="GPX", pos=wx.DefaultPosition,
                           size=wx.Size(279, 284), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.login = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.login, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"Login", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer1.Add(self.m_staticText1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.password = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PASSWORD )
        bSizer1.Add(self.password, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"Password", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        bSizer1.Add(self.m_staticText2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        gSizer1 = wx.GridSizer(0, 2, 0, 0)

        self.btnLogin = wx.Button(self, wx.ID_ANY, u"Login", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.btnLogin, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.btnRegister = wx.Button(self, wx.ID_ANY, u"Register", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.btnRegister, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer1.Add(gSizer1, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.btnLogin.Bind(wx.EVT_BUTTON, self.onLogin)
        self.btnRegister.Bind(wx.EVT_BUTTON, self.onRegister)

    def __del__(self):
        pass

    def onLogin(self, event):
        user_password = self.password.GetValue()
        user_name = self.login.GetValue()

        if sqlAlch.checkUser(user_name, user_password):
            self.logged_in = True
            self.username = user_name
            LoginDialog.loggedUser = self.username
            self.Close()

        else:
            wx.MessageBox("Wrong username or password", "Message", wx.OK | wx.ICON_ERROR)

    def onRegister(self, event):
        regDialog = RegisterFrame.RegisterFrame()
        regDialog.ShowModal()
