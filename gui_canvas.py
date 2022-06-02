import wx
from gui_gl_canvas import MyGLCanvas


class CanvasPanel(wx.Panel):
    def __init__(self, parent, names, devices, network, monitors, push_status):
        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors
        self.push_status = push_status
        
        self.sizer = wx.FlexGridSizer(rows=2, cols=2, vgap=0, hgap=0)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
        self.canvas = MyGLCanvas(self, devices, monitors, self.push_status)

        # Configure the scrollbars for the canvas main panel
        self.vert_scroll = wx.ScrollBar(self, style=wx.SB_VERTICAL)
        self.horiz_scroll = wx.ScrollBar(self, style=wx.SB_HORIZONTAL)

        self.sizer.Add(self.canvas, 1, wx.EXPAND, 0)
        self.sizer.Add(self.vert_scroll, 1, wx.EXPAND, 0)
        self.sizer.Add(self.horiz_scroll, 0, wx.EXPAND, 0)

        self.vert_scroll.Bind(wx.EVT_COMBOBOX, self.on_vert_scroll)
        self.vert_scroll.Bind(wx.EVT_COMBOBOX, self.on_horiz_scroll)

        self.SetSizer(self.sizer)

    def on_vert_scroll(self, event):
        pass

    def on_horiz_scroll(self, event):
        pass
