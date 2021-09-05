# Item 12: Avoid Striding and Slicing in a Single Expression

# Python has special syntax for the stride of a slice in the form
# somelist[start:end:stride]. This lets you take every nth item when
# slicing a sequence. For example, the stride makes it easy to group
# by even and odd indexes in a list:
x = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
odds = x[::2]
evens = x[1::2]
print(odds)
print(evens)
# ['red', 'yellow', 'blue']
# ['orange', 'green', 'purple']

# The problem is that the stride syntax often causes unexpected behavior
# that can introduce bugs. For example, a common Python trick for reversing
# a byte string is to slice the string with a stride of -1:
x = b'mongoose'
y = x[::-1]
print(y)
# b'esoognom'

x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
x[::2]   # ['a', 'c', 'e', 'g']
x[::-2]  # ['h', 'f', 'd', 'b']
x[2::2]     # ['c', 'e', 'g']
x[-2::-2]   # ['g', 'e', 'c', 'a']
x[-2:2:-2]  # ['g', 'e']
x[2:2:-2]   # []

# ✦ Specifying start, end, and stride in a slice can be extremely confusing.
# ✦ Prefer using positive stride values in slices without start or end indexes.
# Avoid negative stride values if possible.
# ✦ Avoid using start, end, and stride together in a single slice.
# If you need all three parameters, consider doing two assignments
# (one to stride and another to slice) or using islice from the itertools
# built-in module.
