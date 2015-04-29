"""User management module.

Data is stored in the format [[Username, ...],[...]]
"""

import json
from os import rename
from time import sleep
from sbot_exceptions import *

help_text = """Currently an empty WIP, soon you'll be able to CHANGE NAME.
Future options may include the ability to reset user data."""

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
            # Save new user's name
            # Format is nested dictionary, User[module][data_item] = data_value
            save_data = {'user': {'name': self.name}}

            # Write to text file
            json.dump(save_data, new_file)
            
        return "New profile \"" + self.name + "\" created!"

def create_new_user(name):
    """Creates a new user instance and data file, returns instance and result."""
    new_user = User(name)
    result = new_user.create_new_user_file()
    return [new_user, result]

def init_user(user_file):
    """Loads up a User instance based on their save file."""
    with open(user_file, 'r') as file:
        user_data = json.load(file)
    return User(user_data['user']['name'])

# User Management module accessed via main menu
def user_management(active_user):
    """User management module. Returns True if an operation requires a restart."""
    
    output = "Welcome to User Management, {user}.".format(user=active_user.name) +\
"\nCHANGE NAME    NEW USER    QUIT to main menu"
    run = True

    while run:
        print output, "\n"
        entered = raw_input('USERS> ')

        # QUIT to menu
        if entered == "quit":
            return False

        # HELP documentation
        elif entered == "help":
            output = help_text

        # CHANGE NAME
        elif entered == "change name":
            file_to_change = active_user.name + ".txt"
            # Prompt for new name
            print "Fancy a change, eh? Choose your new name."
            new_name = raw_input('Name> ')

            # Process changes in save file
            with open(file_to_change, 'r') as user_file:
                user_data = json.load(user_file)
                user_data['user']['name'] = new_name
            with open(file_to_change, 'w') as user_file:
                json.dump(user_data, user_file)
            # Rename save file
            rename(file_to_change, new_name + ".txt")
            print "Name change successful!\n"
            sleep(2.0)
            # Indicate need for program restart
            return True

        # NEW USER creation
        elif entered == "new user":
            # Prompt for new user's name and create
            print "Choose a name! Names are case sensitive and can be changed later."
            new_user_name = raw_input('Name> ')
            user_creation = create_new_user(new_user_name)
            print user_creation[1], "\n"

            # Indicate need for program restart
            return True

        # Invalid input
        else:
            print CommandError(entered), "\n"
