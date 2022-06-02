"""Map variable names and string names to unique integers.

Used in the Logic Simulator project. Most of the modules in the project
use this module either directly or indirectly.

Classes
-------
Names - maps variable names and string names to unique integers.
"""


class Names:

    """Map variable names and string names to unique integers.

    This class deals with storing grammatical keywords and user-defined words,
    and their corresponding name IDs, which are internal indexing integers. It
    provides functions for looking up either the name ID or the name string.
    It also keeps track of the number of error codes defined by other classes,
    and allocates new, unique error codes on demand.

    Parameters
    ----------
    No parameters.

    Public methods
    -------------
    unique_error_codes(self, num_error_codes): Returns a list of unique integer
                                               error codes.

    query(self, name_string): Returns the corresponding name ID for the
                        name string. Returns None if the string is not present.

    lookup(self, name_string_list): Returns a list of name IDs for each
                        name string. Adds a name if not already present.

    get_name_string(self, name_id): Returns the corresponding name string for
                        the name ID. Returns None if the ID is not present.
    """

    def __init__(self):
        """Initialise names list."""
        self.names_list = []
        self.error_code_count = 0  # how many error codes have been declared

    def unique_error_codes(self, num_error_codes):
        """Return a list of unique integer error codes."""
        if not isinstance(num_error_codes, int):
            raise TypeError("Expected num_error_codes to be an integer.")
        self.error_code_count += num_error_codes
        return range(self.error_code_count - num_error_codes,
                     self.error_code_count)

    def query(self, name_string):
        """Return the corresponding name ID for name_string.

        If the name string is not present in the names list, return None.
        """

        if name_string in self.names_list:
            return self.names_list.index(name_string)
        else:
            return None

    def lookup(self, name_input):
        """Return the corresponding name ID for the given name_string.
        If the name string is not present in the names list, add it.
        """
        if type(name_input) == list:
            output_list = []
            # iterate through name_strings in list and perform lookup
            for item in name_input:
                if item in self.names_list:
                    output_list.append(self.names_list.index(item))
                else:
                    if not(item[0].isalpha()):
                        raise TypeError(
                            "Name string must start with a letter, not a number.")
                    else:
                        self.names_list.append(item)
                        output_list.append(len(self.names_list) - 1)

            return output_list
        elif type(name_input) == str:
            # perform lookup for 1 name_string item
            if name_input in self.names_list:
                return self.names_list.index(name_input)
            else:
                if not(name_input[0].isalpha()):
                    raise TypeError(
                        "Name string must start with a letter, not a number.")
                self.names_list.append(name_input)
                return len(self.names_list) - 1
        else:
            raise TypeError("Expect list or string for name_input.")

    def get_string(self, name_id):
        """Return the corresponding name string for the given name_id.

        If the name ID is not a valid index into the names list, return None.
        """
        if type(name_id) == int:
            if name_id < 0:
                raise ValueError(
                    "Invalid name_id. Only positive integers allowed.")
            if name_id < len(self.names_list):
                return self.names_list[name_id]
            else:
                return None
        else:
            raise TypeError("Expect integer for name_id")
