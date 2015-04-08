"""User management module."""

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

    def create_new_user_file(self):
        """Writes a new text file for storing user data and returns operation result."""
        # Does nothing if the profile was never named
        if self.name == "":
            return "create_new_user error: unnamed user profile."

        # Otherwise writes a new file titled the profile name
        with open(self.name + ".txt", "w") as new_file:
            new_file.write(self.name + "\n")
            
        return "New profile \"" + self.name + "\" created!"

def create_new_user(name=""):
    return User(name)

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
