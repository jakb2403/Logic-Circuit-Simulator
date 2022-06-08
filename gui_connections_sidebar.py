import wx
from wx.core import Command, SingleChoiceDialog


class ConnectionsSidebarPanel(wx.Panel):
    def __init__(
        self,
        parent,
        names,
        devices,
        network,
        monitors,
        push_status,
        output_cmd,
    ):
        wx.Panel.__init__(self, parent)
        # self.SetBackgroundColour(wx.WHITE)

        self.parent = parent
        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors
        self.push_status = push_status
        self.output_cmd = output_cmd

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.current_connections_text_list = []
        self.new_connections_text_list = []

        # Create widgets
        info_text1 = wx.StaticText(
            self, wx.ID_ANY, "Choose a connection to replace:"
        )
        info_text2 = wx.StaticText(self, wx.ID_ANY, "Replace ...")
        self.dropdown_find = wx.Choice(
            self,
            wx.CB_DROPDOWN | wx.CB_READONLY,
            choices=self.current_connections_text_list,
            name="find",
        )
        info_text3 = wx.StaticText(self, wx.ID_ANY, "with ...")
        self.dropdown_replace = wx.Choice(
            self,
            wx.CB_DROPDOWN | wx.CB_READONLY,
            choices=self.new_connections_text_list,
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
        self.dropdown_find.Bind(wx.EVT_CHOICE, self.on_dropdown_find)
        self.replace_button.Bind(wx.EVT_BUTTON, self.on_click_replace)

        self.SetSizer(self.sizer)

    def update_dropdown_find(self):
        self.current_connections_text_list = []
        self.dropdown_find.Clear()
        self.dropdown_replace.Clear()
        self.connections_dict = self.network.get_all_connections()
        self.dropdown_find.Append("")
        self.current_connections_text_list = [""]
        for key in self.connections_dict:
            first_device_id = key[0]
            first_port_id = key[1]
            second_device_id = self.connections_dict[key][0]
            second_port_id = self.connections_dict[key][1]

            text = ""
            text += self.devices.get_signal_name(
                first_device_id, first_port_id
            )
            text += " > "
            text += self.devices.get_signal_name(
                second_device_id, second_port_id
            )

            self.current_connections_text_list.append(text)
            self.dropdown_find.Append(text)

    def on_dropdown_find(self, event):
        """Handle the event when the user uses the first (find) dropdown"""
        self.new_connections_text_list = []
        self.dropdown_replace.Clear()
        selection_index = self.dropdown_find.GetCurrentSelection()
        selected_text = self.dropdown_find.GetString(selection_index)
        signal_names = selected_text.split(" > ")
        first_signal_name = signal_names[0]
        second_signal_name = signal_names[1]
        [monitored, not_monitored] = self.monitors.get_signal_names()
        self.new_connections_text_list = [*monitored, *not_monitored]
        for i in range(len(self.new_connections_text_list)):
            third_signal_name = self.new_connections_text_list[i]
            text = "{} > {}".format(third_signal_name, second_signal_name)
            if text != selected_text:
                self.new_connections_text_list.append(text)
                self.dropdown_replace.Append(text)

    def on_click_replace(self, event):
        """Handle the event when the user clicks the Replace button"""
        selection_index = self.dropdown_replace.GetCurrentSelection()
        selected_text = self.dropdown_replace.GetString(selection_index)
        signal_names = selected_text.split(" > ")
        third_signal_name = signal_names[0]
        second_signal_name = signal_names[1]
        third_device_id, third_port_id = self.devices.get_signal_ids(
            third_signal_name
        )
        second_device_id, second_port_id = self.devices.get_signal_ids(
            second_signal_name
        )

        selection_index = self.dropdown_find.GetCurrentSelection()
        selected_text = self.dropdown_find.GetString(selection_index)
        first_signal_name = selected_text.split(" > ")[0]
        self.output_cmd(
            "\nReplacing connection\n"
            "{} > {}"
            "  with  "
            "{} > {}".format(
                first_signal_name,
                second_signal_name,
                third_signal_name,
                second_signal_name,
            )
        )
        self.network.replace_connection(
            second_device_id, second_port_id, third_device_id, third_port_id
        )
        self.update_dropdown_find()
