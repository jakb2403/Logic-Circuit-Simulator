import wx

class SwitchesSidebarPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # self.SetBackgroundColour(wx.YELLOW)
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

        for switch in self.switches_dict:
            # name = switch
            # init_state = self.switches_dict[switch]
            # text, toggle = self.create_switch(name, init_state)
            # self.sizer.Add(text, 0, wx.ALL, 0)
            # self.sizer.Add(toggle, 0, wx.ALL, 0)

            name = switch
            init_state = self.switches_dict[switch]
            switch_sizer = self.create_switch(name, init_state)
            self.sizer.Add(switch_sizer, 0, wx.EXPAND, 0)

        self.SetSizer(self.sizer)


    def create_switch(self, name, init_state):
        horiz_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self, wx.ID_ANY, name)
        toggle = wx.ToggleButton(self, wx.ID_ANY, label=str(init_state))
        if init_state == 1:
            toggle.SetValue(True)
        horiz_sizer.Add(text, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        horiz_sizer.Add(toggle, 1, wx.EXPAND | wx.ALL, 0)

        return horiz_sizer

    # def on_click_switch(self):
