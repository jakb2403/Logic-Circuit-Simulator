"""Read the circuit definition file and translate the characters into symbols.

Used in the Logic Simulator project to read the characters in the definition
file and translate them into symbols that are usable by the parser.

Classes
-------
Scanner - reads definition file and translates characters into symbols.
Symbol - encapsulates a symbol and stores its properties.
"""


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
        self.names = names
        self.symbol_type_list = [
            self.COMMA,
            self.SEMICOLON,
            self.EQUALS,
            self.DOT,
            self.OPENBRACKET,
            self.CLOSEDBRACKET,
            self.OPENCURLYBRACKET,
            self.CLOSEDCURLYBRACKET,
            self.ARROW,
            self.KEYWORD,
            self.DEVICE_ARG,
            self.DEVICE,
            self.DTYPE_IP,
            self.DTYPE_OP,
            self.NUMBER,
            self.NAME,
            self.EOF] = range("""number""")  # feel free to change the names,
        # esp. bracket stuff names, but I can't think of a good name
        # tell us whether MON and I are keywords
        # do we also need END as a keyword?
        self.keywords_list = ["DEVICES", "CONNECT", "MONITOR", "MON", "I"]
        self.device_arg_list = ["CLOCK", "AND", "NAND", "OR", "NOR", "SWITCH"]
        self.device_list = ["DTYPE", "XOR"]
        self.dtype_ip_list = ["SET", "CLEAR", "DATA", "CLK"]
        self.dtype_op_list = ["Q", "QBAR"]

    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""
