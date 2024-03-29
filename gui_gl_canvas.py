"""Create OpenGL canvas for drawing signals.

Used in gui_canvas.py to create a canvas

Classes
-------
MyGLCanvas - handles all canvas drawing operations.
"""


import wx
import wx.glcanvas as wxcanvas
from OpenGL import GL, GLUT, GLU
from dataclasses import dataclass
from PIL import Image


@dataclass
class coord:
    """Class for storing screen coordinates."""

    x: int = 0
    y: int = 0


class MyGLCanvas(wxcanvas.GLCanvas):
    """Handle all drawing operations.

    This class contains functions for drawing onto the canvas. It
    also contains handlers for events relating to the canvas.

    Parameters
    ----------
    parent: parent window.
    devices: instance of the devices.Devices() class.
    monitors: instance of the monitors.Monitors() class.

    Public methods
    --------------
    init_gl(self): Configures the OpenGL context.

    render(self, text): Handles all drawing operations.

    on_paint(self, event): Handles the paint event.

    on_size(self, event): Handles the canvas resize event.

    on_mouse(self, event): Handles mouse events.

    render_text(self, text, x_pos, y_pos): Handles text drawing
                                           operations.
    """

    def __init__(self, parent, devices, monitors, push_status):
        """Initialise canvas properties and useful variables."""
        self.parent = parent
        self.push_status = push_status

        self.devices = devices
        self.monitors = monitors

        super().__init__(
            parent,
            -1,
            attribList=[
                wxcanvas.WX_GL_RGBA,
                wxcanvas.WX_GL_DOUBLEBUFFER,
                wxcanvas.WX_GL_DEPTH_SIZE,
                16,
                0,
            ],
        )
        GLUT.glutInit()
        self.init = False
        self.context = wxcanvas.GLContext(self)

        self.width = 0
        self.height = 0

        # Initialise variables for panning
        self.pan_x = 0
        self.pan_y = 0
        self.last_mouse_x = 0  # previous mouse x position
        self.last_mouse_y = 0  # previous mouse y position

        # Initialise variables for zooming
        self.zoom = 1

        # Bind events to the canvas
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse)

    def init_gl(self):
        """Configure and initialise the OpenGL context."""
        size = self.GetClientSize()
        self.SetCurrent(self.context)
        GL.glDrawBuffer(GL.GL_BACK)
        GL.glClearColor(1.0, 1.0, 1.0, 0.0)
        GL.glViewport(0, 0, size.width, size.height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(0, size.width, 0, size.height, -1, 1)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glTranslated(self.pan_x, self.pan_y, 0.0)
        GL.glScaled(self.zoom, self.zoom, self.zoom)

    def render(self):
        """Handle all drawing operations."""
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        # Clear everything
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        # Draw the monitor signals
        index = 0
        for device_id, output_id in self.monitors.monitors_dictionary:
            monitor_name = self.devices.get_signal_name(device_id, output_id)
            signal_list = self.monitors.monitors_dictionary[
                (device_id, output_id)
            ]
            if len(signal_list) > 0:
                signal_list_bin = self.convert_signal(signal_list)
                self.draw_signal(monitor_name, signal_list_bin, index)
            index += 1

        # We have been drawing to the back buffer, flush the graphics pipeline
        # and swap the back buffer to the front
        GL.glFlush()
        self.SwapBuffers()

    def on_paint(self, event):
        """Handle the paint event."""
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        size = self.GetClientSize()
        self.update_size(size.width, size.height)
        self.render()

    def on_size(self, event):
        """Handle the canvas resize event."""
        # Forces reconfiguration of the viewport, modelview and projection
        # matrices on the next paint event
        self.init = False

    def on_mouse(self, event):
        """Handle mouse events."""
        text = ""
        # Calculate object coordinates of the mouse position
        size = self.GetClientSize()
        ox = (event.GetX() - self.pan_x) / self.zoom
        oy = (size.height - event.GetY() - self.pan_y) / self.zoom
        old_zoom = self.zoom
        if event.ButtonDown():
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()

        if event.ButtonUp():
            pass
        if event.Leaving():
            pass
        if event.Dragging():
            self.pan_x += event.GetX() - self.last_mouse_x
            self.pan_y -= event.GetY() - self.last_mouse_y
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
            self.init = False

        if event.GetWheelRotation() < 0:
            self.zoom *= 1.0 + (
                event.GetWheelRotation() / (20 * event.GetWheelDelta())
            )
            if self.zoom < 0:
                self.zoom = 0.001
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False

        if event.GetWheelRotation() > 0:
            self.zoom /= 1.0 - (
                event.GetWheelRotation() / (20 * event.GetWheelDelta())
            )
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False

        self.render()
        self.Refresh()  # triggers the paint event

    def render_text(self, text, x_pos, y_pos):
        """Handle text drawing operations."""
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        GL.glColor3f(0.0, 0.0, 0.0)  # text is black
        GL.glRasterPos2f(x_pos, y_pos)
        # Alternative font
        # font = GLUT.GLUT_STROKE_ROMAN
        font = GLUT.GLUT_BITMAP_HELVETICA_10
        for character in text:
            if character == "\n":
                y_pos = y_pos - 20
                GL.glRasterPos2f(x_pos, y_pos)
            else:
                GLUT.glutBitmapCharacter(font, ord(character))

    def convert_signal(self, signal_list):
        """Convert signal from output type of network module to 1s and 0s."""
        output_signal = []
        for i in range(len(signal_list) - 1):
            current_sig = signal_list[i]
            # HIGH
            if current_sig == self.devices.HIGH:
                output_signal.append(1)
            # LOW
            elif current_sig == self.devices.LOW:
                output_signal.append(0)
            elif current_sig == self.devices.BLANK:
                output_signal.append(None)
            else:
                continue

        if signal_list[-1] == self.devices.HIGH:
            output_signal.append(1)
        elif signal_list[-1] == self.devices.LOW:
            output_signal.append(0)

        return output_signal

    def draw_signal(self, monitor_name, signal_list_bin, index):
        """Draw a signal to the canvas.

        Parameters
        ----------
        monitor_name
            the signal name of the monitor, for the label
        signal_list_bin
            signal values as list of binary numbers
        index
            the position of the signal in the list of monitored signals
        """
        v_space = 60
        one_cycle = 20
        text_x_offset = 10
        signal_height = v_space * 2 // 3
        signal_x_offset = 30
        signal_y_offset = v_space - signal_height
        tick_length = 10
        tick_y_offset = v_space - signal_height - tick_length
        signal_length = len(signal_list_bin)

        bottom_left = coord(0, (index + 1) * v_space)
        y_low = bottom_left.y + v_space - signal_height
        y_high = bottom_left.y + v_space

        # Draw the tickmarks
        tick_start = coord()
        tick_end = coord()
        for i in range(signal_length + 1):
            if i % 5 == 0:
                tick_start.x = signal_x_offset + (i * one_cycle)
                tick_start.y = bottom_left.y + tick_y_offset
                tick_end.x = signal_x_offset + (i * one_cycle)
                tick_end.y = bottom_left.y + tick_y_offset + tick_length
                GL.glColor3f(
                    180.0 / 256.0, 180.0 / 256.0, 180.0 / 256.0
                )  # tick marks are grey
                GL.glBegin(GL.GL_LINE_STRIP)
                GL.glVertex2f(tick_start.x, tick_start.y)
                GL.glVertex2f(tick_end.x, tick_end.y)
                GL.glEnd()
                self.render_text(str(i), tick_start.x + 1, tick_start.y)

        # Draw the last tick
        if signal_length % 5 != 0:
            tick_start.x = signal_x_offset + (signal_length * one_cycle)
            tick_start.y = bottom_left.y + tick_y_offset
            tick_end.x = signal_x_offset + (signal_length * one_cycle)
            tick_end.y = bottom_left.y + tick_y_offset + tick_length
            GL.glColor3f(
                180.0 / 256.0, 180.0 / 256.0, 180.0 / 256.0
            )  # tick marks are grey
            GL.glBegin(GL.GL_LINE_STRIP)
            GL.glVertex2f(tick_start.x, tick_start.y)
            GL.glVertex2f(tick_end.x, tick_end.y)
            GL.glEnd()
            self.render_text(
                str(signal_length), tick_start.x + 1, tick_start.y
            )

        # Draw the horizontal tickmarks for 1 and 0
        for i in range(2):
            tick_start.x = signal_x_offset - tick_length
            tick_start.y = (
                bottom_left.y + signal_y_offset + (i * signal_height)
            )
            tick_end.x = signal_x_offset
            tick_end.y = bottom_left.y + signal_y_offset + (i * signal_height)
            GL.glColor3f(
                180.0 / 256.0, 180.0 / 256.0, 180.0 / 256.0
            )  # tick marks are grey
            GL.glBegin(GL.GL_LINE_STRIP)
            GL.glVertex2f(tick_start.x, tick_start.y)
            GL.glVertex2f(tick_end.x, tick_end.y)
            GL.glEnd()
            self.render_text(str(i), tick_start.x, tick_start.y + 1)

        # Draw the x axis
        GL.glColor3f(
            180.0 / 256.0, 180.0 / 256.0, 180.0 / 256.0
        )  # axis is grey
        GL.glBegin(GL.GL_LINE_STRIP)
        axis_start = coord(
            signal_x_offset, bottom_left.y + tick_y_offset + tick_length
        )
        axis_end = coord(
            signal_x_offset + signal_length * one_cycle,
            bottom_left.y + tick_y_offset + tick_length,
        )
        GL.glVertex2f(axis_start.x, axis_start.y)
        GL.glVertex2f(axis_end.x, axis_end.y)
        GL.glEnd()

        # Draw the signal trace
        GL.glColor3f(
            87.0 / 256.0, 184.0 / 256.0, 255.0 / 256.0
        )  # signal trace is blue
        GL.glLineWidth(2)
        GL.glBegin(GL.GL_LINE_STRIP)
        sig_current = coord()
        sig_next = coord()
        just_blank = False
        for i in range(signal_length):
            if just_blank:
                GL.glBegin(GL.GL_LINE_STRIP)
                just_blank = not (just_blank)
            sig_current.x = signal_x_offset + (i * one_cycle)
            sig_next.x = signal_x_offset + ((i + 1) * one_cycle)
            if signal_list_bin[i] == 0:
                sig_current.y = y_low
                sig_next.y = y_low
                GL.glVertex2f(sig_current.x, sig_current.y)
                GL.glVertex2f(sig_next.x, sig_next.y)
            elif signal_list_bin[i] == 1:
                sig_current.y = y_high
                sig_next.y = y_high
                GL.glVertex2f(sig_current.x, sig_current.y)
                GL.glVertex2f(sig_next.x, sig_next.y)
            elif signal_list_bin is None:
                GL.glEnd()
                just_blank = not (just_blank)
                continue
        GL.glEnd()
        GL.glLineWidth(1)

        # Display signal name
        display_text = monitor_name
        self.render_text(
            display_text,
            text_x_offset,
            (bottom_left.y + signal_y_offset + signal_height // 2),
        )

    def update_size(self, width=None, height=None):
        """Update the class variables storing the size of the canvas."""
        if not (width is None) and width > self.width:
            self.width = width
        if not (height is None) and height > self.height:
            self.height = height

    def save_to_png(self, filename):
        """Save the current view in the canvas pael to a .png."""
        data = GL.glReadPixels(
            0, 0, self.width, self.height, GL.GL_RGB, GL.GL_UNSIGNED_BYTE, None
        )
        image = Image.frombytes("RGB", (self.width, self.height), data)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image.save(filename, format="png")
