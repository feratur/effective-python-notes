# Item 38: Accept Functions Instead of Classes for Simple Interfaces

names = ['Socrates', 'Archimedes', 'Plato', 'Aristotle']
names.sort(key=len)
print(names)
# ['Plato', 'Socrates', 'Aristotle', 'Archimedes']

# In Python, many hooks are just stateless functions
# with well-defined arguments and return values. Functions are ideal
# for hooks because they are easier to describe and simpler to define
# than classes. Functions work as hooks because Python has first-class
# functions: Functions and methods can be passed around and referenced
# like any other value in the language.

def log_missing():
    print('Key added')
    return 0

# defaultdict allows you to supply a function that will be called with no
# arguments each time a missing key is accessed. The function must
# return the default value that the missing key should have in the dictionary
from collections import defaultdict
current = {'green': 12, 'blue': 3}
increments = [
    ('red', 5),
    ('blue', 17),
    ('orange', 9),
]
result = defaultdict(log_missing, current)
print('Before:', dict(result))
for key, amount in increments:
    result[key] += amount
print('After: ', dict(result))
# Before: {'green': 12, 'blue': 3}
# Key added
# Key added
# After: {'green': 12, 'blue': 20, 'red': 5, 'orange': 9}

# For example, say I now want the default value hook passed to defaultdict
# to count the total number of keys that were missing. One way to
# achieve this is by using a stateful closure
def increment_with_report(current, increments):
    added_count = 0
    def missing():
        nonlocal added_count # Stateful closure
        added_count += 1
        return 0
    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount
    return result, added_count
result, count = increment_with_report(current, increments)
assert count == 2

# The problem with defining a closure for stateful hooks is that it’s
# harder to read than the stateless function example. Another approach
# is to define a small class that encapsulates the state you want to
# track:
class CountMissing:
    def __init__(self):
        self.added = 0
    def missing(self):
        self.added += 1
        return 0

counter = CountMissing()
result = defaultdict(counter.missing, current) # Method ref
for key, amount in increments:
    result[key] += amount
assert counter.added == 2

# __call__ allows an object to be called just like a function.
# It also causes the callable built-in function to return True for
# such an instance, just like a normal function or method. All objects
# that can be executed in this manner are referred to as callables:
class BetterCountMissing:
    def __init__(self):
        self.added = 0
    def __call__(self):
        self.added += 1
        return 0
counter = BetterCountMissing()
assert counter() == 0
assert callable(counter)

counter = BetterCountMissing()
result = defaultdict(counter, current) # Relies on __call__
for key, amount in increments:
    result[key] += amount
assert counter.added == 2

# The __call__ method indicates that a class’s instances will be used
# somewhere a function argument would also be suitable (like API hooks). It
# directs new readers of the code to the entry point that’s responsible
# for the class’s primary behavior. It provides a strong hint that the goal
# of the class is to act as a stateful closure.
# Best of all, defaultdict still has no view into what’s going on when
# you use __call__. All that defaultdict requires is a function for the
# default value hook. Python provides many different ways to satisfy a
# simple function interface, and you can choose the one that works best
# for what you need to accomplish

# ✦ Instead of defining and instantiating classes, you can often simply
# use functions for simple interfaces between components in Python.
# ✦ References to functions and methods in Python are first class,
# meaning they can be used in expressions (like any other type).
# ✦ The __call__ special method enables instances of a class to be
# called like plain Python functions.
# ✦ When you need a function to maintain state, consider defining a
# class that provides the __call__ method instead of defining a stateful closure.
