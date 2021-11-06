import wx
import sqlAlch
import RegisterFrame


class LoginDialog(wx.Dialog):

    def __init__(self):
        wx.Dialog.__init__(self, None, title="Login")
        self.logged = False
        self.username = None
        user_sizer = wx.BoxSizer(wx.HORIZONTAL)
        user = wx.StaticText(self, label="User")
        user_sizer.Add(user, 0, wx.ALL | wx.CENTER, 5)
        self.user = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.user.Bind(wx.EVT_TEXT_ENTER, self.onLogin)
        user_sizer.Add(self.user, 0, wx.ALL)

        pass_sizer = wx.BoxSizer(wx.HORIZONTAL)

        pass_lbl = wx.StaticText(self, label="Password:")
        pass_sizer.Add(pass_lbl, 0, wx.ALL | wx.CENTER, 5)
        self.password = wx.TextCtrl(self, style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        self.password.Bind(wx.EVT_TEXT_ENTER, self.onLogin)
        pass_sizer.Add(self.password, 0, wx.ALL, 5)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(user_sizer, 0, wx.ALL, 5)
        main_sizer.Add(pass_sizer, 0, wx.ALL, 5)

        btnLogin = wx.Button(self, label="Login")
        btnLogin.Bind(wx.EVT_BUTTON, self.onLogin)
        main_sizer.Add(btnLogin, 0, wx.ALL | wx.LEFT, 5)

        btnRegister = wx.Button(self, label="Register")
        btnRegister.Bind(wx.EVT_BUTTON, self.onRegister)
        main_sizer.Add(btnRegister, 0, wx.ALL | wx.RIGHT, 5)

        self.SetSizer(main_sizer)

    def onLogin(self, event):
        user_password = self.password.GetValue()
        user_name = self.user.GetValue()

        if sqlAlch.checkUser(user_name, user_password):
            self.logged_in = True
            self.username = user_name
            self.Close()

        else:
            wx.MessageBox("Wrong username or password", "Message", wx.OK | wx.ICON_ERROR)

    def onRegister(self, event):
        regDialog = RegisterFrame.RegisterFrame()
        regDialog.ShowModal()

