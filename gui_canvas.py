import wx
from gui_gl_canvas import MyGLCanvas


class CanvasPanel(wx.Panel):
    def __init__(self, parent, devices, monitors):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.sizer = wx.FlexGridSizer(rows=2, cols=2, vgap=0, hgap=0)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
        self.canvas = MyGLCanvas(self, devices, monitors)

        # Configure the scrollbars for the canvas main panel
        self.vert_scroll = wx.ScrollBar(self, style=wx.SB_VERTICAL)
        self.horiz_scroll = wx.ScrollBar(self, style=wx.SB_HORIZONTAL)


        self.sizer.Add(self.canvas, 1, wx.EXPAND, 0)
        self.sizer.Add(self.vert_scroll, 1, wx.EXPAND, 0)
        self.sizer.Add(self.horiz_scroll, 0, wx.EXPAND, 0)


        self.SetSizer(self.sizer)
