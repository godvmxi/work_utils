import wx
class App(wx.App):
    def OnInit(self):
        frame = wx.Frame(parent=None, title='no')
        text = wx.TextCtrl(frame,titile="临时卡用户"，
        content="临时卡用户\n时长：2小时\n费用：10")
        frame.Show()
        return True
app = App()
app.MainLoop()