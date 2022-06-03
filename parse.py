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
        self.isoutput = True
        self.error_categories = [self.SYNTAX, self.SEMANTIC] = range(2)
        self.stopping_symbols = [self.scanner.SEMICOLON, self.scanner.COMMA, self.scanner.EOF]
        self.missed_symbol = False
        
        [self.invalid_device_name,
        self.invalid_arg_type,
        self.port_error,
        self.missing_symbol,
        self.unrecognised_device_type,
        self.missing_keyword,
        self.invalid_arg,
        self.duplicate_name,
        self.duplicate_monitor,
        self.input_to_input,
        self.output_to_output,
        self.port_absent,
        self.input_connected] = self.names.unique_error_codes(13)

    def error(self, category, type=None, skip=True, sym=None):
        print(self.scanner.error_found())
        self.error_count += 1
        if category == self.SYNTAX:
            print("SyntaxError: ", end="")
        elif category == self.SEMANTIC:
            print("SemanticError: ", end="")
        
        if type == self.invalid_device_name:
            print("invalid device name")
        if type == self.invalid_arg_type:
            print("argument type error")
        if type == self.port_error:
            print("invalid port identifier")
        if type == self.missing_symbol:
            print("missing symbol: ", sym)
        if type == self.unrecognised_device_type:
            print("unrecognised device type")
        if type == self.missing_keyword:
            print("missing keyword")
        if type == self.invalid_arg:
            print("argument outside of accepted range")
        if type == self.duplicate_name:
            print("name already used in previous device assignment")
        if type == self.duplicate_monitor:
            print("monitor point already declared")
        if type == self.input_to_input:
            print("input connected to input")
        if type == self.output_to_output:
            print("output connected to output")
        if type == self.port_absent:
            print("port is absent")
        if type == self.input_connected:
            print("input is already connected")
        if skip == True: # if you want skipping until stopping symbol
            while self.symbol.type not in self.stopping_symbols:
                self.symbol = self.scanner.get_symbol()

    def name(self):
        """Parse a name and return the name ID if it is a valid name
        Else return None"""
        if self.symbol.type == self.scanner.NAME:
            device_id = self.symbol.id
            self.symbol = self.scanner.get_symbol()
            return device_id
        else:
            self.error(self.SYNTAX, self.invalid_device_name) # invalid device name
            return None

    def argument(self):
        """Parse an argument and return the number
        Else return None (if it's not a number)"""
        if self.symbol.type == self.scanner.NUMBER:
            argument = int(self.symbol.id)
            self.symbol = self.scanner.get_symbol()
            return argument
        else:
            self.error(self.SYNTAX, self.invalid_arg_type) # invalid argument type
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
                if self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.I_ID: # see "I"
                    self.isoutput = False
                    self.symbol = self.scanner.get_symbol()
                    port_id = self.argument() # TODO do we need to check for bad port_id
                elif self.symbol.type == self.scanner.DTYPE_IP: # see dtype input
                    self.isoutput = False
                    if self.symbol.id == self.devices.SET_ID:
                        port_id = self.devices.SET_ID
                    elif self.symbol.id == self.devices.CLEAR_ID:
                        port_id = self.devices.CLEAR_ID
                    elif self.symbol.id == self.devices.DATA_ID:
                        port_id = self.devices.DATA_ID
                    elif self.symbol.id == self.devices.CLK_ID:
                        port_id = self.devices.CLK_ID
                elif self.symbol.type == self.scanner.DTYPE_OP: # see dtype output
                    self.isoutput = True
                    if self.symbol.id == self.devices.Q_ID:
                        port_id = self.devices.Q_ID
                    elif self.symbol.id == self.devices.QBAR_ID:
                        port_id = self.devices.QBAR_ID
                else: # unrecognised port 
                    self.error(self.SYNTAX, self.port_error) # unrecognised port 
                    device_id = None
                    port_id = None
            else: # there was no "."
                self.isoutput = True
                port_id = None
            return device_id, port_id

    def device(self):
        """Parse a device name

        Returns:
            device_kind - type of device
            device_property - number of inputs to the device (None if device
            without arguments)
        """
        if self.symbol.type == self.scanner.DEVICE:  # if the symbol is a
            # device without arguments
            if self.symbol.id == self.scanner.DTYPE_ID:  # it's a DTYPE
                device_kind = self.devices.D_TYPE
            elif self.symbol.id == self.scanner.XOR_ID:  # it's a XOR
                device_kind = self.devices.XOR
            self.symbol = self.scanner.get_symbol()
            return device_kind, None
        elif self.symbol.type == self.scanner.DEVICE_ARG:  # if the symbol is
            # a device with arguments
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
            if self.symbol.type == self.scanner.OPENBRACKET:  # intended for a
                # device with an argument
                self.symbol = self.scanner.get_symbol()
                device_property = self.argument()
                if device_property is not None:  # the argument was valid
                    if self.symbol.type == self.scanner.CLOSEDBRACKET:  # we
                        # remembered to close the bracket
                        self.symbol = self.scanner.get_symbol()
                        return device_kind, device_property
                    else: # we forgot to close the bracket
                        self.error(self.SYNTAX, self.missing_symbol, sym=")") #  missing ")"
                        return None, None
                else:  # the argument was not valid
                    return None, None
            else: # we forgot an "("
                self.error(self.SYNTAX, self.missing_symbol, sym="(") #  missing symbol, expected "("
                return None, None
        else:  # device is not recoginised
            device_type = None
            self.error(self.SYNTAX, self.unrecognised_device_type) #  unrecognised device type
            return None, None  

    def assignment(self):
        """Parse an assigment line.
        This could be a list of names or a single name.
        Make all the devices, as required."""
        name_list = []  # to store any names, single or multiple
        device_id = self.name()
        if device_id is not None:
            name_list.append(device_id)  # store valid name in list
            while self.symbol.type == self.scanner.COMMA:  # see a ","
                self.symbol = self.scanner.get_symbol()
                device_id = self.name()
                if device_id is not None:  # it's a valid name
                    name_list.append(device_id)  # store valid name in list
                else:  # it's not a valid name
                    break
                if self.symbol.type == self.scanner.EOF:  # stop infinite loop
                    break
            if self.symbol.type == self.scanner.NAME: # we encountered another name without a ","
                self.error(self.SYNTAX, self.missing_symbol, sym=",") #  missing symbol ","
            elif self.symbol.type == self.scanner.EQUALS: # finished reading in names
                self.symbol = self.scanner.get_symbol()
                device_kind, device_property = self.device()
                if device_kind is not None:  # it's a valid device
                    error_list = []  # create list of errors to catch duplicate names and arguments outside range
                    for i in range(len(name_list)):
                        error_type = self.devices.make_device(
                            name_list[i], device_kind, device_property)
                        error_list.append(error_type)
                    if self.devices.INVALID_QUALIFIER in error_list: # argument for device outside of range
                        self.error(self.SEMANTIC, self.invalid_arg) #  invalid argument
                    if self.devices.DEVICE_PRESENT in error_list or len(name_list) != len(set(name_list)): # used name in device declaration (duplicate name used)
                        self.error(self.SEMANTIC, self.duplicate_name) #  used name in device declaration
                    if all(item == self.devices.NO_ERROR for item in error_list): # there is no error
                        pass
                else: # it's not a valid device
                    pass # device outputs error for us here
            else: # not another name or "=", therefore an error
                self.error(self.SYNTAX, self.missing_symbol, sym="=") #  missing "="
        
    def connection(self):
        """Parse a connection statement.
        Make all the connections, as required."""
        first_device_id, first_port_id = self.signal_name() # call signal_name and save device_id and port_id
        second_device_ids = [] # list to store device ids of inputs
        second_port_ids = [] # list to store port ids of inputs
        error_list = [] # list to store errors returned from network 
        if first_device_id is not None: # it's a valid signal name
            if self.symbol.type == self.scanner.ARROW:  # see a "->"
                self.symbol = self.scanner.get_symbol()
                second_device_id, second_port_id =  self.signal_name()
                if second_device_id is not None: # it's a valid signal name
                    second_device_ids.append(second_device_id)
                    second_port_ids.append(second_device_id)
                    while self.symbol.type == self.scanner.COMMA: # see a ","
                        self.symbol = self.scanner.get_symbol()
                        second_device_id, second_port_id =  self.signal_name()
                        if second_device_id is not None: # it's a valid signal name
                            second_device_ids.append(second_device_id)
                            second_port_ids.append(second_device_id)
                        else: # signal_name does raise error
                            break
                        if self.symbol.type == self.scanner.EOF: # prevent infinite loop
                            break
                    for i in range(len(second_device_ids)):
                        error = self.network.make_connection(first_device_id, first_port_id, second_device_ids[i], second_port_ids[i])
                        error_list.append(error)
                    if self.network.INPUT_CONNECTED in error_list: # input is already in a connection
                        self.error(self.SEMANTIC, self.input_connected) # TODO 
                    if self.network.INPUT_TO_INPUT in error_list:  # both ports are inputs
                        self.error(self.SYNTAX, self.input_to_input) # TODO
                    if self.network.OUTPUT_TO_OUTPUT in error_list: # both ports are outputs
                        self.error(self.SYNTAX, self.output_to_output) # TODO
                    if self.network.PORT_ABSENT in error_list: # invalid port
                        self.error(self.SEMANTIC, self.port_absent) # TODO
                    if all(item == self.network.NO_ERROR for item in error_list): # there is no error
                        pass
            else: # you don't see an arrow
                self.error(self.SYNTAX, self.missing_symbol, sym="->")
        
    def monitor(self):
        """Parse a monitor statement.
        Make all monitor points, as required."""
        device_id, output_id = self.signal_name()
        if self.isoutput == False:
            input_id, input_port = device_id, output_id
            device_id, output_id = self.network.get_connected_output(input_id, input_port)
        error = self.monitors.make_monitor(device_id, output_id)
        if error == self.monitors.MONITOR_PRESENT:
            self.error(self.SEMANTIC, self.duplicate_monitor)
        elif error == self.monitors.NO_ERROR:
            pass
    
    def section_devices(self):
        """
        Parse a section of assignments.
        """
        if (self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.DEVICES_ID): # cheking for keyword "DEVICES" to start the devices section
            self.symbol = self.scanner.get_symbol()
        else: # missing the keyword "DEVICES"
            self.error(self.SYNTAX, self.missing_keyword) #  missing keyword "DEVICES
        self.assignment() 
        while self.symbol.type == self.scanner.COMMA: # see a ","
            self.symbol = self.scanner.get_symbol()
            self.assignment()
        if self.symbol.type == self.scanner.SEMICOLON: # see a ";" to end the section
            self.symbol = self.scanner.get_symbol()
        elif self.symbol.type == self.scanner.NAME:
            self.error(self.SYNTAX, self.missing_symbol, sym=",") #  missing symbol, expected ","
        elif (self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.CONNECT_ID):
            self.error(self.SYNTAX, self.missing_symbol, skip=False, sym=";") #  missing symbol, expected ";"
            self.missed_symbol = True
        else:
            self.error(self.SYNTAX, self.missing_symbol, sym=";")

    def section_connect(self):
        """
        Parse a section of connections.
        """
        if (self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.CONNECT_ID or self.missed_symbol == True): #checking for keyword "CONNECT" to start the connect section
            self.missed_symbol = False
            self.symbol = self.scanner.get_symbol()
        else:  # missing the keyword "CONNECT"
            self.error(self.SYNTAX, self.missing_keyword) # missing keyword "CONNECT"
        self.connection()
        while self.symbol.type == self.scanner.COMMA: # see a ","
            self.symbol = self.scanner.get_symbol()
            self.connection()
        if self.symbol.type == self.scanner.SEMICOLON: # see a ";" to end the section
            self.symbol = self.scanner.get_symbol()
        elif self.symbol.type == self.scanner.NAME:
            self.error(self.SYNTAX, self.missing_symbol, sym=",") #  missing symbol, expected ","
        elif (self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.MONITOR_ID):
            self.error(self.SYNTAX, self.missing_symbol, skip=False, sym=";") #  missing symbol, expected ";"
            self.missed_symbol = True
        else:
            self.error(self.SYNTAX, self.missing_symbol, sym=";")

    def section_monitor(self):
        """
        Parse a section of connections.
        """
        if (self.symbol.type == self.scanner.KEYWORD and self.symbol.id == self.scanner.MONITOR_ID or self.missed_symbol == True): #checking for keyword "MONITOR" to start the connect section
            self.missed_symbol = False
            self.symbol = self.scanner.get_symbol()
        else:  # missing the keyword "MONITOR"
            self.error(self.SYNTAX, self.missing_keyword) # missing keyword "CONNECT"
        self.monitor()
        while self.symbol.type == self.scanner.COMMA: # see a ","
            self.symbol = self.scanner.get_symbol()
            self.monitor()
        if self.symbol.type == self.scanner.SEMICOLON: # see a ";" to end the section
            self.symbol = self.scanner.get_symbol()
        else:
            self.error(self.SYNTAX, self.missing_symbol, sym=";")

    def program(self):
        """
        Parse the entire program.
        """
        self.symbol = self.scanner.get_symbol()
        self.section_devices()
        self.section_connect()
        self.section_monitor()


    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.
        self.program()
        if self.error_count == 0:
            return True
        else:
            print(f"Error Count: {self.error_count}")
