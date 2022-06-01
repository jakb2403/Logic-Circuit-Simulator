"""Implement the graphical user interface for the Logic Simulator.

Used in the Logic Simulator project to enable the user to run the simulation
or adjust the network properties.

Classes:
--------
MyGLCanvas - handles all canvas drawing operations.
Gui - configures the main window and all the widgets.
"""
import wx
from wx.core import ROLE_SYSTEM_TOOLBAR, VERTICAL
import wx.lib.agw.aui as aui

from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner
from parse import Parser

from gui_cmd import CmdPanel
from gui_monitor_sidebar import MonitorSidebarPanel
from gui_switches_sidebar import SwitchesSidebarPanel
from gui_gl_canvas import MyGLCanvas


class Gui(wx.Frame):
    """Configure the main window and all the widgets.

    This class provides a graphical user interface for the Logic Simulator and
    enables the user to change the circuit properties and run simulations.

    Parameters
    ----------
    title: title of the window.

    Public methods
    --------------
    on_menu(self, event): Event handler for the file menu.

    on_spin(self, event): Event handler for when the user changes the spin
                           control value.

    on_run_button(self, event): Event handler for when the user clicks the run
                                button.

    on_text_box(self, event): Event handler for when the user enters text.
    """

    def __init__(self, title, path, names, devices, network, monitors):
        """Initialise widgets and layout."""
        super().__init__(parent=None, title=title, size=(800, 600))

        self.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT,
                     wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, 'Arial'))

        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors

        # Create AUI manager
        self.mgr = aui.AuiManager()
        # Set the window that the AUI manages
        self.mgr.SetManagedWindow(self)

        # Configure the file menu
        fileMenu = wx.Menu()
        menuBar = wx.MenuBar()
        fileMenu.Append(wx.ID_ABOUT, "&About")
        fileMenu.Append(wx.ID_EXIT, "&Exit")
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)

        # Configure the toolbar
        self.toolbar = self.CreateToolBar()
        self.load_button = self.toolbar.AddTool(
            100, "Load", wx.Bitmap("icons/folder.png"))
        self.run_button = self.toolbar.AddTool(
            101 , "Run", wx.Bitmap("icons/run.png"))
        self.cont_button = self.toolbar.AddTool(
            102, "Continue", wx.Bitmap("icons/continue.png"))
        self.cycle_spin = wx.SpinCtrl(self.toolbar, wx.ID_ANY, "10")
        self.toolbar.AddControl(self.cycle_spin)
        self.exit_button = self.toolbar.AddTool(
            103, "Exit", wx.Bitmap("icons/exit.png"))

        # Configure the status bar
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("Status")

        # Canvas for drawing signals
        self.canvas = MyGLCanvas(self, devices, monitors)

        # Create instance of panel classes
        self.monitor_sidebar = MonitorSidebarPanel(self)
        self.switches_sidebar = SwitchesSidebarPanel(self)
        self.cmd = CmdPanel(self)

        # Add panels to AUI manager
        self.mgr.AddPane(self.canvas, aui.AuiPaneInfo().CenterPane())
        self.mgr.AddPane(
            self.monitor_sidebar, aui.AuiPaneInfo().Left().Floatable(False).CloseButton(False).Caption("Monitor Points"))
        self.mgr.AddPane(
            self.switches_sidebar, aui.AuiPaneInfo().Left().Floatable(False).CloseButton(False).Caption("Control Switches"))
        self.mgr.AddPane(self.cmd, aui.AuiPaneInfo().Bottom().Floatable(False).CloseButton(False).Caption("Command Line"))

        # Set docking guides (THIS FIXES THE FLOATING POINT PROBLEM)
        agwFlags = self.mgr.GetAGWFlags()
        self.mgr.SetAGWFlags(agwFlags | aui.AUI_MGR_AERO_DOCKING_GUIDES)

        self.mgr.Update()

        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.toolbar.Bind(wx.EVT_TOOL, self.on_click_tool)
        self.cycle_spin.Bind(wx.EVT_SPINCTRL, self.on_spin)

        self.toolbar.Realize()
        self.Centre()
        self.Show(True)

    def on_spin(self, event):
        """Handle the event when the user changes the spin control value."""
        spin_value = self.spin.GetValue()
        text = "".join(["New spin control value: ", str(spin_value)])

    def on_click_tool(self, event):
        """Handle the event when the user clicks a button in the toolbar"""
        tool_id = event.GetId()
        if tool_id == 100: # Load button
            with wx.FileDialog(self, "Load .txt file", wildcard=".txt files (*.txt)|*.txt", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return     # the user changed their mind

                # Proceed loading the file chosen by the user
                pathname = fileDialog.GetPath()
                text = "".join(["Opening file: ", pathname])
                self.statusbar.PushStatusText(text)

        elif tool_id == 101: # Run button 
            text = "Run button pressed."
            self.statusbar.PushStatusText(text)
        elif tool_id == 102: # Continue button
            text = "Continue button pressed."
            self.statusbar.PushStatusText(text)
        elif tool_id == 103: # Exit button
            text = "Exiting"
            self.statusbar.PushStatusText(text)
            self.mgr.UnInit()
            self.Destroy()


    def on_menu(self, event):
        """Handle the event when the user selects a menu item."""
        Id = event.GetId()
        if Id == wx.ID_EXIT:
            self.Close(True)
        if Id == wx.ID_ABOUT:
            wx.MessageBox("Logic Simulator\nCreated by Mojisola Agboola\n2017",
                          "About Logsim", wx.ICON_INFORMATION | wx.OK)

    def on_close(self, event):
        # deinitialise the frame manager
        self.mgr.UnInit()
        self.Destroy()
        self.Close()