import csv
def read_csv_to_dicts(filepath, encoding="utf-8", newline="", delimiter=","):
    """Accepts a file path, creates a file object, and returns a list of dictionaries that
    represent the row values using the cvs.DictReader().

    WARN: This function must be implemented using a list comprehension in order to earn points.

    Parameters:
        filepath (str): path to file
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values

    Returns:
        list: nested dictionaries representing the file contents
    """

    with open(filepath, "r", newline=newline, encoding=encoding) as file_obj:
        return [line for line in csv.DictReader(file_obj, delimiter=delimiter)]

def to_float(value):
    """
    Converts the given value to a float.

    Args:
        value (str): The value to be converted to float.

    Returns:
        float or None: The converted float value if successful, None otherwise.
    """
    try:
        return float(r_c_w_p(value))
    except ValueError:
        return None

def to_int(value):
    """
    Converts the given value to an integer.

    Args:
        value (str): The value to be converted.

    Returns:
        int or None: The converted integer value, or None if the conversion fails.
    """
    try:
        return int(to_float(r_c_w_p(value)))
    except:
        return None
    
def r_c_w_p(input_string):
    """
    Replaces all occurrences of ',' with '.' in the input string.

    Args:
        input_string (str): The input string to be processed.

    Returns:
        str: The input string with all occurrences of ',' replaced by '.'.
    """
    return input_string.replace(',', '.')

def clean_string(input_string):
    """
    Cleans the input string by removing leading and trailing whitespace.

    Args:
        input_string (str): The string to be cleaned.

    Returns:
        str: The cleaned string with leading and trailing whitespace removed.
    """
    r_c_w_p(input_string)
    return input_string.strip()

def get_priority_input(prompt):
    """
    Prompts the user to enter a priority value between 0 and 1.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        float: The priority value entered by the user.

    Raises:
        ValueError: If the user enters an invalid input (not a number).

    """
    while True:
        try:
            value = float(input(prompt))
            if 0 <= value <= 1:
                return value
            else:
                print("Please enter a value between 0 and 1.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_distance_input(prompt):
    """
    Prompts the user to enter a positive number and returns the value.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        float: The positive number entered by the user.

    Raises:
        ValueError: If the user enters an invalid input (not a number).
    """
    while True:
        try:
            value = float(input(prompt))
            if value >= 0:
                return value
            else:
                print("Please enter a positive value.")
        except ValueError:
            print("Invalid input. Please enter a number.")