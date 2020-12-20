"""
Advent of code 2020, day 1
--------------------------

The Elves in accounting just need you to fix your expense report (your puzzle
input); apparently, something isn't quite adding up.
"""
from itertools import combinations


def solve_part1(puzzle_input):
    """Solve part 1 of today's puzzle.

    Find the two entries that sum to 2020; what do you get if you multiply them
    together?
    """

    # We need quick lookups, so we store the expense report as a set.
    expense_report = set(int(entry) for entry in puzzle_input.split())

    for entry1 in expense_report:
        # This is the entry that needs to be in the expense report if the two
        # are to sum to 2020.
        entry2 = 2020 - entry1
        if entry2 in expense_report:
            return entry1 * entry2


def solve_part2(puzzle_input):
    """Solve part 2 of today's puzzle.

    In your expense report, what is the product of the three entries that sum
    to 2020?
    """

    # For three entries to sum to 2020, they must be relatively small. We will
    # find the solution much faster if we try the entries in ascending order.
    expense_report = sorted(int(entry) for entry in puzzle_input.split())

    n_iter = 0
    for entry1, entry2, entry3 in combinations(expense_report, 3):
        n_iter += 1
        if entry1 + entry2 + entry3 == 2020:
            print(n_iter)
            return entry1 * entry2 * entry3


def test_part1():
    """Run the test cases for part1 given in the puzzle description."""

    # In this list, the two entries that sum to 2020 are 1721 and 299.
    # Multiplying them together produces 1721 * 299 = 514579, so the correct
    # answer is 514579.
    assert solve_part1('''1721
                          979
                          366
                          299
                          675
                          1456''') == 514579


def test_part2():
    """Run the test cases for part2 given in the puzzle description."""

    # Using the above example again, the three entries that sum to 2020 are
    # 979, 366, and 675. Multiplying them together produces the answer,
    # 241861950.
    assert solve_part2('''1721
                          979
                          366
                          299
                          675
                          1456''') == 241861950


# When the script is run as `python day01.py`, solve the puzzle using the real
# puzzle input.
if __name__ == '__main__':
    with open('day1_input.txt') as f:
        puzzle_input = f.read()
    print('Part 1:', solve_part1(puzzle_input))
    print('Part 2:', solve_part2(puzzle_input))
