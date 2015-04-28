# Simple calculator module
# This import statement makes calc handle int division properly
from __future__ import division

help_text = """A pretty basic arithmetic calculator.
Use +, -, *, /, ** (for exponents), and parenthesis.
Type in expressions normally and hit enter, or QUIT at any time.
You can use an underscore "_" to reference the last calculated result.
"""

def calculator():
    output = "Welcome to the calculator. QUIT at any time."
    # Variable for last calculation result
    _ = 0
    run = True
    while run:
        print output
        entered = raw_input('CALC> ')

        # QUIT to menu
        if entered == "quit":
            break
            
        # HELP documentation
        elif entered == "help":
            output = help_text
            print

        # Evaluates the entered expression by parsing the string.
        # Note that eval() isn't totally safe, as it'll run interpreter
        # functions like help() and quit()
        else:
            try:
                result = eval(entered)
            except (NameError, SyntaxError):
                output = "Can't make sense of that one. Try again!\n"
            except ZeroDivisionError:
                output = "Trying to divide by zero! Can't have that, now can we?\n"
            else:
                # Saves result to memory variable
                _ = result
                output = "\n" + str(result)
