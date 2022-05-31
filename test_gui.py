import wx

class Panel_root(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.panel_1 = Panel_1(self)
        self.panel_2 = Panel_2(self)
        self.panel_3 = Panel_3(self)

        s = wx.BoxSizer(wx.VERTICAL)
        s.Add(self.panel_2, 1, wx.EXPAND)
        s.Add(self.panel_3, 1, wx.EXPAND)

        root_sizer = wx.BoxSizer(wx.HORIZONTAL)
        root_sizer.Add(self.panel_1, 1, wx.EXPAND)
        root_sizer.Add(s, 3, wx.EXPAND)
        self.SetSizer(root_sizer)

        self.Bind(wx.EVT_BUTTON, self.onclic)

    def onclic(self, e):
        origin = e.GetEventObject().GetName()
        if origin == 'first button':
            self.panel_2.update('hello') # note that we use an API...
        elif origin == 'second button':
            self.panel_3.update('hello') # ...to avoid direct access

class Panel_1(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.RED)
        b1 = wx.Button(self, -1, 'first', pos=(10, 10), name='first button')
        b2 = wx.Button(self, -1, 'second', pos=(10, 50), name='second button')

class Panel_2(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.YELLOW)
        self.text = wx.TextCtrl(self, pos=(10, 10))

    def update(self, value): # we provide a public API to update this panel
        self.text.SetValue(value)

class Panel_3(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.GREEN)
        self.text = wx.TextCtrl(self, pos=(10, 10))

    def update(self, value):
        self.text.SetValue(value)

class MainFrame(wx.Frame):
    def __init__(self, *a, **k):
        wx.Frame.__init__(self, *a, **k)
        Panel_root(self)


app = wx.App()
frame = MainFrame()
frame.Show()
app.MainLoop()

