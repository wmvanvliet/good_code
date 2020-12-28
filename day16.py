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
import itertools


def solve_part1(puzzle_input):
    """Solve part 1 of today's puzzle.

    Start by determining which tickets are completely invalid; these are
    tickets that contain values which aren't valid for any field. Ignore your
    ticket for now.

    For example, suppose you have the following notes:

    +----------------------+
    | class: 1-3 or 5-7    |
    | row: 6-11 or 33-44   |
    | seat: 13-40 or 45-50 |
    |                      |
    | your ticket:         |
    | 7,1,14               |
    |                      |
    | nearby tickets:      |
    | 7,3,47               |
    | 40,4,50              |
    | 55,2,20              |
    | 38,6,12              |
    +----------------------+

    It doesn't matter which position corresponds to which field; you can
    identify invalid nearby tickets by considering only whether tickets contain
    values that are not valid for any field. Adding together all of the invalid
    values produces your ticket scanning error rate: 4 + 55 + 12 = 71.

    Consider the validity of the nearby tickets you scanned. What is your
    ticket scanning error rate?
    """
    # We ignore our ticket for now
    rules, _, nearby_tickets = parse_puzzle_input(puzzle_input)

    # Compute total error rate for all tickets
    invalid_numbers = (find_invalid_numbers(ticket, rules)
                       for ticket in nearby_tickets)
    return sum(itertools.chain(*invalid_numbers))


def solve_part2(puzzle_input):
    """Solve part 2 of today's puzzle.

    Once you work out which field is which, look for the six fields on your
    ticket that start with the word departure. What do you get if you multiply
    those six values together?
    """
    decyphered_ticket = decypher_ticket(puzzle_input)

    # Look for the six fields on your ticket that start with the word
    # departure. What do you get if you multiply those six values together?
    answer = 1
    for field_name, field_value in decyphered_ticket.items():
        if field_name.startswith('departure'):
            answer *= field_value
    return answer


def parse_puzzle_input(puzzle_input):
    """Parse the puzzle input into convenient Python data structures."""
    rules_str, your_ticket_str, nearby_tickets_str = puzzle_input.split('\n\n')

    # Regular expression matching substrings such as:
    #     class: 1-3 or 5-7
    #     row: 6-11 or 33-44
    #     seat: 13-40 or 45-50
    #     departure time: 46-147 or 153-958
    rule_matcher = re.compile(r'\s*([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)\s*')

    # Apply the regular expression to parse the rules into a dict.
    rules = dict()
    for match in rule_matcher.finditer(rules_str):
        field_name, from1, to1, from2, to2 = match.groups()
        # Ranges in the puzzle input are end-inclusive.
        # Python ranges are end-exclusive, so we need to add one.
        rules[field_name] = (range(int(from1), int(to1) + 1),
                             range(int(from2), int(to2) + 1))

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


def find_invalid_numbers(ticket, rules):
    """Find all numbers in a ticket that are not part of any valid range."""
    invalid_numbers = list()
    for num in ticket:
        # Concatenate all valid ranges into one big iterator
        range_iter = itertools.chain(*rules.values())

        # Check whether the number is in any of the ranges.
        for rule in range_iter:
            if num in rule:
                break  # Valid number
        else:
            # The number was not part of any range.
            invalid_numbers.append(num)

    return invalid_numbers


def decypher_ticket(puzzle_input):
    """Convert the puzzle input into a decyphered train ticket.

    Now that you've identified which tickets contain invalid values, discard
    those tickets entirely. Use the remaining valid tickets to determine which
    field is which.

    Using the valid ranges for each field, determine what order the fields
    appear on the tickets. The order is consistent between all tickets: if seat
    is the third field, it is the third field on every ticket, including your
    ticket.

    For example, suppose you have the following notes:

    +----------------------+
    | class: 0-1 or 4-19   |
    | row: 0-5 or 8-19     |
    | seat: 0-13 or 16-19  |
    |                      |
    | your ticket:         |
    | 11,12,13             |
    |                      |
    | nearby tickets:      |
    | 3,9,18               |
    | 15,1,5               |
    | 5,14,9               |
    +----------------------+

    Based on the nearby tickets in the above example, the first position must
    be row, the second position must be class, and the third position must be
    seat; you can conclude that in your ticket, class is 12, row is 11, and
    seat is 13.
    """
    rules, your_ticket, nearby_tickets = parse_puzzle_input(puzzle_input)

    # Discard all invalid tickets.
    def is_valid(ticket):
        return len(find_invalid_numbers(ticket, rules)) == 0
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
        potential_names = set(name for name, (range1, range2) in rules.items()
                              if all(v in range1 or v in range2
                                     for v in observed_values))
        potential_fields_names[field_num] = potential_names

    # The decyphered ticket is a dictionary: field_name -> field_value
    decyphered_ticket = dict()

    # Start decyphering each field. We can decypher a field when it only has
    # one potential field name.
    while len(potential_fields_names) > 0:
        # Find a field with only one potential name
        for field_num, potential_names in potential_fields_names.items():
            if len(potential_names) == 1:
                break

        # Now we know the name of this field, so we can decypher it.
        assigned_name = potential_names.pop()
        decyphered_ticket[assigned_name] = your_ticket[field_num]

        # We're done with this field. By removing it from the dictionary it
        # shrinks and eventually will be empty. Once the dictionary is empty,
        # we know we have decyphered all the fields.
        del potential_fields_names[field_num]

        # Remove the assigned field name from the list of potential
        # names for all other fields.
        for other_potential_names in potential_fields_names.values():
            try:
                other_potential_names.remove(assigned_name)
            except KeyError:
                # assigned_name was not part of the other_potential_names set
                # and that's ok.
                pass

    return decyphered_ticket


def test_part1():
    """Run the test cases for part1 given in the puzzle description."""

    assert solve_part1('''class: 1-3 or 5-7
                          row: 6-11 or 33-44
                          seat: 13-40 or 45-50

                          your ticket:
                          7,1,14

                          nearby tickets:
                          7,3,47
                          40,4,50
                          55,2,20
                          38,6,12''') == 71


def test_part2():
    """Run the test cases for part2 given in the puzzle description."""

    assert decypher_ticket('''class: 0-1 or 4-19
                              row: 0-5 or 8-19
                              seat: 0-13 or 16-19

                              your ticket:
                              11,12,13

                              nearby tickets:
                              3,9,18
                              15,1,5
                              5,14,9''') == {'class': 12,
                                             'row': 11,
                                             'seat': 13}


# When the script is run as `python day16.py`, solve the puzzle using the real
# puzzle input.
if __name__ == '__main__':
    with open('day16_input.txt') as f:
        puzzle_input = f.read()
    print('Part 1:', solve_part1(puzzle_input))
    print('Part 2:', solve_part2(puzzle_input))
