import wx_window.main_window
import wx


wx_app = wx.App()
main_window = wx_window.main_window.WxMainWindow(None)
data_model = main_window.get_model()

wx_app.MainLoop()