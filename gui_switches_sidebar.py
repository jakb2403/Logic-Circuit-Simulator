import wx

class SwitchesSidebarPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.YELLOW)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.switches_dict = {
            "SW1": 0,
            "SW2": 1,
            "SW3": 0,
            "SW4": 1,
            "SW5": 0,
        }

        # Create widgets
        test_text = wx.StaticText(self, wx.ID_ANY, "This is a test")

        self.sizer.Add(test_text, 0, wx.ALL, 0)

        self.SetSizer(self.sizer)


    # def create_switch(name, init_state):
    #     text = wx.StaticText(wx.ID_ANY, name)
    #     toggle = wx.ToggleButton(wx.)