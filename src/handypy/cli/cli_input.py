"""
Defines cli_input which is a fancy terminal string parser.
"""
from termcolor import cprint
import numpy as np



def cli_input(message : str = "Gimme some input:", dtype=None, default=None, parser=None):
    """
    A convenient way to ask the user for some input using the command line

    Args:
        message : str
            A string message that is used as a prompt to the user.
        dtype : data-type
            Data type of the returned type. Used to check if the user's input is valid
            if a parser is not given.
        default
            Default value if the user inputs nothing.
        parser : {function, str}
            The parser is a function that takes a single string argument, the user input,
            and returns a tuple (success, value) where success is True if the user input
            is valid and value is the parsed user input.

            Alternatively, there's a number of standard parsers that can be specified by
            a string. These are "positive" and "negative". To use them, dtype
            must also be specified.

            If parser is None, a simple parser is constructed by trying to cast the user input
            as dtype(user input) and success is set to True if no ValueError exception is raised.
    """

    # Construct parser if none is given
    if parser is None:
        if dtype is None:
            # If no dtype is given, simply return the user input verbatim.
            dtype = str

        if dtype is bool:
            # Bools are a bit annoying...
            message = f"{message} (y for True, anything else for False)"

            def dtype_parser(user_input):
                return True, user_input == 'y'
        else:
            def dtype_parser(user_input):
                try:
                    return True, dtype(user_input)
                except ValueError:
                    cprint(f"Failed parsing {user_input} as {dtype}!", "red")
                    return False, user_input

        parser = dtype_parser

    if isinstance(parser, str) and dtype is None:
        raise ValueError("To use the builtin string-specified parsers, dtype must be specified!")

    if parser == "positive":
        def positive_parser(user_input):
            try:
                value = dtype(user_input)
                if value > 0:
                    return True, value

                cprint("Value must be positive!", "red")
                return False, value
            except ValueError:
                cprint(f"Failed parsing {user_input} as {dtype}!", "red")
                return False, user_input
        parser = positive_parser

    if parser == "negative":
        def negative_parser(user_input):
            try:
                value = dtype(user_input)
                if value < 0:
                    return True, value

                cprint("Value must be negative!", "red")
                return False, value
            except ValueError:
                cprint(f"Failed parsing {user_input} as {dtype}!", "red")
                return False, user_input
        parser = negative_parser


    success = False

    if default is None:
        default_str = ""
    else:
        default_str = f" (default is {default}) "

    while not success:
        user_input = input(f"{message}{default_str}")

        if len(user_input) == 0:
            # Empty input is okay only if default is specified.
            if default is None:
                cprint("Input required!", "red")
                continue

            cprint("Defaulting to", "yellow", end=" ")
            cprint(f"{default}", "yellow", attrs=["bold"])
            return default

        success, value = parser(user_input)

    cprint("Chose", "green", end=" ")
    cprint(f"{value}", "green", attrs=["bold"])
    return value

def select_interval(name: str, sorted_range: np.array, dtype=float):
    """
    Selects the start and the end of an interval contained within a sorted range.
    """

    # just in case
    sorted_range = np.asarray(sorted_range)

    range_min = sorted_range[0]
    range_max = sorted_range[-1]

    print(f"Selecting {name} in range [{range_min}, {range_max}].")
    def in_range(value: dtype):
        value = dtype(value)
        
        if value < range_min:
            cprint(f"Must be at least {range_min}!")
            return False, value

        if value > range_max:
            cprint(f"Must be at most {range_max}!")
            return False, value

        return True, value


    start = cli_input("Start = ", dtype=dtype, parser=in_range, default=range_min)
    end = cli_input("End = ", dtype=dtype, parser=in_range, default=range_max)

    index_start = np.argwhere(sorted_range >= start)[0][0]
    index_end = np.argwhere(sorted_range <= end)[-1][0]

    start = sorted_range[index_start]
    end = sorted_range[index_end]

    return index_start, index_end, start, end
