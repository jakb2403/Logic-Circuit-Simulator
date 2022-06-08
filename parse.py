"""Parse the definition file and build the logic network.

Used in the Logic Simulator project to analyse the syntactic and semantic
correctness of the symbols received from the scanner and then builds the
logic network.

Classes
-------
Parser - parses the definition file and builds the logic network.
"""
import builtins
import wx
builtins._ = wx.GetTranslation


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

    Non-public methods
    ------------------
    _parser_output(self, text, end="\n"): Print text to the correct output
                                          terminal.

    _error(self, category, type=None, sym=None, keyword=None): Print error and
                                                               skip parsing
                                                               until stopping
                                                               symbol.

    _name(self): Parse a name and return the name ID if it is a valid name.

    _argument(self): Parse an argument and return the number.

    _signal_name(self): Parse an input or output name and return device_id
                        and port_id.

    _device(self): Parse a device name and return device_kind and
                   device_property.

    _assignment(self): Parse an assignment statement and make device.

    _connection(self): Parse a connection statement in _section_connect and
                       connect the devices.

    _monitor(self): Parse a monitor statement in _section_monitor and make
                    monitor point.

    _section_devices(self): Parse a devices section.

    _section_connect(self): Parse a connect section.

    _section_monitor(self): Parse a monitor section.

    _section(self,type): Call _section_### function if a keyword is present.
                         If keyword is not present call the intended function.
                         Return section type.

    _program(self): Parse the entire program.
    """

    def __init__(
        self,
        names,
        devices,
        network,
        monitors,
        scanner,
        mode="terminal",
        output_cmd=None,
    ):
        """Initialise constants."""

        self.mode = mode
        self.output_cmd = output_cmd

        # get instances of other modules from arguments
        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors
        self.scanner = scanner

        # initialise error counter, error categories, and stopping symbols
        self.error_count = 0
        self.error_categories = [self.SYNTAX, self.SEMANTIC] = range(2)
        self.stopping_symbols = [
            self.scanner.SEMICOLON,
            self.scanner.EOF,
        ] = range(2)

        # boolean variable indicating whether signal_name is input or output
        self.isoutput = True

        self.section_type = [self.dev, self.con, self.mon] = range(3)

        [
            self.invalid_device_name,
            self.device_as_name,
            self.keyword_as_name,
            self.dtype_as_name,
            self.invalid_arg_type,
            self.port_error,
            self.missing_symbol,
            self.missing_argument,
            self.unrecognised_device_type,
            self.missing_keyword,
            self.invalid_arg,
            self.duplicate_name,
            self.duplicate_monitor,
            self.monitor_is_input,
            self.input_to_input,
            self.output_to_output,
            self.port_absent,
            self.input_connected,
            self.unconnected_inputs,
            self.section_order_error,
        ] = self.names.unique_error_codes(20)

    def _parser_output(self, text, end="\n"):
        """Print text to the correct output terminal."""
        if self.mode == "terminal":
            print(text, end=end)
        elif self.mode == "gui":
            self.output_cmd(text)

    def _error(self, category, type=None, sym=None, keyword=None, skip=True):
        """Print error category (syntax or semantic), error type,
        and error location. Error location is specified using error_found
        function from scanner.py.
        If an error is found, skip parsing until stopping symbol.
        """
        self._parser_output(self.scanner.error_found())
        self.error_count += 1

        if type == self.invalid_device_name:
            self._parser_output(_("invalid device name\n"))
        if type == self.device_as_name:
            self._parser_output(
                _("device type '{}' cannot be device name\n").format(keyword)
            )
        if type == self.dtype_as_name:
            self._parser_output(
                _("dtype input/output '{}' cannot" " be device name\n").format(
                    keyword
                )
            )
        if type == self.keyword_as_name:
            self._parser_output(
                _("keyword '{}' cannot be device name\n").format(keyword)
            )
        if type == self.invalid_arg_type:
            self._parser_output(_("invalid argument type\n"))
        if type == self.port_error:
            self._parser_output(_("invalid port identifier\n"))
        if type == self.missing_symbol:
            self._parser_output(_("missing symbol: {}\n").format(sym))
        if type == self.missing_argument:
            self._parser_output(
                _("missing argument for decive type '{}'\n").format(keyword)
            )
        if type == self.unrecognised_device_type:
            self._parser_output(_("unrecognised device type\n"))
        if type == self.missing_keyword:
            self._parser_output(_("missing keyword '{}'\n").format(keyword))
        if type == self.invalid_arg:
            self._parser_output(
                _("argument '{}' outside of accepted range\n").format(keyword)
            )
        if type == self.duplicate_name:
            self._parser_output(
                _(
                    "name '{}' already used in previous device" " assignment\n"
                ).format(keyword)
            )
        if type == self.duplicate_monitor:
            self._parser_output(
                _("monitor point '{}' already declared\n").format(keyword)
            )
        if type == self.monitor_is_input:
            self._parser_output(
                _("monitor point is an input, only outputs are allowed\n")
            )
        if type == self.input_to_input:
            self._parser_output(_("input connected to input\n"))
        if type == self.output_to_output:
            self._parser_output(_("output connected to output\n"))
        if type == self.port_absent:
            self._parser_output(_("port is absent\n"))
        if type == self.input_connected:
            self._parser_output(_("input is already connected\n"))
        if type == self.unconnected_inputs:
            self._parser_output(
                _("incomplete network, not all inputs are connected\n")
            )
        if type == self.section_order_error:
            self._parser_output(_("incorrect ordering of sections\n"))
        if skip is True:
            while self.symbol.type not in self.stopping_symbols:
                self.symbol = self.scanner.get_symbol()
        elif skip is False:
            self.symbol = self.scanner.get_symbol()

    def _name(self):
        """Parse a name and return the name ID if it is a valid name.
        Else return None."""
        if self.symbol.type == self.scanner.NAME:
            device_id = self.symbol.id
            self.symbol = self.scanner.get_symbol()
            return device_id
        # if device type is device name
        elif (
            self.symbol.type == self.scanner.DEVICE
            or self.symbol.type == self.scanner.DEVICE_ARG
        ):
            device_type = self.names.get_name_string(self.symbol.id)
            self._error(self.SYNTAX, self.device_as_name, keyword=device_type)
            return None
        # if dtype input output is device name
        elif (
            self.symbol.type == self.scanner.DTYPE_IP
            or self.symbol.type == self.scanner.DTYPE_OP
        ):
            dtype = self.names.get_name_string(self.symbol.id)
            self._error(self.SYNTAX, self.dtype_as_name, keyword=dtype)
            return None
        # if keyword is device name
        elif self.symbol.type == self.scanner.KEYWORD:
            keyword = self.names.get_name_string(self.symbol.id)
            self._error(self.SYNTAX, self.keyword_as_name, keyword=keyword)
            return None
        else:
            # invalid device name
            self._error(self.SYNTAX, self.invalid_device_name)
            return None

    def _argument(self):
        """Parse an argument and return the number.
        Else return None (if it's not a number)."""
        if self.symbol.type == self.scanner.NUMBER:
            argument = int(self.symbol.id)
            self.symbol = self.scanner.get_symbol()
            return argument
        else:
            # invalid argument type
            self._error(self.SYNTAX, self.invalid_arg_type)
            return None

    def _signal_name(self):
        """Parse an input or output name in the formats:
        input - [name].I[port_id]
            or  [name].[dtype_ip]
        output -[name]
            or  [name].[dtype_op].
        Returns device_id and port_id.
        """
        device_id = self._name()
        if device_id is not None:  # if the device name is valid
            if self.symbol.type == self.scanner.DOT:  # seen a "."
                self.symbol = self.scanner.get_symbol()
                if (
                    self.symbol.type == self.scanner.KEYWORD
                    and self.symbol.id == self.scanner.I_ID
                ):  # see "I"
                    self.isoutput = False
                    self.symbol = self.scanner.get_symbol()
                    arg = self._argument()
                    if arg is not None:  # if the argument is valid
                        port_id = self.names.lookup(f"I{arg}")
                    else:  # if the argument is invalid
                        device_id = None  # <- error
                        port_id = None
                # see dtype input
                elif self.symbol.type == self.scanner.DTYPE_IP:
                    self.isoutput = False
                    if self.symbol.id == self.devices.SET_ID:
                        port_id = self.devices.SET_ID
                    elif self.symbol.id == self.devices.CLEAR_ID:
                        port_id = self.devices.CLEAR_ID
                    elif self.symbol.id == self.devices.DATA_ID:
                        port_id = self.devices.DATA_ID
                    elif self.symbol.id == self.devices.CLK_ID:
                        port_id = self.devices.CLK_ID
                    self.symbol = self.scanner.get_symbol()
                # see dtype output
                elif self.symbol.type == self.scanner.DTYPE_OP:
                    self.isoutput = True
                    if self.symbol.id == self.devices.Q_ID:
                        port_id = self.devices.Q_ID
                    elif self.symbol.id == self.devices.QBAR_ID:
                        port_id = self.devices.QBAR_ID
                    self.symbol = self.scanner.get_symbol()
                else:  # unrecognised port
                    # unrecognised port
                    self._error(self.SYNTAX, self.port_error)
                    device_id = None  # <- error
                    port_id = None
            else:  # there was no "." -> output
                self.isoutput = True
                port_id = None
            return (device_id, port_id)
        else:  # if the device name is invalid
            return (None, None)

    def _device(self):
        """Parse a device name.

        Returns:
            device_kind - type of device
            device_property - number of inputs to the device (None if device
            without arguments).
        """
        # if the symbol is a device without arguments
        if self.symbol.type == self.scanner.DEVICE:
            if self.symbol.id == self.scanner.DTYPE_ID:  # it's a DTYPE
                device_kind = self.devices.D_TYPE
            elif self.symbol.id == self.scanner.XOR_ID:  # it's a XOR
                device_kind = self.devices.XOR
            elif self.symbol.id == self.scanner.NOT_ID:  # it's a NOT
                device_kind = self.devices.NOT
            self.symbol = self.scanner.get_symbol()
            return device_kind, None
        # if the symbol is a device with arguments
        elif self.symbol.type == self.scanner.DEVICE_ARG:
            device_id = self.names.get_name_string(self.symbol.id)
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
            # device with arguments have to be followed by an openbracket
            if self.symbol.type == self.scanner.OPENBRACKET:
                self.symbol = self.scanner.get_symbol()
                device_property = self._argument()
                if device_property is not None:  # the argument was valid
                    # we remembered to close the bracket
                    if self.symbol.type == self.scanner.CLOSEDBRACKET:
                        self.symbol = self.scanner.get_symbol()
                        return device_kind, device_property
                    else:  # we forgot to close the bracket
                        # missing ")"
                        self._error(self.SYNTAX, self.missing_symbol, sym=")")
                        return None, None
                else:  # the argument was not valid
                    return None, None
            else:  # we forgot an "("
                # missing argument for device
                self._error(
                    self.SYNTAX, self.missing_argument, keyword=device_id
                )
                return None, None
        else:  # device is not recoginised
            self._error(self.SYNTAX, self.unrecognised_device_type)
            return None, None

    def _assignment(self):
        """Parse an assigment line.
        This could be a list of names or a single name.
        Make all the devices, as required."""
        name_list = []  # to store any names, single or multiple
        device_id = self._name()
        if device_id is not None:  # if device name is valid
            name_list.append(device_id)  # store valid name in list
        # see a "," or the next symbol is not stopping symbol
        while self.symbol.type == self.scanner.COMMA:
            self.symbol = self.scanner.get_symbol()
            device_id = self._name()
            if device_id is not None:  # valid name
                name_list.append(device_id)  # store valid name in list
            else:  # it's not a valid name
                break
            if self.symbol.type == self.scanner.EOF:
                break
        # we encountered another name without a ","
        if self.symbol.type == self.scanner.NAME:
            self._error(
                self.SYNTAX, self.missing_symbol, sym=","
            )  # missing symbol ","
        # finished reading in names
        elif self.symbol.type == self.scanner.EQUALS:
            self.symbol = self.scanner.get_symbol()
            device_kind, device_property = self._device()
            if device_kind is not None:  # it's a valid device
                error_list = []  # create list of errors to catch duplicate
                # names and arguments outside range
                for i in range(len(name_list)):
                    error_type = self.devices.make_device(
                        name_list[i], device_kind, device_property
                    )
                    error_list.append(error_type)
                # argument for device outside of range
                if self.devices.INVALID_QUALIFIER in error_list:
                    # invalid argument
                    self._error(
                        self.SEMANTIC,
                        self.invalid_arg,
                        keyword=device_property,
                    )
                # used name in device declaration (duplicate name used)
                if self.devices.DEVICE_PRESENT in error_list or len(
                    name_list
                ) != len(set(name_list)):
                    device_name = self.names.get_name_string(device_id)
                    # used name in device declaration
                    self._error(
                        self.SEMANTIC, self.duplicate_name, keyword=device_name
                    )
            else:  # it's not a valid device
                pass  # device outputs error for us here
        else:  # not another name or "=", therefore missing equals symbol
            self._error(
                self.SYNTAX, self.missing_symbol, sym="="
            )  # missing "="
        if self.symbol.type == self.scanner.SEMICOLON:  # see ";"
            pass
        else:
            self._error(self.SYNTAX, self.missing_symbol, sym=";")

    def _connection(self):
        """Parse a connection statement.
        Make all the connections, as required."""
        # call signal_name and save device_id and port_id
        first_device_id, first_port_id = self._signal_name()
        second_device_ids = []  # list to store device ids of inputs
        second_port_ids = []  # list to store port ids of inputs
        error_list = []  # list to store errors returned from network
        if first_device_id is not None:  # it's a valid signal name
            if self.symbol.type == self.scanner.ARROW:  # see a ">"
                self.symbol = self.scanner.get_symbol()
                second_device_id, second_port_id = self._signal_name()
                if second_device_id is not None:  # it's a valid signal name
                    # add device_id to list of device ids
                    second_device_ids.append(second_device_id)
                    # add port_id to list of port ids
                    second_port_ids.append(second_port_id)
                while self.symbol.type == self.scanner.COMMA:  # see a ","
                    self.symbol = self.scanner.get_symbol()
                    second_device_id, second_port_id = self._signal_name()
                    # it's a valid signal name
                    if second_device_id is not None:
                        # add device_id to list of device ids
                        second_device_ids.append(second_device_id)
                        # add port_id to list of port ids
                        second_port_ids.append(second_port_id)
                    else:  # signal_name raises an error
                        break
                    if self.symbol.type == self.scanner.EOF:
                        break
                # iterate over devices in connection output
                for i in range(len(second_device_ids)):
                    # see if an error is returned by network.make_connection
                    error = self.network.make_connection(
                        first_device_id,
                        first_port_id,
                        second_device_ids[i],
                        second_port_ids[i],
                    )
                    # add the error to a list of errors
                    error_list.append(error)
                # input is already in a connection
                if self.network.INPUT_CONNECTED in error_list:
                    self._error(self.SEMANTIC, self.input_connected)
                # both ports are inputs
                if self.network.INPUT_TO_INPUT in error_list:
                    self._error(self.SYNTAX, self.input_to_input)
                # both ports are outputs
                if self.network.OUTPUT_TO_OUTPUT in error_list:
                    self._error(self.SYNTAX, self.output_to_output)
                if self.network.PORT_ABSENT in error_list:  # invalid port
                    self._error(self.SEMANTIC, self.port_absent)
            else:  # you don't see an arrow
                self._error(self.SYNTAX, self.missing_symbol, sym=">")
        if self.symbol.type == self.scanner.SEMICOLON:
            pass
        else:  # you don't see a ";"
            self._error(self.SYNTAX, self.missing_symbol, sym=";")

    def _monitor(self):
        """Parse a monitor statement.
        Make all monitor points, as required."""
        device_id, output_id = self._signal_name()
        if self.isoutput is False:  # monitor point is an input, invalid
            self._error(self.SYNTAX, self.monitor_is_input)
        else:  # monitor point is an output, valid
            # see if an error is returned by monitors.make_monitor
            error = self.monitors.make_monitor(device_id, output_id)
            if error == self.monitors.MONITOR_PRESENT:
                monitor_name = self.names.get_name_string(device_id)
                if output_id is not None:
                    monitor_name += "."
                    monitor_name += self.names.get_name_string(output_id)
                self._error(
                    self.SEMANTIC, self.duplicate_monitor, keyword=monitor_name
                )
            if self.symbol.type == self.scanner.SEMICOLON:
                pass
            else:
                self._error(self.SYNTAX, self.missing_symbol, sym=";")

    def _section_devices(self):
        """Parse a section of assignments."""
        # cheking for keyword "DEVICES" to start the devices section
        if (
            self.symbol.type == self.scanner.KEYWORD
            and self.symbol.id == self.scanner.DEVICES_ID
        ):
            self.symbol = self.scanner.get_symbol()
        else:  # missing the keyword "DEVICES"
            # missing keyword "DEVICES
            self._error(
                self.SYNTAX,
                self.missing_keyword,
                keyword="DEVICES",
                skip=False,
            )
        self._assignment()
        # _assignment function ends with a semicolon
        while self.symbol.type == self.scanner.SEMICOLON:
            self.symbol = self.scanner.get_symbol()
            # stop loop when you see an "END"
            if (
                self.symbol.type == self.scanner.KEYWORD
                and self.symbol.id == self.scanner.END_ID
            ):
                break
            # stop loop when you see "CONNECT" or "MONITOR" and raise error
            elif self.symbol.type == self.scanner.KEYWORD and (
                self.symbol.id == self.scanner.CONNECT_ID
                or self.symbol.id == self.scanner.MONITOR_ID
            ):
                self._error(self.SYNTAX, self.missing_keyword, keyword="END")
                break
            # prevent infinite loop
            elif self.symbol.type == self.scanner.EOF:
                self._error(self.SYNTAX, self.missing_keyword, keyword="END")
                break
            else:
                self._assignment()
        if self.symbol.type != self.scanner.EOF:
            self.symbol = self.scanner.get_symbol()

    def _section_connect(self):
        """Parse a section of connections."""
        # cheking for keyword "CONNECT" to start the devices section
        if (
            self.symbol.type == self.scanner.KEYWORD
            and self.symbol.id == self.scanner.CONNECT_ID
        ):
            self.symbol = self.scanner.get_symbol()
        else:  # missing the keyword "CONNECT"
            # missing keyword "CONNECT
            self._error(
                self.SYNTAX,
                self.missing_keyword,
                keyword="CONNECT",
                skip=False,
            )
        self._connection()
        # _connection function ends with a semicolon
        while self.symbol.type == self.scanner.SEMICOLON:
            self.symbol = self.scanner.get_symbol()
            # stop loop when you see an "END"
            if (
                self.symbol.type == self.scanner.KEYWORD
                and self.symbol.id == self.scanner.END_ID
            ):
                break
            # stop loop when you see "DEVICES" or "MONITOR" and raise error
            elif self.symbol.type == self.scanner.KEYWORD and (
                self.symbol.id == self.scanner.DEVICES_ID
                or self.symbol.id == self.scanner.MONITOR_ID
            ):
                self._error(self.SYNTAX, self.missing_keyword, keyword="END")
                break
            # prevent infinite loop
            elif self.symbol.type == self.scanner.EOF:
                self._error(self.SYNTAX, self.missing_keyword, keyword="END")
                break
            else:
                self._connection()
        if self.symbol.type != self.scanner.EOF:
            self.symbol = self.scanner.get_symbol()

    def _section_monitor(self):
        """Parse a section of monitors."""
        # checking for keyword "MONITOR" to start the connect section
        if (
            self.symbol.type == self.scanner.KEYWORD
            and self.symbol.id == self.scanner.MONITOR_ID
        ):
            self.symbol = self.scanner.get_symbol()
        else:  # missing the keyword "MONITOR"
            # missing keyword "CONNECT"
            self._error(
                self.SYNTAX,
                self.missing_keyword,
                keyword="MONITOR",
                skip=False,
            )
        self._monitor()
        # _monitor function ends with a semicolon
        while self.symbol.type == self.scanner.SEMICOLON:
            self.symbol = self.scanner.get_symbol()
            # stop loop when you see an "END"
            if (
                self.symbol.type == self.scanner.KEYWORD
                and self.symbol.id == self.scanner.END_ID
            ):
                break
            # stop loop when you see "DEVICES" or "CONNECT" and raise error
            elif self.symbol.type == self.scanner.KEYWORD and (
                self.symbol.id == self.scanner.DEVICES_ID
                or self.symbol.id == self.scanner.CONNECT_ID
            ):
                self._error(self.SYNTAX, self.missing_keyword, keyword="END")
                break
            # prevent infinite loop
            elif self.symbol.type == self.scanner.EOF:
                self._error(self.SYNTAX, self.missing_keyword, keyword="END")
                break
            else:
                self._monitor()
        if self.symbol.type != self.scanner.EOF:
            self.symbol = self.scanner.get_symbol()

    def _section(self, type):
        """Call _section_### function if a keyword is present.
        If keyword is not present call the intended function.

        Return section type.
        """
        if (
            self.symbol.type == self.scanner.KEYWORD
            and self.symbol.id == self.scanner.DEVICES_ID
        ):
            self._section_devices()
            return self.dev
        elif (
            self.symbol.type == self.scanner.KEYWORD
            and self.symbol.id == self.scanner.CONNECT_ID
        ):
            self._section_connect()
            return self.con
        elif (
            self.symbol.type == self.scanner.KEYWORD
            and self.symbol.id == self.scanner.MONITOR_ID
        ):
            self._section_monitor()
            return self.mon
        else:  # if keyword is not present
            if type == self.dev:
                self._section_devices()
            elif type == self.con:
                self._section_connect()
            elif type == self.mon:
                self._section_monitor()
            return type

    def _program(self):
        """Parse the entire program."""
        self.symbol = self.scanner.get_symbol()
        section_dev = self._section(self.dev)
        # if the first section is not a devices section
        if section_dev != self.dev:
            self._error(self.SYNTAX, self.section_order_error, skip=False)
        section_con = self._section(self.con)
        # if the second section is not a connect section
        if section_con != self.con:
            self._error(self.SYNTAX, self.section_order_error, skip=False)
        section_mon = self._section(self.mon)
        # if the third section is not a monitor section
        if section_mon != self.mon:
            self._error(self.SYNTAX, self.section_order_error, skip=False)
        # if all inputs are connected
        if self.network.check_network() is True:
            pass
        # if not all inputs are connected
        elif self.network.check_network() is False:
            self._error(self.SEMANTIC, self.unconnected_inputs)

    def parse_network(self):
        """Parse the circuit definition file."""
        self._program()
        if self.error_count == 0:
            return True
        else:
            self._parser_output(_("Error Count: {}").format(self.error_count))
            return False
