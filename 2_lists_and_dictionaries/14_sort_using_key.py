# Item 14: Sort by Complex Criteria Using the key Parameter

# The list built-in type provides a sort method for ordering
# the items in a list instance based on a variety of criteria.
# By default, sort will order a list’s contents by the natural
# ascending order of the items.
numbers = [93, 86, 11, 68, 70]
numbers.sort()
print(numbers)
# [11, 68, 70, 86, 93]

class Tool:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
    def __repr__(self):
        return f'Tool({self.name!r}, {self.weight})'

# Sorting objects of this type doesn’t work because the sort method
# tries to call comparison special methods that aren’t defined by the class
tools = [
    Tool('level', 3.5),
    Tool('hammer', 1.25),
    Tool('screwdriver', 0.5),
    Tool('chisel', 0.25),
]
# tools.sort() -> TypeError: '<' not supported between instances of 'Tool' and 'Tool'

# you can define the necessary special methods - if your class should have a natural ordering
# but if there’s an attribute on the object that you’d like to use for sorting
# the sort method accepts a key parameter that’s expected to be a function.
# The key function is passed a single argument, which is an item from the list
# that is being sorted. The return value of the key function should be a comparable
# value (i.e., with a natural ordering) to use in place of an item for sorting purposes.
print('Unsorted:', repr(tools))
tools.sort(key=lambda x: x.name)
print('\nSorted:  ', tools)
tools.sort(key=lambda x: x.weight)
print('By weight:', tools)

places = ['home', 'work', 'New York', 'Paris']
places.sort()
print('Case sensitive:  ', places)
places.sort(key=lambda x: x.lower())
print('Case insensitive:', places)

# Sometimes you may need to use multiple criteria for sorting.
power_tools = [
    Tool('drill', 4),
    Tool('circular saw', 5),
    Tool('jackhammer', 40),
    Tool('sander', 4),
]
# Tuples are comparable by default and have a natural ordering,
# meaning that they implement all of the special methods, such as __lt__,
# that are required by the sort method. Tuples implement these special
# method comparators by iterating over each position in the tuple and
# comparing the corresponding values one index at a time.
saw = (5, 'circular saw')
jackhammer = (40, 'jackhammer')
assert not (jackhammer < saw)  # Matches expectations
drill = (4, 'drill')
sander = (4, 'sander')
assert drill[0] == sander[0]  # Same weight
assert drill[1] < sander[1]   # Alphabetically less
assert drill < sander         # Thus, drill comes first

# You can take advantage of this tuple comparison behavior in order
# to sort the list of power tools first by weight and then by name.
power_tools.sort(key=lambda x: (x.weight, x.name))
print(power_tools)

# One limitation of having the key function return a tuple is that
# the direction of sorting for all criteria must be the same
# (either all in ascending order, or all in descending order).
# For numerical values it’s possible to mix sorting directions
# by using the unary minus operator in the key function.
# This negates one of the values in the returned tuple, effectively
# reversing its sort order while leaving the others intact.
power_tools.sort(key=lambda x: (-x.weight, x.name))
print(power_tools)

# Unfortunately, unary negation isn’t possible for all types.
# For situations like this, Python provides a stable sorting algorithm.
# The sort method of the list type will preserve the order of the input
# list when the key function returns values that are equal to each other.
# This means that I can call sort multiple times on the same list to combine
# different criteria together.

power_tools.sort(key=lambda x: x.name)   # Name ascending
power_tools.sort(key=lambda x: x.weight, # Weight descending
                 reverse=True)

# This same approach can be used to combine as many different types of
# sorting criteria as you’d like in any direction, respectively. You just
# need to make sure that you execute the sorts in the opposite sequence of
# what you want the final list to contain.

# ✦ The sort method of the list type can be used to rearrange a list’s contents
# by the natural ordering of built-in types like strings, integers, tuples,
# and so on.
# ✦ The sort method doesn’t work for objects unless they define a natural ordering
# using special methods, which is uncommon.
# ✦ The key parameter of the sort method can be used to supply a helper function
# that returns the value to use for sorting in place of each item from the list.
# ✦ Returning a tuple from the key function allows you to combine multiple sorting
# criteria together. The unary minus operator can be used to reverse individual sort
# orders for types that allow it.
# ✦ For types that can’t be negated, you can combine many sorting criteria together
# by calling the sort method multiple times using different key functions and reverse
# values, in the order of lowest rank sort call to highest rank sort call.
