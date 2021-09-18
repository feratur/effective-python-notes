# Item 31: Be Defensive When Iterating Over Arguments

def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

visits = [15, 35, 80]
percentages = normalize(visits)
print(percentages)
assert sum(percentages) == 100.0
# [11.538461538461538, 26.923076923076923, 61.53846153846154]

def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)

# it = read_visits('my_numbers.txt')
# percentages = normalize(it)
# print(percentages)
# []

# This behavior occurs because an iterator produces its results only a single time.
# If you iterate over an iterator or a generator that has already raised a StopIteration
# exception, you won’t get any results the second time around
#
# it = read_visits('my_numbers.txt')
# print(list(it))
# print(list(it))  # Already exhausted
# [15, 35, 80]
# []

# Confusingly, you also won’t get errors when you iterate over an already exhausted iterator.
# for loops, the list constructor, and many other functions throughout the Python standard
# library expect the StopIteration exception to be raised during normal operation. These functions
# can’t tell the difference between an iterator that has no output and an iterator that had output
# and is now exhausted.
def normalize_copy(numbers):
    numbers_copy = list(numbers)  # Copy the iterator
    total = sum(numbers_copy)
    result = []
    for value in numbers_copy:
        percent = 100 * value / total
        result.append(percent)
    return result

# Now works correctly
#
# it = read_visits('my_numbers.txt')
# percentages = normalize_copy(it)
# print(percentages)
# assert sum(percentages) == 100.0
# [11.538461538461538, 26.923076923076923, 61.53846153846154]

# The problem with this approach is that the copy of the input iterator’s contents could be extremely large.
# One way around this is to accept a function that returns a new iterator each time it’s called
def normalize_func(get_iter):
    total = sum(get_iter())   # New iterator
    result = []
    for value in get_iter():  # New iterator
        percent = 100 * value / total
        result.append(percent)
    return result

# path = 'my_numbers.txt'
# percentages = normalize_func(lambda: read_visits(path))
# print(percentages)
# assert sum(percentages) == 100.0
# [11.538461538461538, 26.923076923076923, 61.53846153846154]

# Although this works, having to pass a lambda function like this is clumsy. A better way to achieve
# the same result is to provide a new container class that implements the iterator protocol.

# When Python sees a statement like for x in foo, it actually calls iter(foo). The iter built-in
# function calls the foo.__iter__ special method in turn. The __iter__ method must return an iterator
# object (which itself implements the __next__ special method). Then, the for loop repeatedly calls
# the next built-in function on the iterator object until it’s exhausted (indicated by raising a
# StopIteration exception).

# It sounds complicated, but practically speaking, you can achieve all of this behavior for your
# classes by implementing the __iter__ method as a generator.
class ReadVisits:
    def __init__(self, data_path):
        self.data_path = data_path
    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)

# visits = ReadVisits(path)
# percentages = normalize(visits)
# print(percentages)
# assert sum(percentages) == 100.0
# [11.538461538461538, 26.923076923076923, 61.53846153846154]

# The protocol states that when an iterator is passed to the iter built-in function, iter returns
# the iterator itself. In contrast, when a container type is passed to iter, a new iterator object
# is returned each time. Thus, you can test an input value for this behavior and raise a TypeError
# to reject arguments that can’t be repeatedly iterated over
def normalize_defensive(numbers):
    if iter(numbers) is numbers:  # An iterator -- bad!
        raise TypeError('Must supply a container')
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

# Alternatively, the collections.abc built-in module defines an Iterator class that can be used in
# an isinstance test to recognize the potential problem
from collections.abc import Iterator
def normalize_defensive(numbers):
    if isinstance(numbers, Iterator):  # Another way to check
        raise TypeError('Must supply a container')
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

# The approach of using a container is ideal if you don’t want to copy the full input iterator,
# as with the normalize_copy function above, but you also need to iterate over the input data
# multiple times. This function works as expected for list and ReadVisits inputs because they
# are iterable containers that follow the iterator protocol:
visits = [15, 35, 80]
percentages = normalize_defensive(visits)
assert sum(percentages) == 100.0
# visits = ReadVisits(path)
# percentages = normalize_defensive(visits)
# assert sum(percentages) == 100.0

# The function raises an exception if the input is an iterator rather than a container:
#
# visits = [15, 35, 80]
# it = iter(visits)
# normalize_defensive(it)
# Traceback ...
# TypeError: Must supply a container

# The same approach can also be used for asynchronous iterators

# ✦ Beware of functions and methods that iterate over input arguments multiple times. If these
# arguments are iterators, you may see strange behavior and missing values.
# ✦ Python’s iterator protocol defines how containers and iterators interact with the iter and
# next built-in functions, for loops, and related expressions.
# ✦ You can easily define your own iterable container type by implementing the __iter__ method
# as a generator.
# ✦ You can detect that a value is an iterator (instead of a container) if calling iter on it
# produces the same value as what you passed in. Alternatively, you can use the isinstance
# built-in function along with the collections.abc.Iterator class.
