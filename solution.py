assignments = []


def cross(A, B):
    return [a + b for a in A for b in B]


rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units_list = [cross(r, cols) for r in rows]
col_units_list = [cross(rows, c) for c in cols]
square_units_list = [cross(rs, cs) for rs in ['ABC', 'DEF', 'GHI'] for cs in ['123', '456', '789']]
diagonal_units_list = [[row + col for row, col in zip(rows, cols)],
                       [row + col for row, col in zip(rows, reversed(cols))]]
all_units_list = row_units_list + col_units_list + square_units_list + diagonal_units_list

units = dict((box, [unit for unit in all_units_list if box in unit]) for box in boxes)
peers = dict((box, set(sum(units[box], [])) - {box}) for box in boxes)


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

    for unit in all_units_list:
        unit_dict_reduced = naked_twins_for_unit(dict([(box, values[box]) for box in unit]))
        for box, value in unit_dict_reduced.items():
            assign_value(values, box, value)

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
            for key, value in unit_dict_output.items():
                if key not in naked_twins_occurrences[naked_twin_value]:
                    assign_value(unit_dict_output, key, value.replace(digit, ''))

    if unit_dict_input != unit_dict_output:
        return naked_twins_for_unit(unit_dict_output)
    else:
        return unit_dict_output


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
    grid_not_empty = []
    for value in grid:
        if value == '.':
            grid_not_empty.append('123456789')
        else:
            grid_not_empty.append(value)

    return dict(zip(boxes, grid_not_empty))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """

    width = 1 + max([len(values[box]) for box in boxes])
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    single_value_boxes = [box for box in boxes if len(values[box]) == 1]

    for single_value_box in single_value_boxes:
        single_value = values[single_value_box]
        for peer_box in peers[single_value_box]:
            assign_value(values, peer_box, values[peer_box].replace(single_value, ''))

    return values


def only_choice(values):
    for unit in all_units_list:
        for digit in '123456789':
            digit_occurrences = [box for box in unit if digit in values[box]]
            if len(digit_occurrences) == 1:
                assign_value(values, digit_occurrences[0], digit)

    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    reduced_values = reduce_puzzle(values)
    if reduced_values is False:
        return False
    if all(len(reduced_values[box]) == 1 for box in boxes):
        return reduced_values
    unsolved_values = [(len(reduced_values[box]), box) for box in reduced_values.keys() if len(reduced_values[box]) > 1]
    optimal_box = min(unsolved_values)[1]
    for digit in reduced_values[optimal_box]:
        reduced_values_copy = reduced_values.copy()
        reduced_values_copy[optimal_box] = digit
        return search(reduced_values_copy)


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))


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
