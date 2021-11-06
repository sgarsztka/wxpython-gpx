import wx
import sqlAlch


class RegisterFrame(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, title="Register new user")
        user_sizer = wx.BoxSizer(wx.HORIZONTAL)
        user = wx.StaticText(self, label="User")
        user_sizer.Add(user, 0, wx.ALL | wx.CENTER, 5)
        self.user = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.user.Bind(wx.EVT_TEXT_ENTER, self.onRegister)
        user_sizer.Add(self.user, 0, wx.ALL)

        pass_sizer = wx.BoxSizer(wx.HORIZONTAL)

        pass_lbl = wx.StaticText(self, label="Password:")
        pass_sizer.Add(pass_lbl, 0, wx.ALL | wx.CENTER, 5)
        self.password = wx.TextCtrl(self, style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        self.password.Bind(wx.EVT_TEXT_ENTER, self.onRegister)
        pass_sizer.Add(self.password, 0, wx.ALL, 5)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(user_sizer, 0, wx.ALL, 5)
        main_sizer.Add(pass_sizer, 0, wx.ALL, 5)

        btnRegister = wx.Button(self, label="Create User")
        btnRegister.Bind(wx.EVT_BUTTON, self.onRegister)
        main_sizer.Add(btnRegister, 0, wx.ALL | wx.CENTER, 5)

        self.SetSizer(main_sizer)

    def onRegister(self, event):
        user_password = self.password.GetValue()
        user_name = self.user.GetValue()
        sqlAlch.insertUser(user_name, user_password)
        if sqlAlch.checkUser(user_name, user_password):
            wx.MessageBox("User created!", "Message", wx.OK | wx.ICON_INFORMATION)
            self.Close()

        else:
            wx.MessageBox("User not created properly", "Message", wx.OK | wx.ICON_ERROR)

