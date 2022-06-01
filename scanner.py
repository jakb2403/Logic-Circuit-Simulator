"""Read the circuit definition file and translate the characters into symbols.

Used in the Logic Simulator project to read the characters in the definition
file and translate them into symbols that are usable by the parser.

Classes
-------
Scanner - reads definition file and translates characters into symbols.
Symbol - encapsulates a symbol and stores its properties.
"""
from inspect import FrameInfo, currentframe, getframeinfo
import sys
import os


class Symbol:

    """Encapsulate a symbol and store its properties.

    Parameters
    ----------
    No parameters.

    Public methods
    --------------
    No public methods.
    """

    def __init__(self):
        """Initialise symbol properties."""
        self.type = None
        self.id = None


class Scanner:

    """Read circuit definition file and translate the characters into symbols.

    Once supplied with the path to a valid definition file, the scanner
    translates the sequence of characters in the definition file into symbols
    that the parser can use. It also skips over comments and irrelevant
    formatting characters, such as spaces and line breaks.

    Parameters
    ----------
    path: path to the circuit definition file.
    names: instance of the names.Names() class.

    Public methods
    -------------
    get_symbol(self): Translates the next sequence of characters into a symbol
                      and returns the symbol.
    """

    def __init__(self, path, names):
        """Open specified file and initialise reserved words and IDs."""

        self.char_counter = 0
        file_name = os.path.basename(path)

        try:
            self.file = open(file_name, "r")
        except IOError:
            print("Error: can\'t find file or read data")
            sys.exit()

        self.line_length = []
        self.file.seek(0, 0)
        # indicate get_symbol which state current_character is
        self.indicator_types = [self.NORMAL, self.MISSING,
                                self.AFTERDOT, self.NONE] = range(4)
        self.indicator = self.NONE
        self.missed_symbol = ""
        self.current_character = ""

        self.names = names

        self.symbol_type_list = [
            self.DOT,
            self.COMMA,
            self.SEMICOLON,
            self.EQUALS,
            self.ARROW,
            self.OPENBRACKET,
            self.CLOSEDBRACKET,
            self.OPENCURLYBRACKET,
            self.CLOSEDCURLYBRACKET,
            self.KEYWORD,
            self.DEVICE_ARG,
            self.DEVICE,
            self.DTYPE_IP,
            self.DTYPE_OP,
            self.NUMBER,
            self.NAME,
            self.EOF] = range(17)

        self.keywords_list = ["DEVICES", "CONNECT", "MONITOR", "I"]
        self.device_arg_list = ["CLOCK", "AND", "NAND", "OR", "NOR", "SWITCH"]
        self.device_list = ["DTYPE", "XOR"]
        self.dtype_ip_list = ["SET", "CLEAR", "DATA", "CLK"]
        self.dtype_op_list = ["Q", "QBAR"]
        [self.DEVICES_ID, self.CONNECT_ID, self.MONITOR_ID,
            self.I_ID] = self.names.lookup(self.keywords_list)
        [self.CLOCK_ID, self.AND_ID, self.NAND_ID, self.OR_ID, self.NOR_ID,
            self.SWITCH_ID] = self.names.lookup(self.device_arg_list)
        [self.DTYPE_ID, self.XOR_ID] = self.names.lookup(self.device_list)
        [self.SET_ID, self.CLEAR_ID, self.DATA_ID,
            self.CLK_ID] = self.names.lookup(self.dtype_ip_list)
        [self.Q_ID, self.QBAR_ID] = self.names.lookup(self.dtype_op_list)

    def get_next_character(self):
        """Read and return the next character."""
        # add 1 to the character counter to track location in line
        self.char_counter += 1
        return(self.file.read(1))

    def skip_spaces(self):
        """Seek and return the next non-whitespace character."""
        nwc = self.get_next_character()
        for i in range(1000):
            if nwc.isspace():
                nwc = self.get_next_character()
            else:
                return(nwc)

    def get_number(self):
        """Seek and return the next number."""
        num = ""
        num += self.current_character
        for i in range(1000):
            next_num = self.get_next_character()
            if next_num.isdigit():
                num += next_num
                self.current_character = next_num
            else:
                self.missed_symbol = next_num
                return num

    def get_name(self):
        """Seek and return the next name."""
        name = ""
        name += self.current_character
        for i in range(1000):
            next_char = self.get_next_character()
            if next_char.isalnum():
                name += next_char
                self.current_character = next_char
            else:
                self.missed_symbol = next_char
                return name

    def error_found(self):
        """Outputs the current line and a ^ symbol on the next line to
        highlight the location of the error"""
        current_location = self.file.tell()
        self.file.seek(0,0)
        line_counter = 0
        char_counter = 0
        for i in range(current_location):
            x = self.get_next_character()
            char_counter += 1
            if x =="\n":
                char_counter -= 1
                self.line_length.append(char_counter)
                line_counter += 1
                char_counter = -1
        if char_counter == -1:
            line_counter -= 1
            char_counter = self.line_length[-2]

        self.file.seek(0,0)
        line_text = self.file.read().split("\n")[line_counter-1]
        output = line_text + "\n" + " "*char_counter +"^" 
        return output

    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""
        symbol = Symbol()
        if (self.indicator == self.NORMAL or self.indicator == self.AFTERDOT
                or self.indicator == self.NONE):
            self.current_character = self.skip_spaces()
        elif self.indicator == self.MISSING:
            self.current_character = self.missed_symbol
            if self.current_character.isspace():
                self.current_character = self.skip_spaces()

        # if symbol is a name
        if self.current_character.isalpha():
            # differntiate I from name
            if (self.indicator == self.AFTERDOT and
                    self.current_character in self.keywords_list):
                self.indicator = self.NORMAL
                symbol.type = self.KEYWORD
                symbol.id = self.names.lookup(self.current_character)
            else:
                self.indicator = self.MISSING
                name_string = self.get_name()
                if name_string in self.keywords_list:
                    symbol.type = self.KEYWORD
                elif name_string in self.device_arg_list:
                    symbol.type = self.DEVICE_ARG
                elif name_string in self.device_list:
                    symbol.type = self.DEVICE
                elif name_string in self.dtype_ip_list:
                    symbol.type = self.DTYPE_IP
                elif name_string in self.dtype_op_list:
                    symbol.type = self.DTYPE_OP
                else:
                    symbol.type = self.NAME
                [symbol.id] = self.names.lookup([name_string])

        # if symbol is a number
        elif self.current_character.isdigit():
            self.indicator = self.MISSING
            symbol.id = self.get_number()
            symbol.type = self.NUMBER

        # if symbol is a dot
        elif self.current_character == ".":
            self.indicator = self.AFTERDOT
            symbol.type = self.DOT

        # if symbol is a comma
        elif self.current_character == ",":
            self.indicator = self.NORMAL
            symbol.type = self.COMMA

        # if symbol is a semicolon
        elif self.current_character == ";":
            self.indicator = self.NORMAL
            symbol.type = self.SEMICOLON

        # if symbol is a equals
        elif self.current_character == "=":
            self.indicator = self.NORMAL
            symbol.type = self.EQUALS

        # if symbol is an arrow
        elif self.current_character == "-":
            self.current_character = self.skip_spaces()
            if self.current_character == ">":
                self.indicator = self.NORMAL
                symbol.type = self.ARROW
            else:
                pass

        # if symbol is an openbracket
        elif self.current_character == "(":
            self.indicator = self.NORMAL
            symbol.type = self.OPENBRACKET

        # if symbol is an closedbracket
        elif self.current_character == ")":
            self.indicator = self.NORMAL
            symbol.type = self.CLOSEDBRACKET

        # if symbol is an opencurlybracket
        elif self.current_character == "{":
            self.indicator = self.NORMAL
            symbol.type = self.OPENCURLYBRACKET

        # if symbol is an closedcurlybracket
        elif self.current_character == "}":
            self.indicator = self.NORMAL
            symbol.type = self.CLOSEDCURLYBRACKET

        # if symbol is the end of file
        elif self.current_character == "":
            self.indicator = self.NORMAL
            symbol.type = self.EOF

        # if symbol is a hashtag - comment
        elif self.current_character == "#":
            self.indicator = self.NORMAL
            while True:
                self.current_character = self.get_next_character()
                if self.current_character == "\n":
                    break
            return self.get_symbol()

        # if symbol is an invalid character
        else:
            pass
        return symbol
