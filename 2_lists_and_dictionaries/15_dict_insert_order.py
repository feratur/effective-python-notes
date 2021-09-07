# Item 15: Be Cautious When Relying on dict Insertion Ordering

# Starting with Python 3.6, and officially part of the Python specification
# in version 3.7, dictionaries will preserve insertion order.
baby_names = {
    'cat': 'kitten',
    'dog': 'puppy',
}
print(baby_names)
print(list(baby_names.keys()))
print(list(baby_names.values()))
print(list(baby_names.items()))
print(baby_names.popitem())  # Last item inserted
# ['cat', 'dog']
# ['kitten', 'puppy']
# [('cat', 'kitten'), ('dog', 'puppy')]
# ('dog', 'puppy')

# Keyword arguments to functions—including the **kwargs catch-all parameter;
# previously would come through in seemingly random order, which can make it
# harder to debug function calls. Now, the order of keyword arguments is always
# preserved to match how the programmer originally called the function:
def my_func(**kwargs):
    for key, value in kwargs.items():
        print(f'{key} = {value}')
my_func(goose='gosling', kangaroo='joey')
# goose = gosling
# kangaroo = joey

# Classes also use the dict type for their instance dictionaries.
class MyClass:
    def __init__(self):
        self.alligator = 'hatchling'
        self.elephant = 'calf'
a = MyClass()
for key, value in a.__dict__.items():
    print(f'{key} = {value}')
# alligator = hatchling
# elephant = calf

# For a long time the collections built-in module has had an OrderedDict class
# that preserves insertion ordering. Although this class’s behavior is similar
# to that of the standard dict type (since Python 3.7), the performance
# characteristics of OrderedDict are quite different. If you need to handle a
# high rate of key insertions and popitem calls (e.g., to implement a
# least-recently-used cache), OrderedDict may be a better fit than the standard
# Python dict type.

# However, you shouldn’t always assume that insertion ordering behavior
# will be present when you’re handling dictionaries (because custom class
# may not conform to this contract):
from collections.abc import MutableMapping
class SortedDict(MutableMapping):
    def __init__(self):
        self.data = {}
    def __getitem__(self, key):
        return self.data[key]
    def __setitem__(self, key, value):
        self.data[key] = value
    def __delitem__(self, key):
        del self.data[key]
    def __iter__(self):
        keys = list(self.data.keys())
        keys.sort()
        for key in keys:
            yield key
    def __len__(self):
        return len(self.data)

# The problem of non-matching contracts/expectations can be mitigated:
# - no longer assume that dict-like object has a specific iteration order
# - add an explicit check to ensure that the type of object matches expectations
# - use type annotations to enforce specific types

# ✦ Since Python 3.7, you can rely on the fact that iterating a dict instance’s
# contents will occur in the same order in which the keys were initially added.
# ✦ Python makes it easy to define objects that act like dictionaries but that
# aren’t dict instances. For these types, you can’t assume that insertion ordering
# will be preserved.
# ✦ There are three ways to be careful about dictionary-like classes: Write code
# that doesn’t rely on insertion ordering, explicitly check for the dict type at
# runtime, or require dict values using type annotations and static analysis (mypy).
