import wx

class MonitorSidebarPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # self.SetBackgroundColour(wx.RED)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.devices_list = ["G1", "G2", "G3", "G4"]
        self.device_types_list = ["All", "AND", "NAND",
                                  "OR", "NOR", "XOR", "SWITCH", "CLOCK", "DTYPE"]
        self.available_devices = self.devices_list

        # Create widgets
        device_type = wx.StaticText(self, wx.ID_ANY, "Device type")
        mon_add_dropdown = wx.ComboBox(
            self, choices=self.device_types_list, style=wx.CB_READONLY)
        monitor_checklist = wx.CheckListBox(
            self, choices=self.available_devices, name="Monitor Signals")

        self.sizer.Add(device_type, 0, wx.ALL, 0)
        self.sizer.Add(mon_add_dropdown, 0,
                       wx.EXPAND | wx.LEFT | wx.RIGHT, 0)
        self.sizer.Add(monitor_checklist, 1,
                       wx.EXPAND | wx.LEFT | wx.RIGHT, 0)

        # Bind events to event handlers
        mon_add_dropdown.Bind(wx.EVT_COMBOBOX, self.on_dropdown)

        self.SetSizer(self.sizer)

    def on_dropdown(self, event):
        """Handle the event when the user clicks the dropdown menu to add a
        monitor signal"""
        self.device_to_add = self.mon_add_dropdown.GetValue()
        text = "".join(["Signal type to display: ", self.signal_to_add])
