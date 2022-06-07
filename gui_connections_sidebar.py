import wx
from wx.core import Command, SingleChoiceDialog


class ConnectionsSidebarPanel(wx.Panel):
    def __init__(
        self, parent, names, devices, network, monitors, push_status, input_cmd
    ):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.WHITE)

        self.parent = parent
        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors
        self.push_status = push_status
        self.input_cmd = input_cmd

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.all_devices = []

        # Create widgets
        info_text1 = wx.StaticText(
            self, wx.ID_ANY, "Choose a connection to replace:"
        )
        info_text2 = wx.StaticText(self, wx.ID_ANY, "Replace ...")
        self.dropdown_find = wx.Choice(
            self,
            wx.CB_DROPDOWN | wx.CB_READONLY,
            choices=["1", "2"],
            name="find",
        )
        info_text3 = wx.StaticText(self, wx.ID_ANY, "with ...")
        self.dropdown_replace = wx.Choice(
            self,
            wx.CB_DROPDOWN | wx.CB_READONLY,
            choices=["1", "2"],
            name="replace",
        )
        self.replace_button = wx.Button(self, wx.ID_ANY, "Replace")

        self.sizer.Add(info_text1, 0, wx.ALL, 3)
        self.sizer.Add(info_text2, 0, wx.ALL, 3)
        self.sizer.Add(self.dropdown_find, 0, wx.ALL | wx.EXPAND, 3)
        self.sizer.Add(info_text3, 0, wx.ALL, 3)
        self.sizer.Add(self.dropdown_replace, 0, wx.ALL | wx.EXPAND, 3)
        self.sizer.Add(self.replace_button, 0, wx.ALL | wx.EXPAND, 3)

        # Bind events to event handlers
        # self.monitor_checklist.Bind(wx.EVT_CHECKLISTBOX, self.on_check)

        self.SetSizer(self.sizer)

    def on_dropdown_find(self, event):
        """Handle the event when the user uses the first (find) dropdown"""
        pass

    def on_dropdown_replace(self, event):
        """Handle the event when the user uses the second (replace) dropdown"""
        pass
