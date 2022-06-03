"""Parse the definition file and build the logic network.

Used in the Logic Simulator project to analyse the syntactic and semantic
correctness of the symbols received from the scanner and then builds the
logic network.

Classes
-------
Parser - parses the definition file and builds the logic network.
"""


class Parser:

    """Parse the definition file and build the logic network.

    The parser deals with error handling. It analyses the syntactic and
    semantic correctness of the symbols it receives from the scanner, and
    then builds the logic network. If there are errors in the definition file,
    the parser detects this and tries to recover from it, giving helpful
    error messages.

    Parameters
    ----------
    names: instance of the names.Names() class.
    devices: instance of the devices.Devices() class.
    network: instance of the network.Network() class.
    monitors: instance of the monitors.Monitors() class.
    scanner: instance of the scanner.Scanner() class.

    Public methods
    --------------
    parse_network(self): Parses the circuit definition file.
    """

    def __init__(self, names, devices, network, monitors, scanner):
        """Initialise constants."""

        # get instances of other modules from arguments
        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors
        self.scanner = scanner

        # initialise error counter
        self.error_count = 0

        # [] = self.names.unique_error_codes()

    def syntax_error(self):
        print(self.scanner.error_found())
        self.error_count += 1
        print("Error encountered")

    def name(self):
        """Parse a name and return the name ID if it is a valid name
        Else return None"""
        if self.symbol.type == self.scanner.NAME:
            device_id = self.symbol.id
            self.symbol = self.scanner.get_symbol()
            return device_id
        else:
            self.syntax_error()   # TODO invalid device name
            return None

    def argument(self):
        """Parse an argument and return the number
        Else return None (if it's not a number)"""
        if self.symbol.type == self.scanner.NUMBER:
            argument = int(self.symbol.id)
            self.symbol = self.scanner.get_symbol()
            return argument
        else:
            self.syntax_error()  # TODO invalid argument type
            return None

    def signal_name(self):
        """Parse an input or output name in the formats
            input - [name].I[port_id] 
                or  [name].[dtype_ip]
            output -[name]
                or  [name].[dtype_op]
            Returns device_id and port_id
        """
        device_id = self.name()
        if device_id is not None:  # if the device name is valid
            if self.symbol.type == self.scanner.DOT:  # seen a "."
                self.symbol = self.scanner.get_symbol()
                if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.I_ID:  # see "I"
                    self.symbol = self.scanner.get_symbol()
                    port_id = self.argument()  # TODO do we need to check for bad port_id
                elif self.symbol.type == self.scanner.DTYPE_IP:  # see dtype input
                    if self.symbol.id == self.devices.SET_ID:
                        port_id = self.devices.SET_ID
                    elif self.symbol.id == self.devices.CLEAR_ID:
                        port_id = self.devices.CLEAR_ID
                    elif self.symbol.id == self.devices.DATA_ID:
                        port_id = self.devices.DATA_ID
                    elif self.symbol.id == self.devices.CLK_ID:
                        port_id = self.devices.CLK_ID
                elif self.symbol.type == self.scanner.DTYPE_OP:  # see dtype output
                    if self.symbol.id == self.devices.Q_ID:
                        port_id = self.devices.Q_ID
                    elif self.symbol.id == self.devices.QBAR_ID:
                        port_id = self.devices.QBAR_ID
                else:  # unrecognised port
                    self.syntax_error()  # TODO unrecognised port
                    device_id = None
                    port_id = None
            else:  # there was no "."
                port_id = None
            return device_id, port_id

    def device(self):
        """Parse a device name

        Returns:
            device_kind - type of device
            device_property - number of inputs to the device (None if device without arguments)
        """
        if self.symbol.type == self.scanner.DEVICE:  # if the symbol is a device without arguments
            if self.symbol.id == self.scanner.DTYPE_ID:  # it's a DTYPE
                device_kind = self.devices.D_TYPE
            elif self.symbol.id == self.scanner.XOR_ID:  # it's a XOR
                device_kind = self.devices.XOR
            self.symbol = self.scanner.get_symbol()
            return device_kind, None
        elif self.symbol.type == self.scanner.DEVICE_ARG:  # if the symbol is a device with arguments
            if self.symbol.id == self.scanner.CLOCK_ID:  # it's a CLOCK
                device_kind = self.devices.CLOCK
            if self.symbol.id == self.scanner.AND_ID:  # it's a AND
                device_kind = self.devices.AND
            if self.symbol.id == self.scanner.OR_ID:  # it's a OR
                device_kind = self.devices.OR
            if self.symbol.id == self.scanner.NAND_ID:  # it's a NAND
                device_kind = self.devices.NAND
            if self.symbol.id == self.scanner.NOR_ID:  # it's a NOR
                device_kind = self.devices.NOR
            if self.symbol.id == self.scanner.SWITCH_ID:  # it's a SWITCH
                device_kind = self.devices.SWITCH
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.OPENBRACKET:  # intended for a device with an argument
                self.symbol = self.scanner.get_symbol()
                device_property = self.argument()
                if device_property is not None:  # the argument was valid
                    if self.symbol.type == self.scanner.CLOSEDBRACKET:  # we remembered to close the bracket
                        self.symbol = self.scanner.get_symbol()
                        return device_kind, device_property
                    else:  # we forgot to close the bracket
                        self.syntax_error()  # TODO missing ")"
                        return None, None
                else:  # the argument was not valid
                    return None, None
            else:  # we forgot an "("
                self.syntax_error()  # TODO missing symbol, expected "("
                return None, None
        else:  # device is not recoginised
            device_type = None
            self.syntax_error()  # TODO unrecognised device type
            return None, None

    def assignment(self):
        """Parse an assigment line.
        This could be a list of names or a single name.
        Make all the devices, as required."""
        pass

    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.
        return True
