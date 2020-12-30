"""
Advent of code 2020, day 16
---------------------------

As you're walking to yet another connecting flight, you realize that one of the
legs of your re-routed trip coming up is on a high-speed train. However, the
train ticket you were given is in a language you don't understand. You should
probably figure out what it says before you get to the train station after the
next flight. Unfortunately, you can't actually read the words on the ticket.
You can, however, read the numbers, and so you figure out the fields these
tickets must have and the valid ranges for values in those fields.

You collect the rules for ticket fields, the numbers on your ticket, and the
numbers on other nearby tickets for the same train service (via the airport
security cameras) together into a single document you can reference (your
puzzle input).

The rules for ticket fields specify a list of fields that exist somewhere on
the ticket and the valid ranges of values for each field. For example, a rule
like "class: 1-3 or 5-7" means that one of the fields in every ticket is named
class and can be any value in the ranges 1-3 or 5-7 (inclusive, such that 3 and
5 are both valid in this field, but 4 is not).

Each ticket is represented by a single line of comma-separated values. The
values are the numbers on the ticket in the order they appear; every ticket has
the same format. For example, consider this ticket:

.--------------------------------------------------------.
| ????: 101    ?????: 102   ??????????: 103     ???: 104 |
|                                                        |
| ??: 301  ??: 302             ???????: 303      ??????? |
| ??: 401  ??: 402           ???? ????: 403    ????????? |
'--------------------------------------------------------'

Here, ? represents text in a language you don't understand. This ticket might
be represented as 101,102,103,104,301,302,303,401,402,403; of course, the
actual train tickets you're looking at are much more complicated. In any case,
you've extracted just the numbers in such a way that the first number is always
the same specific field, the second number is always a different specific
field, and so on - you just don't know what each position actually means!
"""
import re


def solve_part1(puzzle_input):
    """Solve part 1 of today's puzzle.

    Start by determining which tickets are completely invalid; these are
    tickets that contain values which aren't valid for any field. Ignore your
    ticket for now.

    Consider the validity of the nearby tickets you scanned. What is your
    ticket scanning error rate?

    Examples
    --------
    Suppose you have the following notes:

    >>> puzzle_input = '''class: 1-3 or 5-7
    ...                row: 6-11 or 33-44
    ...                seat: 13-40 or 45-50
    ...
    ...                your ticket:
    ...                7,1,14
    ...
    ...                nearby tickets:
    ...                7,3,47
    ...                40,4,50
    ...                55,2,20
    ...                38,6,12'''

    It doesn't matter which position corresponds to which field; you can
    identify invalid nearby tickets by considering only whether tickets contain
    values that are not valid for any field. Adding together all of the invalid
    values produces your ticket scanning error rate: 4 + 55 + 12 = 71.

    >>> solve_part1(puzzle_input)
    71

    Parameters
    ----------
    puzzle_input : str
        The puzzle input provided by the Advent of Code website.

    Returns
    -------
    error_rate : int
        The answer to part 1 of the puzzle.
    """
    # We ignore our ticket for now
    rules, _, nearby_tickets = parse_puzzle_input(puzzle_input)

    # Compute total error rate for all tickets
    error_rate = 0
    for ticket in nearby_tickets:
        # Find all numbers in a ticket that do not satify any of the rules.
        invalid_values = (value for value in ticket
                          if not any(rule.is_valid(value) for rule in rules))
        error_rate += sum(invalid_values)
    return error_rate


def solve_part2(puzzle_input):
    """Solve part 2 of today's puzzle.

    Once you work out which field is which, look for the six fields on your
    ticket that start with the word departure. What do you get if you multiply
    those six values together?

    Parameters
    ----------
    puzzle_input : str
        The puzzle input provided by the Advent of Code website.

    Returns
    -------
    product_of_departure_fields : int
        The answer to part 2 of the puzzle.
    """
    decyphered_ticket = decypher_ticket(puzzle_input)

    # Look for the six fields on your ticket that start with the word
    # departure. What do you get if you multiply those six values together?
    product_of_departure_fields = 1
    for field_name, field_value in decyphered_ticket.items():
        if field_name.startswith('departure'):
            product_of_departure_fields *= field_value
    return product_of_departure_fields


class Rule:
    """
    Parameters
    ----------
    rule_str : str
        The string representation of the rule as given in the puzzle input.
    """
    # Regular expression used to parse the string representation of a rule.
    # It matches substrings such as:
    #     class: 1-3 or 5-7
    #     row: 6-11 or 33-44
    #     seat: 13-40 or 45-50
    #     departure time: 46-147 or 153-958
    pattern = re.compile(r'\s*([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)\s*')

    @staticmethod
    def __init__(self, rule_str):
        match = Rule.pattern.search(rule_str)
        self.name, from1, to1, from2, to2 = match.groups()

        # Ranges in the puzzle input are end-inclusive.
        # Python ranges are end-exclusive, so we need to add one.
        self.valid_range1 = range(int(from1), int(to1) + 1)
        self.valid_range2 = range(int(from2), int(to2) + 1)

    def is_valid(self, value):
        """Checks whether a value adheres to this rule.

        For a value to be valid, it needs to be part of either of the
        valid value ranges of this rule.

        Parameters
        ----------
        value : int
            The value to check against this rule.

        Returns
        -------
        is_valid : bool
            Whether the given value is valid according to this rule.
        """
        return value in self.valid_range1 or value in self.valid_range2


