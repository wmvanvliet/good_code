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

The Elves in accounting need to fix a expense report (our puzzle input); apparently, something isn't quite adding up.
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
On a theoretical level, it's numbers all the way down.
It is through the names we assign to these numbers that meaning can be derived from them.
In many contexts, my chosen names `solve_part1` and `test_part1` would be quite uninformative.
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
Of course, we should not think in terms of "the string" and "the list of numbers", but always use appropriate names given the context of the problem.
In the puzzle description, the string is called the "puzzle input", each number an "entry" and the list of numbers an "expense report".
My attempt to translate the above into Python in the most obvious way possible is this:
```python
expense_report = [int(entry) for entry in puzzle_input.lines()]
```

One way to find the two entries that sum to 2020 is to keep trying combinations until we find the correct one:

```python
for entry1 in expense_report:
    for entry2 in expense_report:
        if entry1 + entry2 == 2020:
            return entry1 * entry2
```

However, that has a time complexity of O(n²).
Requirement #3 asks us to think if we can find a better way.
One optimization would be to not try both the `entry1, entry2` and `entry2, entry1` combinations, as they have the same sum.
But following that line of thought, it occured to me that we can do even better.
For a given `entry1` we can directly compute the matching `entry2` through `2020 - entry1`.
We just need to check whether the thus computed `entry2` is part of the expense report.
Since the order of the entries in the expense report is irrelevant to the puzzle, we can store it in a `set()` to have very quick lookups.
The following implementation has a time complexity of around O(n) (it depends on how many hash collisions the `set()` will experience, but it will be pretty fast):

```python
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
```

Comments were added to explain anything that may be non-obvious in the code.

In many scenarios, the names `entry1` and `entry2` would be bad variable names, because there would be a more semantic description of the role of these two entries and their relationship to one another.
However, in the abstract world of this puzzle, there isn't anything more to these entries other than that there are two of them, so in this case, anything else would be more confusing than `entry1` and `entry2`.
Again, context is everything.

What about the number `2020`?
In many cases, its better to assign this value to a variable with a descriptive name, because we are more interested in what the number represents (the speed of light, the number of gigawatts required to power a time machine) than the actual number.
But in this context, the puzzle gives no meaning to the number 2020, in which case, its probably best not to try and invent one and just use the number itself.

How about generalizing the solution to allow us to search for entries that sum for a number other than 2020?
Or to search for more than two entries?
You might have heart of "premature optimization is the root of all evil" and in my opinion, something similar applies to premature generalization.
Especially in the context of data analysis, there are plenty of cases where we are only interested in one specific computation, performed on one specific dataset, and generalizing it would only make the code more complex.
The trick is to recognize when code should be generic, and when it should not be.
The same goes for checking edge cases: when code needs to be generic, you don't know what the input may be in the future, so you must take care of any and all edge cases.
On the other hand, if you do know the input and know it's not going to change, there is a case to be made for avoiding code that deals with edge cases if it would add too much complexity.
In the case of this Advent of Code puzzle, there is no need to be generic, nor deal with edge cases, so we won't.
All we care about is the shortest, most obvious code possible.

Part two of the puzzle asks us to find **three** entries that sum to 2020.
One way to solve this is to make our solution to part 1 generic and re-use it in part 2.
But in practise, this adds quite some complexity (try it yourself and discover the amount of stuff you suddenly have to deal with).
For example, we have to move the parsing of the puzzle input outside the `solve_part1` function.
And we must deal with the case where these is no solution to part1.
And we must return the actual entries from the `solve_part1` function.
Not worth it.

Instead, let's focus first on a solution to part 2 in isolation.
First the most straightforward solution:

```python
expense_report = [int(entry) for entry in puzzle_input.lines()]
for entry1 in expense_report:
    for entry2 in expense_report:
        for entry3 in expense_report:
            if entry1 + entry2 + entry3 == 2020:
                return entry1 * entry2 * entry3
```

Triple nested loops, that's getting difficult to read by a human.
Can we do better?
Yes, if we use the `itertools` module that is part of the standard library.
As a bonus, we now no longer test multiple permutations of the same three entries:

```python
from itertools import combinations

expense_report = [int(entry) for entry in puzzle_input.lines()]
for entry1, entry2, entry3 in combinations(expense_report, 2):
    if entry1 + entry2 + entry3 == 2020:
        return entry1 * entry2 * entry3
```

That's pretty nice to read.
However, the time complexity is O(n³), how about trying to satisfy requirement #3 without adding too much complexity?
We could implement our `2020 - x` and `set()` lookup trick, which looks like this:

```python
from itertools import combinations

expense_report = set(int(entry) for entry in puzzle_input.lines())
for entry1, entry2 in combinations(expense_report, 2):
    entry3 = 2020 - (entry1 + entry2)
    if entry3 in expense_report:
        return entry1 * entry2 * entry3
```

Now we're at around O(n²) (again, it depends on the amount of hash collisions in the `set()`), but it has come at the cost of readability.
We generate combinations of two entries while the puzzle asks us to consider combinations of three.
The code is no longer immediately obvious.

For our final version, let's consider another optimization strategy.
If three numbers need to sum to 2020, they must be relatively small.
What happens if we try the small entries first?

```python
from itertools import combinations

# For three entries to sum to 2020, they must be relatively small. We will
# find the solution much faster if we try the entries in ascending order.
expense_report = sorted(int(entry) for entry in puzzle_input.lines())

for entry1, entry2, entry3 in combinations(expense_report, 3):
    if entry1 + entry2 + entry3 == 2020:
        return entry1 * entry2 * entry3
```

This finds the solution after only 227 iterations, even though the worst case complexity is still O(n³).
But we don't care about worst case complexity, we have a specific puzzle input and it must be fast for that specific case, which it is.

Finally, we need to run the algorithms on the real puzzle input:

```python
# When the script is run as `python day01.py`, solve the puzzle using the real
# puzzle input.
if __name__ == '__main__':
    with open('day1_input.txt') as f:
        puzzle_input = f.read()
        print('Part 1:', solve_part1(puzzle_input))
        print('Part 2:', solve_part2(puzzle_input))
```

You can find the code in its final form here: [`day01.py`](day01.py).
