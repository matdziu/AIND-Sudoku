assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    row_units_list = [cross(r, cols) for r in rows]
    col_units_list = [cross(rows, c) for c in cols]
    square_units_list = [cross(rs, cs) for rs in ['ABC', 'DEF', 'GHI'] for cs in ['123', '456', '789']]

    for row_unit in row_units_list:
        row_unit_dict_reduced = naked_twins_for_unit(dict([(box, values[box]) for box in row_unit]))
        for box, value in row_unit_dict_reduced.items():
            values[box] = value

    for col_unit in col_units_list:
        col_unit_dict_reduced = naked_twins_for_unit(dict([(box, values[box]) for box in col_unit]))
        for box, value in col_unit_dict_reduced.items():
            values[box] = value

    for square_unit in square_units_list:
        square_unit_dict_reduced = naked_twins_for_unit(dict([(box, values[box]) for box in square_unit]))
        for box, value in square_unit_dict_reduced.items():
            values[box] = value

    return values


def naked_twins_for_unit(unit_dict_input):
    unit_dict_output = unit_dict_input.copy()
    # Find all instances of naked twins
    potential_naked_twins = dict(
        [(box, unit_dict_input[box]) for box in unit_dict_input.keys() if len(unit_dict_input[box]) == 2])

    potential_naked_twins_occurrences = {}
    for box, value in potential_naked_twins.items():
        potential_naked_twins_occurrences[value] = potential_naked_twins_occurrences.get(value, [])
        potential_naked_twins_occurrences[value].append(box)

    naked_twins_values \
        = [value for value, boxes in potential_naked_twins_occurrences.items() if len(boxes) == 2]

    naked_twins_occurrences = dict([(value, potential_naked_twins_occurrences[value]) for value in naked_twins_values])

    # Eliminate the naked twins as possibilities for their peers
    for naked_twin_value in naked_twins_occurrences.keys():
        for digit in naked_twin_value:
            for key, value in unit_dict_input.items():
                if key not in naked_twins_occurrences[naked_twin_value]:
                    unit_dict_output[key] = value.replace(digit, '')

    if unit_dict_input != unit_dict_output:
        naked_twins_for_unit(unit_dict_output)
    else:
        return unit_dict_output


def cross(A, B):
    return [a + b for a in A for b in B]


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    pass


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    pass


def eliminate(values):
    pass


def only_choice(values):
    pass


def reduce_puzzle(values):
    pass


def search(values):
    pass


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
