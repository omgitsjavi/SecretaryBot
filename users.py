"""User management module.

Data is stored in the format [[Username, ...],[...]]
"""

import json

help_text = """Welcome to User Management. Currently an empty WIP, soon you'll be
able to CHANGE NAME. Future options may include the ability to reset user data."""

class User:
    """Class for user profiles. Each profile saves user data in a text file."""

    def __init__(self, name=""):
        self.name = name

    @property
    def name(self):
        return self.name

    # Note the use of Properties. Just use [user].name = [new_name] to change.
    @name.setter
    def name(self, new_name):
        """For when the user wants to change their name after creation."""
        self.name = new_name

    def create_new_user_file(self, module_list):
        """Writes a new text file for storing user data and returns operation result."""
        # Does nothing if the profile was never named
        if self.name == "":
            return "create_new_user error: unnamed user profile."

        # Otherwise writes a new file titled the profile name
        with open(self.name + ".txt", "w") as new_file:
            # Build nested data list
            save_file = []
            for key in module_list:
                save_file.append([])
                
            # Save new user's name in file
            save_file[0].append(self.name)
            # Write to text file
            json.dump(save_file, new_file)
            
        return "New profile \"" + self.name + "\" created!"

def create_new_user(name, module_list):
    """Creates a new user instance and data file, returns instance and result."""
    new_user = User(name)
    result = new_user.create_new_user_file(module_list)
    return [new_user, result]

# User Management module accessed via main menu
def user_management():
    output = "User management. QUIT at any time."
    run = True

    while run:
        print output, "\n"
        entered = raw_input('USERS> ')

        # QUIT to menu
        if entered == "quit":
            run = False

        # HELP documentation
        elif entered == "help":
            output = help_text

        # CHANGE NAME
        elif entered == "change name":
            output = "Sorry, this feature hasn't been implemented yet!"
