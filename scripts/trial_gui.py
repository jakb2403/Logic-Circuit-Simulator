import wx
from wx.core import BoxSizer
import wx.lib.agw.aui as aui


class FloatingPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.sizer = BoxSizer(wx.VERTICAL)

        self.text2 = wx.TextCtrl(self, wx.ID_ANY, 'Text 2 - side dock')

        self.sizer.Add(self.text2, 1, wx.EXPAND, 0)
        self.SetSizer(self.sizer)


class TrailGui(wx.Frame):

    def __init__(self):

        super().__init__(parent=None, size=(800, 600))

        # create AuiManager
        self.mgr = aui.AuiManager()

        # notify AUI which frame to use
        self.mgr.SetManagedWindow(self)

        self.text1 = wx.TextCtrl(
            self, wx.ID_ANY, 'Text 1 - this part is like the main centre bit')

        # self.floating_panel = wx.Panel(self)
        # self.floating_panel_sizer = wx.BoxSizer(wx.VERTICAL)

        # self.text2 = wx.TextCtrl(self.floating_panel, wx.ID_ANY, 'Text 2 - side dock')

        # self.floating_panel_sizer.Add(self.text2, 1, wx.EXPAND, 0)
        # self.floating_panel.SetSizer(self.floating_panel_sizer)

        self.floating_panel = FloatingPanel(self)

        self.mgr.AddPane(self.text1, aui.AuiPaneInfo().CenterPane())
        self.mgr.AddPane(self.floating_panel,
                         aui.AuiPaneInfo().Left().Floatable(False))

        # set docking guiges (THIS FIXES THE FLOATING POINT PROBLEM)
        agwFlags = self.mgr.GetAGWFlags()
        self.mgr.SetAGWFlags(agwFlags | aui.AUI_MGR_AERO_DOCKING_GUIDES)

        self.mgr.Update()

        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Centre()
        self.Show(True)

    def on_close(self, event):
        # deinitialise the frame manager
        self.mgr.UnInit()
        self.Destroy()


app = wx.App()
frame = TrailGui()
frame.Show()
app.MainLoop()
