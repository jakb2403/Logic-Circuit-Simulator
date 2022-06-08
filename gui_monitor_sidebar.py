import wx
from wx.core import Command, SingleChoiceDialog


class MonitorSidebarPanel(wx.Panel):
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

        self.all_devices = []

        # Create widgets
        info_text = wx.StaticText(
            self, wx.ID_ANY, _("Choose devices to monitor:")
        )
        self.monitor_checklist = wx.CheckListBox(
            self, choices=self.all_devices, name=_("Monitor Signals")
        )

        self.sizer.Add(info_text, 0, wx.ALL, 3)
        self.sizer.Add(
            self.monitor_checklist, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 0
        )

        # Bind events to event handlers
        self.monitor_checklist.Bind(wx.EVT_CHECKLISTBOX, self.on_check)

        self.SetSizer(self.sizer)

    def update_checklist(self):

        [self.monitored, self.not_monitored] = self.monitors.get_signal_names()
        self.all_devices = [*self.monitored, *self.not_monitored]

        self.monitor_checklist.Clear()
        for item in self.all_devices:
            self.monitor_checklist.Append(item)

        monitors_index = range(len(self.monitored))
        self.monitor_checklist.SetCheckedItems(monitors_index)

    def on_check(self, event):
        """Handle the event when the user clicks one of the checkbox items"""
        changed = wx.CommandEvent.GetInt(event)
        new_state = self.monitor_checklist.IsChecked(changed)

        device_name = self.all_devices[changed]

        if new_state == True:  # adding a monitor point
            command = "m {}".format(device_name)
            self.input_cmd(command)
            text = _("Device {} added to monitor points").format(device_name)

        else:  # zapping a monitor point
            command = "z {}".format(device_name)
            self.input_cmd(command)
            text = _("Device {} zapped from monitor points").format(
                device_name
            )

        self.push_status(text)
