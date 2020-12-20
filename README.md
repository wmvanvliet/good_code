# Thoughts on writing good code

When you start out as a programmer, your main concern is to come up with a working programming code that does what you want it to do.
Once you become good enough at this that multiple ways to write this code occur to you, a new problem arises: which way is best?
Other than the prime requirement of creating the program you desire, what secondary, "nice to have", requirements does good programming code have?

In this document, I will explore the following requirements and see where they lead us:

 1. The programming code must produce a program with the desired functionality
 2. It must be obvious to a human reading the code, that the code produces the desired program
 3. The resulting program must be efficient
 
To be able to discuss requirement #1, we need some example desired functionality.
The [Advent of code](https://adventofcode.com) puzzle challenge will provide this for us.
The desired functionality for our program will be to produce the answer to one of the puzzles in this challenge.

We will see that fullfilling the second requirement depends a great deal on the context in which the program is being read by a human.
The context I chose is that of a laboratory that produces groundbreaking results from measurements obtained through experiments.
The reason for this choice is that this is the context in which I usually write code and hence have thought enough about that I may have something worthwhile to say.

I'll be discussing the code I wrote to solve two puzzles and describe some of my design decisions and the reasoning behind those decisions in light of the three requirements listed above.

# Advent of code 2020, day 1

The Elves in accounting need is to fix a expense report (our puzzle input); apparently, something isn't quite adding up.
Specifically, given a list of numbers (the expense report), they need us to find the two entries that sum to 2020.
The solution to the puzzle is those two numbers multiplied together.
I invite you to [read the puzzle description for yourself](https://adventofcode.com/2020/day/1).

First is the choice of programming language.
The program we are aiming for will only need to be run once and produce a single output without any user interaction.
This is a perfect use case for a scripting language.
In science, [Python](https://python.org) is currently used a lot for short data analysis scripts, and such a script seems appropriate in this case.

The puzzle description contains a simplified example, which would serve well as unit test.
So for this program, I chose to employ test driven design: first write some unit tests, then write the functionality to pass the test.
This style is very well suited when faced with puzzle-like problems (less so in other scenarios) and since we get a unit test handed to us, it makes a lot of sense to use it.

Along with some comments explaining the puzzle and example (copied from the puzzle description), my initial program looked like this:

```python
"""
Advent of code 2020, day 1
--------------------------

The Elves in accounting just need you to fix your expense report (your puzzle
input); apparently, something isn't quite adding up.
"""


def solve_part1(puzzle_input):
    """Solve part 1 of today's puzzle.

    Find the two entries that sum to 2020; what do you get if you multiply them
    together?
    """
    pass  # TODO: write actual function body


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
```

Following Python conventions, the description of what the script does goes in a docstring at the top of the file.
Each function has its own docstring explaining its purpose.
The unit test can be run through the terminal command: `py.test day01.py` and currently fails because there is no code yet to actually solve the puzzle.

To satisfy requirement #2, that it must be obvious to a human reading the code to decipher what it does, names are **extremely** important.
On a theoretical level, all is numbers.
It is in the names we assign to these numbers that meaning can be derived from them.
In many context, my chosen names `solve_part1` and `test_part1` would be quite uninformative.
Part 1 of what?
Now we see how important the context of a program is to requirement #2.
In the context of Advent of Code puzzles, it is more obvious to call the function `solve_part1` than it would be to name it something like `balance_expenses`.
All Advent of Code puzzles come in two parts and they are named "part 1" and "part 2" in the puzzle description.
The function name should describe what problem the function is doing and the problem has been given a name in the puzzle description, so it would be a mistake to call it anything else in our code.
Furthermore, as a general rule, function names should start with a verb, since functions are like the verbs in a programming language.
Hence, instead of just `part1`, I opted to start with a verb and make it `solve_part1`.
The testing framework requires all our unit tests to start with the verb `test_`, so `test_part1` it is.

On to the implementation of the `solve_part1` function.
First, we must parse the input, which comes to us as a string, to a list of numbers.
We should always use the names given in the context of the problem.
In the puzzle description, the string is called the "puzzle input", each number an "entry" and the list of numbers an "expense report".
My attempt to translate the above into Python in the most obvious way possible is this:
```python
expense_report = [int(entry) for entry in puzzle_input.lines()]
```

One way to find the two entries that sum to 2020 is to keep trying combinations until we find the correct one:

```python
from itertools import combinations
for entry1, entry in combinations(expense_report, 2):
    if entry1 + entry2 == 2020:
        return entry1 * entry2
```

However, that has a time complexity of O(n²).
Requirement #3 asks us to think if we can find a better way.
One thing that comes to mind is that when know `entry1`, we can quickly compute which `entry2` we are looking for, namely `2020 - entry1`.
Furthermore, the order of the entries in the expense report is irrelevant to the puzzle, so we may opt to store it in a set to have very quick lookups.
The following implementation has a time complexity of O(n):

```python
expense_report = set(int(entry) for entry in puzzle_input.lines())
for entry1 combinations(expense_report):
    entry2 = 2020 - entry1
    if entry2 in expense_report:
        return entry1 * entry2
```

