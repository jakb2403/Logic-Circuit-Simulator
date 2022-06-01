import wx

class SwitchesSidebarPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # self.SetBackgroundColour(wx.YELLOW)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.parent = parent

        self.switches_dict = {
            "SW1": [0, 1],
            "SW2": [1, 2],
            "SW3": [0, 3],
            "SW4": [1, 4],
            "SW5": [0, 5],
        }

        # Create widgets
        for switch in self.switches_dict:

            name = switch
            init_state = self.switches_dict[switch][0]
            device_id = self.switches_dict[switch][1]
            self.create_switch(name, device_id, init_state)

        self.SetSizer(self.sizer)


    def create_switch(self, name, device_id, init_state):
        text = wx.StaticText(self, device_id, name)
        toggle = wx.ToggleButton(self, wx.ID_ANY, label=str(init_state))
        if init_state == 1:
            toggle.SetValue(True)
        switch_sizer = wx.BoxSizer(wx.HORIZONTAL)
        switch_sizer.Add(text, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        switch_sizer.Add(toggle, 1, wx.EXPAND | wx.ALL, 0)
        toggle.Bind(wx.EVT_TOGGLEBUTTON, self.on_toggle_switch)
        self.sizer.Add(switch_sizer, 0, wx.EXPAND, 0)


    def on_toggle_switch(self, event):
        toggle = event.GetEventObject()
        if toggle.GetLabel() == "1":
            toggle.SetLabel("0")
        elif toggle.GetLabel() == "0":
            toggle.SetLabel("1")
        
        