"""Create GUI command line panel.

Used in gui.py to make instance of the GUI command line.

Classes
-------
CmdPanel - creates wx panel for GUI command line interface
"""

import wx


class CmdPanel(wx.Panel):
    """Create wx.Panel for canvas."""

    def __init__(
        self, parent, names, devices, network, monitors, userint, push_status
    ):
        """Initialise the CmdPanel panel.

        Parameters
        ----------
        parent
            parent panel
        names
            instance of names class
        devices
            instance of devices class
        network
            instance of network class
        monitors
            instance of monitors class
        userint
            instance of userint class
        push_status
            GUI statusbar pushstatus function
        """
        wx.Panel.__init__(self, parent)
        self.SetFont(
            wx.Font(
                13,
                wx.FONTFAMILY_TELETYPE,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                "Courier",
            )
        )
        # self.SetBackgroundColour(wx.WHITE)

        self.parent = parent
        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors
        self.push_status = push_status
        self.userint = userint

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Create sizers for input and output
        output_sizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create widgets
        self.cmd_output_text_box = wx.TextCtrl(
            self, style=wx.TE_MULTILINE | wx.TE_READONLY, size=wx.Size(400, 10)
        )
        self.com_text = wx.StaticText(self, wx.ID_ANY, "#")
        self.cmd_input_text_box = wx.TextCtrl(
            self, wx.BOTTOM, "", style=wx.TE_PROCESS_ENTER
        )

        # Add widgets to sizer
        output_sizer.Add(self.cmd_output_text_box, 1, wx.EXPAND, 0)
        # TODO to set value of textbox: self.textpanel.SetValue(s)
        input_sizer.Add(
            self.com_text, 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5
        )
        input_sizer.Add(self.cmd_input_text_box, 1, wx.RIGHT, 15)

        # Add sub-sizers to main sizer
        self.sizer.Add(output_sizer, 1, wx.EXPAND, 0)
        self.sizer.Add(input_sizer, 0, wx.EXPAND, 0)

        # Bind events to event handlers
        self.cmd_input_text_box.Bind(wx.EVT_TEXT_ENTER, self.on_cmd_enter)

        self.SetSizer(self.sizer)

        self.cmd_output_init()

    def cmd_output_init(self):
        """Initialise the GUI command line with a help message."""
        self.cmd_output_text_box.Clear()
        start_statement = _(
            "Logic Simulator: interactive command line user interface.\n"
            "Enter 'h' for help.\n"
        )
        self.output_cmd(start_statement)

    def on_cmd_enter(self, event):
        """Handle the event when the user enters text."""
        user_input = self.cmd_input_text_box.GetValue()
        self.cmd_input_text_box.Clear()
        self.output_cmd("\n#:" + user_input)
        if user_input == "q":
            self.parent.on_close(None)
        self.userint.command_interface(
            user_input, self.output_cmd, self.input_cmd
        )
        text = "".join(["New cmd input: ", user_input])
        self.push_status(text)

    def input_cmd(self, command):
        """Type the command text in the GUI command input box and press enter.

        Parameters
        ----------
        command
            command to be input
        """
        self.cmd_input_text_box.Clear()
        self.cmd_input_text_box.AppendText(command)
        self.on_cmd_enter(None)

    def output_cmd(self, text):
        """Output the command to the GUI command line output.

        Parameters
        ----------
        text
            text to be output
        """
        self.cmd_output_text_box.AppendText("\n" + text)
