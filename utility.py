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
    try:
        return float(r_c_w_p(value))
    except ValueError:
        return None

def to_int(value):
    try:
        return int(to_float(r_c_w_p(value)))
    except:
        return None
    
def r_c_w_p(input_string):
    return input_string.replace(',', '.')

def clean_string(input_string):
    r_c_w_p(input_string)
    return input_string.strip()

def get_priority_input(prompt):
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
    while True:
        try:
            value = float(input(prompt))
            if value >= 0:
                return value
            else:
                print("Please enter a positive value.")
        except ValueError:
            print("Invalid input. Please enter a number.")