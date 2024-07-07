"""
Defines the CLIMenu class which is used for making user-friendly CLI scripts.
"""
from termcolor import cprint


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
