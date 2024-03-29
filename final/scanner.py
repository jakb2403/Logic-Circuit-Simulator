"""Read the circuit definition file and translate the characters into symbols.

Used in the Logic Simulator project to read the characters in the definition
file and translate them into symbols that are usable by the parser.

Classes
-------
Scanner - reads definition file and translates characters into symbols.
Symbol - encapsulates a symbol and stores its properties.
"""
from inspect import FrameInfo, currentframe, getframeinfo
from pathlib import Path
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
    --------------
    get_symbol(self): Translates the next sequence of characters into a symbol
                      and returns the symbol.

    error_found(self):Outputs the current line and a ^ symbol on the next line
                      to highlight the location of the error.

    Non-public methods
    ------------------
    _advance(self): Read the next character.

    _skip_spaces(self): Skip all whitespace character.

    _get_number(self): Seek and return the next number.

    _get_name(self): Seek and return the next name.
    """

    def __init__(self, path, names):
        """Open specified file and initialise reserved words and IDs."""
        self.char_counter = 0
        self.line_counter = 1

        if Path(str(path)).is_file():
            if Path(str(path)).suffix == ".txt":
                self.file = open(Path(str(path)), "r")

                self.file.seek(0, 0)
                self.current_character = self.file.read(1)

                self.names = names
                self.afterdot = False

                self.char_in_line = []

                self.symbol_type_list = [
                    self.NONETYPE,
                    # fixes a spurious error with scanner seeing a semicolon
                    # as the 0th element
                    self.DOT,
                    self.COMMA,
                    self.SEMICOLON,
                    self.EQUALS,
                    self.ARROW,
                    self.OPENBRACKET,
                    self.CLOSEDBRACKET,
                    self.KEYWORD,
                    self.DEVICE_ARG,
                    self.DEVICE,
                    self.DTYPE_IP,
                    self.DTYPE_OP,
                    self.NUMBER,
                    self.NAME,
                    self.EOF,
                ] = range(16)

                self.keywords_list = [
                    "DEVICES",
                    "CONNECT",
                    "MONITOR",
                    "END",
                    "I",
                ]
                self.device_arg_list = [
                    "CLOCK",
                    "AND",
                    "NAND",
                    "OR",
                    "NOR",
                    "SWITCH",
                ]
                self.device_list = ["DTYPE", "XOR", "NOT"]
                self.dtype_ip_list = ["SET", "CLEAR", "DATA", "CLK"]
                self.dtype_op_list = ["Q", "QBAR"]
                [
                    self.DEVICES_ID,
                    self.CONNECT_ID,
                    self.MONITOR_ID,
                    self.END_ID,
                    self.I_ID,
                ] = self.names.lookup(self.keywords_list)
                [
                    self.CLOCK_ID,
                    self.AND_ID,
                    self.NAND_ID,
                    self.OR_ID,
                    self.NOR_ID,
                    self.SWITCH_ID,
                ] = self.names.lookup(self.device_arg_list)
                [self.DTYPE_ID, self.XOR_ID, self.NOT_ID] = self.names.lookup(
                    self.device_list
                )
                [
                    self.SET_ID,
                    self.CLEAR_ID,
                    self.DATA_ID,
                    self.CLK_ID,
                ] = self.names.lookup(self.dtype_ip_list)
                [self.Q_ID, self.QBAR_ID] = self.names.lookup(
                    self.dtype_op_list
                )

            else:
                print(_("\nError: incorrect file type\n"))
        else:
            print(_("\nError invalid path\n"))

    def _advance(self):
        """Read the next character."""
        # add 1 to the character counter to track location in line
        self.current_character = self.file.read(1)
        self.char_counter += 1
        if self.current_character == "\n":
            self.char_in_line.append(self.char_counter - 1)
            self.line_counter += 1
            self.char_counter = 0

    def _skip_spaces(self):
        """Skip all whitespace character."""
        while self.current_character.isspace():
            self._advance()

    def _get_number(self):
        """Seek and return the next number."""
        num = ""
        num += self.current_character
        self._advance()
        while self.current_character.isdigit():
            num += self.current_character
            self._advance()

        return num

    def _get_name(self):
        """Seek and return the next name."""
        name = self.current_character
        self._advance()
        while self.current_character.isalnum():
            name += self.current_character
            self._advance()

        return name

    def error_found(self):
        """Scanner error output.

        Outputs the current line and a ^ symbol on the next line to
        highlight the location of the error.
        """
        error_location = self.file.tell()
        self.file.seek(0, 0)
        if self.char_counter == 0:
            if self.line_counter != 1:
                self.line_counter -= 1
                line_text = self.file.read().split("\n")[self.line_counter - 1]
                self.char_counter = self.char_in_line[-1]
            else:  # if the file is an empty file
                line_text = ""
        else:
            line_text = self.file.read().split("\n")[self.line_counter - 1]
        output = (
            _("Error on line ")
            + str(self.line_counter)
            + "\n"
            + line_text
            + "\n"
            + " " * (self.char_counter - 1)
            + "^"
        )

        self.file.seek(0, 0)
        self.line_counter = 1
        self.char_counter = 0
        for i in range(error_location):
            self._advance()
        return output

    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""
        symbol = Symbol()
        self._skip_spaces()

        # if symbol is a name
        if self.current_character.isalpha():
            if (
                self.afterdot is True
                and self.current_character in self.keywords_list
            ):
                self.afterdot = False
                symbol.type = self.KEYWORD
                symbol.id = self.I_ID
                self._advance()
            else:
                name_string = self._get_name()
                self.afterdot = False
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
            self.afterdot = False
            symbol.id = self._get_number()
            symbol.type = self.NUMBER

        # if symbol is a dot
        elif self.current_character == ".":
            self.afterdot = True
            symbol.type = self.DOT
            self._advance()

        # if symbol is a comma
        elif self.current_character == ",":
            self.afterdot = False
            symbol.type = self.COMMA
            self._advance()

        # if symbol is a semicolon
        elif self.current_character == ";":
            self.afterdot = False
            symbol.type = self.SEMICOLON
            self._advance()

        # if symbol is a equals
        elif self.current_character == "=":
            self.afterdot = False
            symbol.type = self.EQUALS
            self._advance()

        # if symbol is an arrow
        elif self.current_character == ">":
            self.afterdot = False
            symbol.type = self.ARROW
            self._advance()

        # if symbol is an openbracket
        elif self.current_character == "(":
            self.afterdot = False
            symbol.type = self.OPENBRACKET
            self._advance()

        # if symbol is an closedbracket
        elif self.current_character == ")":
            self.afterdot = False
            symbol.type = self.CLOSEDBRACKET
            self._advance()

        # if symbol is the end of file
        elif self.current_character == "":
            symbol.type = self.EOF

        # if symbol is a hashtag - comment
        elif self.current_character == "#":
            while True:
                self._advance()
                if (
                    self.current_character == "\n"
                    or self.current_character == ""
                ):
                    break
            return self.get_symbol()

        # if symbol is an invalid character
        else:
            self._advance()
        return symbol
