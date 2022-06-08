import wx
import wx.lib.scrolledpanel


class SwitchesSidebarPanel(wx.Panel):
    def __init__(
        self, parent, names, devices, network, monitors, push_status, input_cmd
    ):
        wx.Panel.__init__(self, parent)
        # self.SetBackgroundColour(wx.WHITE)

        self.parent = parent
        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors
        self.push_status = push_status
        self.input_cmd = input_cmd

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.scroll_sizer = wx.BoxSizer(wx.VERTICAL)

        info_text = wx.StaticText(
            self, wx.ID_ANY, _("Change state of switches:")
        )

        self.scroll_panel = wx.lib.scrolledpanel.ScrolledPanel(
            self, -1  # , style=wx.SIMPLE_BORDER
        )
        self.scroll_panel.SetupScrolling()
        self.scroll_panel.SetSizer(self.scroll_sizer)

        self.sizer.Add(info_text, 0, wx.ALL, 3)
        self.sizer.Add(self.scroll_panel, 1, wx.ALL | wx.EXPAND, 0)

        self.SetSizer(self.sizer)

    def update_list(self):
        self.switches_list = self.devices.find_devices(self.devices.SWITCH)
        for i in range(len(self.switches_list)):
            device_id = self.switches_list[i]
            name = self.devices.get_signal_name(device_id, None)
            init_state = self.devices.get_device(device_id).switch_state
            self.create_switch(name, device_id, init_state)
        self.SetSizer(self.sizer)

    def create_switch(self, name, device_id, init_state):
        text = wx.StaticText(self.scroll_panel, wx.ID_ANY, name)
        toggle = wx.ToggleButton(
            self.scroll_panel, device_id, label=str(init_state)
        )
        if init_state == 1:
            toggle.SetValue(True)
        switch_sizer = wx.BoxSizer(wx.HORIZONTAL)
        switch_sizer.Add(text, 1, wx.ALIGN_CENTER | wx.ALL, 1)
        switch_sizer.Add(toggle, 1, wx.EXPAND | wx.ALL, 1)
        toggle.Bind(wx.EVT_TOGGLEBUTTON, self.on_toggle_switch)
        self.scroll_sizer.Add(switch_sizer, 0, wx.ALL | wx.EXPAND, 0)

    def on_toggle_switch(self, event):
        toggle = event.GetEventObject()
        id = toggle.GetId()
        switch_name = self.devices.get_signal_name(id, None)
        current_state = int(toggle.GetLabel())
        if current_state == 1:
            new_state = 0
        elif current_state == 0:
            new_state = 1

        toggle.SetLabel(str(new_state))

        command = "s {} {}".format(switch_name, new_state)
        self.input_cmd(command)

        text = _("Switch {} toggled to {}").format(switch_name, new_state)
        self.push_status(text)
