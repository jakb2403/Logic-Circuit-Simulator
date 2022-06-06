import wx


class SwitchesSidebarPanel(wx.Panel):
    def __init__(self, parent, names, devices, network,
                 monitors, push_status, input_cmd):
        wx.Panel.__init__(self, parent)
        # self.SetBackgroundColour(wx.YELLOW)

        self.parent = parent
        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors
        self.push_status = push_status
        self.input_cmd = input_cmd

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.switches_dict = {
            1: ["SW1", 0],
            2: ["SW2", 1],
            3: ["SW3", 0],
            4: ["SW4", 1],
            5: ["SW5", 0],
        }

        # self.switches_dict = {}
        # self.switch_device_ids = self.devices.find_devices(devices.SWITCH)
        # for id in self.switch_device_ids:
        #     state = self.devices.get_device().switch_state
        #     name = self.devices.get_signal_name(id, None)
        #     self.switches_dict[id] = [name, state]

        # Create widgets
        for switch in self.switches_dict:
            device_id = switch
            name = self.switches_dict[switch][0]
            init_state = self.switches_dict[switch][1]
            self.create_switch(name, device_id, init_state)

        self.SetSizer(self.sizer)

    def create_switch(self, name, device_id, init_state):
        text = wx.StaticText(self, wx.ID_ANY, name)
        toggle = wx.ToggleButton(self, device_id, label=str(init_state))
        if init_state == 1:
            toggle.SetValue(True)
        switch_sizer = wx.BoxSizer(wx.HORIZONTAL)
        switch_sizer.Add(text, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        switch_sizer.Add(toggle, 1, wx.EXPAND | wx.ALL, 1)
        toggle.Bind(wx.EVT_TOGGLEBUTTON, self.on_toggle_switch)
        self.sizer.Add(switch_sizer, 0, wx.EXPAND, 0)

    def on_toggle_switch(self, event):
        toggle = event.GetEventObject()
        id = toggle.GetId()
        switch_name = self.switches_dict[id][0]
        current_state = int(toggle.GetLabel())
        if current_state == 1:
            new_state = 0
        elif current_state == 0:
            new_state = 1

        toggle.SetLabel(str(new_state))

        command = f"s {switch_name} {new_state}"
        self.input_cmd(command)

        text = f"Switch {switch_name} toggled to {new_state}"
        self.push_status(text)
