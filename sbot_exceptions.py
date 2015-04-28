import random

class SBotException(Exception):
    """Superclass for SBot exceptions."""
    pass

# Command error feedback, the {cmd} fields get replaced with the triggering command via str.format()
command_errors = ["""Man I wish I knew how to process {cmd}, but I'm pretty dumb.
Try again? Or you could ask for HELP.""",
                  "Mm...no. {cmd} doesn't make any sense to me. You sure you don't need any HELP?",
                  """Huh. I punched in {cmd} like you told me to and all I got was a picture
                  of the command prompt with the word HELP typed in. Useless."""]

def choose_from(stuff):
    """Simple function for semi-randomizing text responses from a set list (defined above)."""
    return random.choice(stuff)


class CommandError(SBotException):
    """Handles commands that module main menus can't interpret."""
    def __init__(self, invalid_command):
        self.command = invalid_command
        
    def __str__(self):
        if self.command.istitle():
            return "Sorry love, it's casuals only in here. Use lowercase commands next time."
        elif self.command.isupper():
            return "Ahhh! Jeez, whatcha yelling at me for? Lowercase will do just fine, thanks."
        else:
            return choose_from(command_errors).format(cmd = "\"" + self.command + "\"")

    @property
    def command(self):
        return self.command


class LoadUserError(SBotException):
    """Handles failure to load a .txt file as a user file."""
    def __init__(self, user_file):
        self.file = user_file

    def __str__(self):
        return "Error loading user profile: \"" + self.file + "\" is not a valid user file."


class NestedListIndexError(SBotException):
    """Handles entering of invalid indices when editing nested lists in ToDo."""
    def __init__(self, invalid_index):
        self.index = invalid_index

    def __str__(self):
        return "The entered line number: " + self.index + " doesn't exist!"
