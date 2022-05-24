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
        self.symbol_type_list = [self.COMMA, self.SEMICOLON, self.EQUALS, 
        self.KEYWORD, self.NUMBER, self.NAME, self.EOF] = range(7)
        #PLEASE tell us whether MON and I are keywords
        self.keywords_list = ["DEVICES", "CONNECT", "MONITOR", "DTYPE", "XOR", 
        "CLOCK", "AND", "NAND", "OR", "NOR", "MON", "I", "DATA", "CLK", "SET", 
        "CLEAR", "Q", "QBAR"] 

    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""
