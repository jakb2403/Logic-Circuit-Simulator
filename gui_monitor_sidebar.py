from typing import Counter
import wx
from wx.core import SingleChoiceDialog

class MonitorSidebarPanel(wx.Panel):
    def __init__(self, parent, names, devices, network, monitors, push_status):
        wx.Panel.__init__(self, parent)
        # self.SetBackgroundColour(wx.RED)

        self.parent = parent
        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors
        self.push_status = push_status

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.monitor_dict = {
            0: ["AND1", 0, 1],
            1: ["AND2", 1, 1],
            2: ["NAND1", 2, 1],
            3: ["NOR1", 3, 1],
            4: ["XOR1", 4, 1],
        }
        self.monitor_names = [item[0] for item in [*self.monitor_dict.values()]]

        # self.monitor_dict = {}
        # checkbox_index = 0
        # for device_id, output_id in self.monitors.monitors_dictionary:
        #     monitor_name = self.devices.get_signal_name(device_id, output_id)
        #     signal_list = self.monitors.monitors_dictionary[(device_id, output_id)]
        #     self.monitor_dict[checkbox_index] = [monitor_name, device_id, output_id]
        #     checkbox_index += 1

        # Create widgets
        info_text = wx.StaticText(self, wx.ID_ANY, "Choose devices to monitor:")
        self.monitor_checklist = wx.CheckListBox(
            self, choices=self.monitor_names, name="Monitor Signals")


        self.sizer.Add(info_text, 0, wx.ALL, 3)
        self.sizer.Add(self.monitor_checklist, 1,
                       wx.EXPAND | wx.LEFT | wx.RIGHT, 0)

        # Bind events to event handlers
        self.monitor_checklist.Bind(wx.EVT_CHECKLISTBOX, self.on_check)

        self.SetSizer(self.sizer)

    def on_check(self, event):
        """Handle the event when the user clicks one of the checkbox items"""
        checked_items_index = self.monitor_checklist.GetCheckedItems()
        checked_names = []
        for checkbox_index in checked_items_index:
            device_id = self.monitor_dict[checkbox_index][1]
            output_id = self.monitor_dict[checkbox_index][2]
            cycles_completed = self.parent.cycles_completed
            self.monitors.make_monitor(device_id, output_id, cycles_completed)
            
            checked_names.append(self.monitor_dict[checkbox_index][0])

        text = f"These signals are now being shown: {(', '.join(checked_names))}"
        self.push_status(text)
