import re

# A dictionary to store variables
variables = {}

def evaluate_expression(expr):
    """Evaluates expressions involving operators and variables."""
    expr = expr.strip()

    # Check if the expression is a simple variable (like 'message')
    if expr.isalpha():  # If it's a simple variable name (no spaces, just letters)
        return variables.get(expr, None)  # Return the value of the variable or None if not found
    
    # Check if the expression is a string enclosed in quotes (like "HELLO!")
    if expr.startswith('"') and expr.endswith('"'):
        return expr[1:-1]  # Return the string without quotes

    # If the expression looks like a literal value (e.g., HELLO!)
    if re.match(r'^[A-Za-z0-9!]+$', expr):  # Matches words like HELLO! without quotes
        return expr

    # Replace variables with their values
    for var, value in variables.items():
        expr = expr.replace(var, str(value))

    try:
        return eval(expr)
    except:
        return None

def execute_command(command):
    """Executes a single command."""
    global variables

    # Handling SET command
    set_pattern = r"SET (\w+) = (.+)"
    match = re.match(set_pattern, command)
    if match:
        var_name = match.group(1)
        value_expr = match.group(2)
        
        # Evaluate the value expression
        value = evaluate_expression(value_expr)
        
        if value is not None:
            variables[var_name] = value
        else:
            print(f"Error: Invalid value expression for SET {command}")
        return

    # Handling PRINT command (with variables and operators)
    if command.startswith("PRINT "):
        if command.startswith('PRINT ['):
            # Print direct text (e.g., PRINT [Hello])
            print(command[7:-1])  # Strip [ and ]
        else:
            # Print evaluated expression (e.g., variables, arithmetic)
            var_name_or_expr = command[6:].strip()
            result = evaluate_expression(var_name_or_expr)
            if result is not None:
                print(result)
            else:
                print(f"Error: Invalid expression in PRINT {command}")
        return

    # Handling INPUT command (captures user input and assigns it to a variable)
    input_pattern = r"INPUT (\w+) \[(.*?)\]"
    match = re.match(input_pattern, command)
    if match:
        var_name = match.group(1).strip()
        prompt = match.group(2).strip()
        
        # Ask the user for input and show the prompt
        user_input = input(f"{prompt} ")
        
        # Store the user input in the specified variable
        variables[var_name] = int(user_input)  # Convert the input to an integer

        return  # Input is captured and stored as a variable

    # Handling IF-ELSE command (conditional logic based on the 'age' variable)
    if "IF " in command and "THEN" in command and "ELSE" in command:
        # Extract the command parts for conditional evaluation
        condition_expr = re.search(r"IF (.+?) THEN", command).group(1).strip()
        then_part = re.search(r"THEN (.*?) ELSE", command).group(1).strip()
        else_part = re.search(r"ELSE (.*)", command).group(1).strip()

        condition_result = evaluate_expression(condition_expr)
        
        # Remove the "PRINT" part and strip the brackets
        if condition_result:
            # Remove "PRINT " and brackets [] around the string
            print(then_part[1:-1] if then_part.startswith('[') and then_part.endswith(']') else then_part)
        else:
            # Remove "PRINT " and brackets [] around the string
            print(else_part[1:-1] if else_part.startswith('[') and else_part.endswith(']') else else_part)

        return

    # Handling LOOP command (for inline loops like LOOP 5 PRINT [Hello])
    loop_pattern = r"LOOP (\d+) (.+)"
    match = re.match(loop_pattern, command)
    if match:
        loop_count = int(match.group(1))
        command_to_execute = match.group(2).strip()

        for _ in range(loop_count):
            execute_command(command_to_execute)
        return

def process_input(input_text):
    """Process the input script."""
    commands = input_text.splitlines()  # Split by newlines to get individual commands
    for command in commands:
        command = command.strip()
        if command:
            execute_command(command)

# Main loop to accept input from user
if __name__ == "__main__":
    print("Welcome to the Turing Complete Language! Type 'exit' to quit.")
    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            break
        process_input(user_input)
