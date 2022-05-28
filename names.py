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
        if name_string not in self.names_list:
            raise ValueError("Invalid name_string. Couldn't find that name.")
        if name_string in self.names_list:
            return self.names_list[name_string]
        else:
            return None


    def lookup(self, name_string):
        """Return the corresponding name ID for the given name_string.

        If the name string is not present in the names list, add it.
        """

        if type(name_string) == list:
            for name in name_string:
                if name_string in self.names_list:
                    return self.names_list.index(name_string)
                else:
                    if not(name_string[0].isalpha()):
                        raise TypeError("Name string must start with a letter, not a number.")
                    self.names_list.append(name_string)
                    return len(self.names_list) - 1

        else: 
            if name_string in self.names_list:
                return self.names_list.index(name_string)
            else:
                if not(name_string[0].isalpha()):
                    raise TypeError("Name string must start with a letter, not a number.")
                self.names_list.append(name_string)
                return len(self.names_list) - 1

    def get_name_string(self, name_id):
        """Return the corresponding name string for the given name_id.

        If the name ID is not a valid index into the names list, return None.
        """
        if name_id < 0:
            raise ValueError("Invalid name_id. Only positive integers allowed.")
        if name_id < len(self.names_list):
            return self.names_list[name_id]
        else:
            return None