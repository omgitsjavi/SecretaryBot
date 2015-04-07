# Simple calculator module

help_text = """Type in expressions normally and hit enter.
You can use an underscore "_" to reference the last calculated result."""

def calculator():
    output = "Welcome to the calculator. QUIT at any time."
    # Variable for last calculation result
    _ = None
    run = True
    while run:
        print "\n", output
        entered = raw_input('CALC> ')

        # QUIT to menu
        if entered == "quit":
            run = False
            
        # HELP documentation
        elif entered == "help":
            output = help_text

        # Evaluates the entered expression by parsing the string.
        # Clunky with int and float typing, but it works.
        else:
            output = eval(entered)
            # Saves result to memory variable
            _ = output

