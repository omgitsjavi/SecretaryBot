# Simple calculator module

# init
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
            output = """Type in expressions normally and hit enter.
You can use an underscore "_" to reference the last calculated result."""

        # Evaluates the entered expression as if it were typed as Python code.
        # Clunky and potentially dangerous, but it works.
        else:
            output = eval(entered)
            # Saves result to memory variable
            _ = output

