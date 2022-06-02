"""Parse the definition file and build the logic network.

Used in the Logic Simulator project to analyse the syntactic and semantic
correctness of the symbols received from the scanner and then builds the
logic network.

Classes
-------
Parser - parses the definition file and builds the logic network.
"""


from distutils.log import error


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
        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors
        self.scanner = scanner

        self.error_count = 0
        [self.output_to_output, self.input_to_input, self.input_to_output,
         self.invalid_device_name, self.invalid_device_inOut_name,
         self.unrecognised_device_type, self.invalid_argument_type,
         self.missing_argument, self.missing_keyword,
         self.missing_symbol,
         self.section_order_error, self.device_as_name, self.keyword_as_name, self.dtype_as_name] = self.names.unique_error_codes(14)

        self.keyword = [self.scanner.DEVICES_ID,
                        self.scanner.CONNECT_ID,
                        self.scanner.MONITOR_ID]

    def syntax_error(self, error_type=None, dev=None, sym=None):
        """Print error type and count total number of syntax
        errors."""
        self.error_count += 1
        print(self.scanner.error_found())
        print("SyntaxError: ", end="")
        if error_type == self.output_to_output:
            print("output connected to output")
        elif error_type == self.input_to_input:
            print("input connected to input")
        elif error_type == self.input_to_output:
            print("input connected to output")
        elif error_type == self.invalid_device_name:
            print("invalid device name")
        elif error_type == self.invalid_device_inOut_name:
            print("invalid input/output name")
        elif error_type == self.unrecognised_device_type:
            print("unrecognised device type")
        elif error_type == self.invalid_argument_type:
            print("expected argument to be an integer")
        elif error_type == self.missing_argument:
            print("missing argument for device type: " + dev)
        elif error_type == self.missing_symbol:
            print("missing symbol: " + sym)
        elif error_type == self.missing_keyword:
            print("missing keyword")
        elif error_type == self.section_order_error:
            print("incorrect ordering of sections")
        elif error_type == self.keyword_as_name:
            print("keyword cannot be device name")
        elif error_type == self.device_as_name:
            print("device type cannot be device name")
        elif error_type == self.dtype_as_name:
            print("dtype input/output cannot be device name")
        elif error_type is None:
            print("fuck off")
        while (self.symbol.type != self.scanner.SEMICOLON
                and self.symbol.type != self.scanner.EOF):
            self.symbol = self.scanner.get_symbol()

    def name(self):
        """Pass when symbol is name."""
        print(self.scanner.current_character)
        if self.symbol.type == self.scanner.NAME:
            device_id = self.symbol.id
            self.symbol = self.scanner.get_symbol()
            return device_id
        elif (self.symbol.type == self.scanner.DEVICE or
                self.symbol.type == self.scanner.DEVICE_ARG):
            self.syntax_error(self.device_as_name)
            return None
        elif (self.symbol.type == self.scanner.DTYPE_IP or
                self.symbol.type == self.scanner.DTYPE_OP):
            self.syntax_error(self.dtype_as_name)
            return None
        elif self.symbol.type == self.scanner.KEYWORD:
            self.syntax_error(self.keyword_as_name)
            return None
        else:
            self.syntax_error(self.invalid_device_name)
            return None

    def argument(self):
        """Pass until symbol is not number."""
        if self.symbol.type == self.scanner.NUMBER:
            integer = self.symbol.id
            self.symbol = self.scanner.get_symbol()
            return int(integer)
        else:
            self.syntax_error(self.invalid_argument_type)
            return None

    def inputOroutput(self):
        self.name()
        if self.symbol.type == self.scanner.DOT:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.DTYPE_OP:
                self.symbol = self.scanner.get_symbol()
                return True
            elif (self.symbol.type == self.scanner.KEYWORD and
                    self.symbol.id == self.scanner.I_ID):
                self.argument()
                return False
            elif self.symbol.type == self.scanner.DTYPE_IP:
                self.symbol = self.scanner.get_symbol()
                return False
            else:
                self.syntax_error()
        else:
            return True

    def device(self):
        """device = "DTYPE" | "XOR" ;"""
        """device_arg = "CLOCK" | "AND" | "NAND" | "OR" | "NOR" | "SWITCH" ;"""
        if self.symbol.type == self.scanner.DEVICE:
            device_type = self.symbol.type
            if self.symbol.id == self.scanner.DTYPE_ID:
                device_kind = self.devices.D_TYPE
                dev_name = "DTYPE"
            else:
                device_kind = self.devices.XOR
                dev_name = "XOR"
            self.symbol = self.scanner.get_symbol()
        elif self.symbol.type == self.scanner.DEVICE_ARG:
            device_type = self.symbol.type
            if self.symbol.id == self.scanner.CLOCK_ID:
                device_kind = self.devices.CLOCK
                dev_name = "CLOCK"
            elif self.symbol.id == self.scanner.AND_ID:
                device_kind = self.devices.AND
                dev_name = "AND"
            elif self.symbol.id == self.scanner.OR_ID:
                device_kind = self.devices.OR
                dev_name = "OR"
            elif self.symbol.id == self.scanner.NAND_ID:
                device_kind = self.devices.NAND
                dev_name = "NAND"
            elif self.symbol.id == self.scanner.NOR_ID:
                device_kind = self.devices.NOR
                dev_name = "NOR"
            else:
                device_kind = self.devices.SWITCH
                dev_name = "SWITCH"
            self.symbol = self.scanner.get_symbol()
        else:
            device_type = None
            self.syntax_error(self.unrecognised_device_type)
            return [None, None]
        if device_type is not None:
            if self.symbol.type == self.scanner.OPENBRACKET:
                if device_type == self.scanner.DEVICE_ARG:
                    self.symbol = self.scanner.get_symbol()
                    device_property = self.argument()
                    if type(device_property) == int:
                        if self.symbol.type == self.scanner.CLOSEDBRACKET:
                            self.symbol = self.scanner.get_symbol()
                            return [device_kind, device_property]
                        else:
                            self.syntax_error(self.missing_symbol, sym=")")
                            return [None, None]
                else:
                    self.symbol = self.scanner.get_symbol()
                    if self.symbol.type == self.scanner.NUMBER:
                        device_property = self.argument()
                        if type(device_property) == int:
                            if self.symbol.type == self.scanner.CLOSEDBRACKET:
                                self.symbol = self.scanner.get_symbol()
                                return [device_kind, device_property]
                            else:
                                self.syntax_error(self.missing_symbol, sym=";")
                                return [None, None]
                    else:
                        self.syntax_error(self.missing_symbol, sym=";")
                        return [None, None]
            elif self.symbol.type == self.scanner.SEMICOLON:
                if device_type == self.scanner.DEVICE:
                    return [device_kind, None]
                else:
                    self.syntax_error(self.missing_argument, dev=dev_name)
                    return [None, None]
            else:
                if device_type == self.scanner.DEVICE:
                    self.syntax_error(self.missing_symbol, sym=";")
                    return [None, None]
                else:
                    self.syntax_error(self.missing_argument, dev=dev_name)
                    return [None, None]

    def assignment(self):
        name_list = []
        device_id = self.name()
        if device_id is not None:
            name_list.append(device_id)
            while self.symbol.type == self.scanner.COMMA:
                self.symbol = self.scanner.get_symbol()
                device_id = self.name()
                if device_id is not None:
                    name_list.append(device_id)
                else:
                    break
                if self.symbol.type == self.scanner.EOF:
                    break
            if self.symbol.type == self.scanner.EQUALS:
                self.symbol = self.scanner.get_symbol()
                [device_kind, device_property] = self.device()
                if device_kind is not None:
                    if self.symbol.type == self.scanner.SEMICOLON:
                        self.symbol = self.scanner.get_symbol()
                    else:
                        self.syntax_error(self.missing_symbol, sym=";")
            else:
                self.syntax_error(self.missing_symbol, sym="=")

    def connection(self):
        """connection = ( name | dtype_op), "->", ( input | dtype_ip ),
        { "," , ( input | dtype_ip ) }, ";" ;"""
        x = self.inputOroutput()
        if self.symbol.type == self.scanner.ARROW:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error()
        y = self.inputOroutput()
        if x is True and y is False:
            while self.symbol.type == self.scanner.COMMA:
                self.symbol = self.scanner.get_symbol()
                z = self.inputOroutput()
                if z is True:
                    self.syntax_error(self.output_to_output)
                    break
                if self.symbol.type == self.scanner.EOF:
                    break
        elif x is True and y is True:
            self.syntax_error(self.output_to_output)
        elif x is False and y is False:
            self.syntax_error(self.input_to_input)
        else:
            self.syntax_error(self.input_to_output)
        if self.symbol.type == self.scanner.SEMICOLON:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error(self.missing_symbol, ";")

    def monitor(self):
        """monitor = monitor_name, "=", ( name | input ), ";" ;"""
        self.inputOroutput()
        if self.symbol.type == self.scanner.SEMICOLON:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error(self.missing_symbol, ";")

    def section(self):
        if (self.symbol.type == self.scanner.KEYWORD and
                self.symbol.id in self.keyword):
            sec_def = self.symbol.id
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error(self.missing_keyword)
        if self.symbol.type == self.scanner.OPENCURLYBRACKET:
            self.symbol = self.scanner.get_symbol()
        else:
            self.syntax_error(self.missing_symbol, sym="{")
        if sec_def == self.scanner.DEVICES_ID:
            self.assignment()
        elif sec_def == self.scanner.CONNECT_ID:
            self.connection()
        else:
            self.monitor()
        while self.symbol.type != self.scanner.CLOSEDCURLYBRACKET:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.EOF:
                break
            else:
                if sec_def == self.scanner.DEVICES_ID:
                    self.assignment()
                elif sec_def == self.scanner.CONNECT_ID:
                    self.connection()
                else:
                    self.monitor()
        if self.symbol.type == self.scanner.CLOSEDCURLYBRACKET:
            self.symbol = self.scanner.get_symbol()
            return sec_def
        else:
            self.syntax_error(self.missing_symbol, sym="}")

    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.
        self.symbol = self.scanner.get_symbol()
        dev = self.section()
        con = self.section()
        mon = self.section()
        if dev != self.scanner.DEVICES_ID:
            self.syntax_error(self.section_order_error)
        if con != self.scanner.CONNECT_ID:
            self.syntax_error(self.section_order_error)
        if mon != self.scanner.MONITOR_ID:
            self.syntax_error(self.section_order_error)
        if self.error_count == 0:
            return True
        else:
            return False
