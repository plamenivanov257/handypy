"""
Contains some useful CLI tools.
"""
from termcolor import cprint


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

    while not success:
        user_input = input(f"{message} (default is {default}) ")

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


class CLIMenu:
    """
    Command-line menu with numbered choices.
    """
    done = False
    actions = []
    actions_fns = []
    item_suffix = "   "

    def run_menu(self, input_prompt="Choose an action:"):
        """
        Displays the menu and prompts the user to make a choice.
        """
        menu_str = f"{input_prompt}\n"
        for i in range(len(self.actions)):
            menu_str += f"{self.item_suffix}{i}: {self.actions[i]}\n"

        while not self.done:
            try:
                choice = int(input(menu_str))
            except ValueError:
                continue
            try:
                self.actions_fns[choice]()
            except KeyboardInterrupt:
                cprint("\nCaught a KeyboardInterrupt, returning to menu...\n", "red")

    def add_option(self, action : str, action_fn):
        """
        Adds an action to the list of choices.
        """
        self.actions.append(action)
        self.actions_fns.append(action_fn)

    def _exit_menu(self):
        self.done = True

    def __init__(self, builtin_exit=True, item_suffix="   "):
        self.item_suffix = item_suffix
        if builtin_exit:
            self.actions.append("Exit")
            self.actions_fns.append(self._exit_menu)


def cli_option(action : str, menu : CLIMenu):
    """
    Adds a given function to a CLI menu
    """
    def decor(func):
        menu.actions.append(action)
        menu.actions_fns.append(func)
        return func

    return decor
