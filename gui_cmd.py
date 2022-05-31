import wx

class CmdPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.GREEN)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Create sizers for input and output
        output_sizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create widgets
        self.cmd_output_text_box = wx.TextCtrl(
            self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.com_text = wx.StaticText(self, wx.ID_ANY, "$")
        self.cmd_input_text_box = wx.TextCtrl(self, wx.BOTTOM, "",
                                              style=wx.TE_PROCESS_ENTER)

        # Add widgets to sizer
        output_sizer.Add(self.cmd_output_text_box, 0, wx.EXPAND, 0)
        # TODO to set value of textbox: self.textpanel.SetValue(s)
        input_sizer.Add(self.com_text, 0, wx.LEFT |
                        wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 12)
        input_sizer.Add(self.cmd_input_text_box, 1, wx.RIGHT, 5)

        # Add sub-sizers to main sizer
        self.sizer.Add(output_sizer, 1, wx.EXPAND, 0)
        self.sizer.Add(input_sizer, 0, wx.EXPAND, 0)

        # Bind events to event handlers
        self.cmd_input_text_box.Bind(wx.EVT_TEXT_ENTER, self.on_cmd_enter)

        self.SetSizer(self.sizer)

    def on_cmd_enter(self, event):
        """Handle the event when the user enters text."""
        text_box_value = self.cmd_input_text_box.GetValue()
        self.cmd_input_text_box.Clear()
        self.cmd_output_text_box.AppendText("\n $  " + text_box_value)
        text = "".join(["New text box value: ", text_box_value])
        
