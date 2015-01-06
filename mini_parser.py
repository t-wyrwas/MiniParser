import wx_panel
import wx


wx_app = wx.App()
main_window = wx_panel.WxPanel(None)
data_model = main_window.get_model()

wx_app.MainLoop()