def parse_puzzle_input(puzzle_input):
    """Parse the puzzle input into convenient Python data structures.

    Parameters
    ----------
    puzzle_input : str
        The puzzle input provided by the Advent of Code website.

    Returns
    -------
    rules : list of Rule
        The rules given at the top of the puzzle input.
    your_ticket : list of int
        The values written on your ticket.
    nearby_ticket : list of list of int
        For each nearby ticket, the values written on that ticket.
    """
    rules_str, your_ticket_str, nearby_tickets_str = puzzle_input.split('\n\n')

    # Parse all the rules
    rules = [Rule(line) for line in rules_str.split('\n')]

    # Parse lines such as:
    #     your ticket:
    #     7,1,14
    _, ticket_numbers_str = your_ticket_str.split('your ticket:')
    your_ticket = [int(num) for num in ticket_numbers_str.split(',')]

    # Parse lines such as:
    #     nearby tickets:
    #     7,3,47
    #     40,4,50
    #     55,2,20
    nearby_tickets = list()
    for ticket_numbers_str in nearby_tickets_str.strip().split('\n')[1:]:
        ticket = [int(num) for num in ticket_numbers_str.split(',')]
        nearby_tickets.append(ticket)

    return(rules, your_ticket, nearby_tickets)


def decypher_ticket(puzzle_input):
    """Convert the puzzle input into a decyphered train ticket.

    Now that you've identified which tickets contain invalid values, discard
    those tickets entirely. Use the remaining valid tickets to determine which
    field is which.

    Using the valid ranges for each field, determine what order the fields
    appear on the tickets. The order is consistent between all tickets: if seat
    is the third field, it is the third field on every ticket, including your
    ticket.

    Examples
    --------
    Suppose you have the following notes:

    >>> puzzle_input = '''class: 0-1 or 4-19
    ...                   row: 0-5 or 8-19
    ...                   seat: 0-13 or 16-19
    ...
    ...                   your ticket:
    ...                   11,12,13
    ...
    ...                   nearby tickets:
    ...                   3,9,18
    ...                   15,1,5
    ...                   5,14,9'''

    Based on the nearby tickets in the above example, the first position must
    be row, the second position must be class, and the third position must be
    seat; you can conclude that in your ticket, class is 12, row is 11, and
    seat is 13.

    >>> decypher_ticket(puzzle_input)
    {'row': 11, 'class': 12, 'seat': 13}
    """
    rules, your_ticket, nearby_tickets = parse_puzzle_input(puzzle_input)

    # Discard all invalid tickets.
    def is_valid(ticket):
        """Are all the values in a ticket valid according to any rule?"""
        return all(any(rule.is_valid(value) for value in ticket)
                   for rule in rules)
    nearby_tickets = filter(is_valid, nearby_tickets)

    # Collect all observed values for each field.
    observed_fields_values = zip(*nearby_tickets)

    # For each field, find all the names that it could potentially have.
    # The rule list at the start of the puzzle input gives us the valid ranges
    # associated with a name. If all the observed values for a field fall
    # within these valid ranges, the corresponding name is a potential name for
    # the field. We collect the (field_num -> potential_names) pairs in a
    # dictionary, because this datastructure will be convenient later on.
    potential_fields_names = dict()
    for field_num, observed_values in enumerate(observed_fields_values):
        potential_names = set(rule.name for rule in rules
                              if all(rule.is_valid(value)
                                     for value in observed_values))
        potential_fields_names[field_num] = potential_names

    # The decyphered ticket is a dictionary: field_name -> field_value
    decyphered_ticket = dict()

    # Start decyphering our ticket by assigning names to each field.
    # We can assign a name to a field whenever the field has only one potential
    # field name.
    unassigned_field_names = set(rule.name for rule in rules)
    while len(unassigned_field_names) > 0:
        # Find a field with only one potential name
        for field_num, potential_names in potential_fields_names.items():
            if len(potential_names) == 1:
                break

        # Now we know the name of this field, so we can decypher it.
        assigned_name = potential_names.pop()
        decyphered_ticket[assigned_name] = your_ticket[field_num]

        # Remove the assigned field name from the list of potential
        # names for all fields.
        for other_potential_names in potential_fields_names.values():
            try:
                other_potential_names.remove(assigned_name)
            except KeyError:
                # assigned_name was not part of the other_potential_names set
                # and that's ok.
                pass

        # We're done with this field.
        unassigned_field_names.remove(assigned_name)

    return decyphered_ticket


# When the script is run as `python day16.py`, solve the puzzle using the real
# puzzle input.
if __name__ == '__main__':
    with open('day16_input.txt') as f:
        puzzle_input = f.read()
    print('Part 1:', solve_part1(puzzle_input))
    print('Part 2:', solve_part2(puzzle_input))
