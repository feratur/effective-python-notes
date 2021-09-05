# Item 11: Know How to Slice Sequences

# Slicing can be extended to any Python class that implements
# the __getitem__ and __setitem__ special methods

# The basic form of the slicing syntax is somelist[start:end],
# where start is inclusive and end is exclusive:
a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
print('Middle two:  ', a[3:5])
print('All but ends:', a[1:7])
# When slicing from the start of a list, you should leave out the
# zero index to reduce visual noise:
assert a[:5] == a[0:5]
# When slicing to the end of a list, you should leave out the final index
# because it’s redundant:
assert a[5:] == a[5:len(a)]
# Using negative numbers for slicing is helpful for doing offsets relative
# to the end of a list. All of these forms of slicing would be clear to a
# new reader of your code
assert a[-3:-1] == ['f', 'g']

# Slicing deals properly with start and end indexes that are beyond the
# boundaries of a list by silently omitting missing items. This behavior
# makes it easy for your code to establish a maximum length to consider
# for an input sequence

# However, somelist[-0:] is equivalent to somelist[:] - copies the list

# The result of slicing a list is a whole new list. References to the
# objects from the original list are maintained. Modifying the result
# of slicing won’t affect the original list
b = a[3:]
print('Before:   ', b)
b[1] = 99
print('After:    ', b)
print('No change:', a)
# Before:    ['d', 'e', 'f', 'g', 'h']
# After:     ['d', 99, 'f', 'g', 'h']
# No change: ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

# When used in assignments, slices replace the specified range in the original list.
# Unlike unpacking assignments (such as a, b = c[:2]), the lengths of slice
# assignments don’t need to be the same. The values before and after the assigned
# slice will be preserved. Here, the list shrinks because the replacement list is
# shorter than the specified slice:
print('Before ', a)
a[2:7] = [99, 22, 14]
print('After  ', a)
# Before  ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
# After   ['a', 'b', 99, 22, 14, 'h']

# And here the list grows because the assigned list is longer than the specific slice:
print('Before ', a)
a[2:3] = [47, 11]
print('After  ', a)
# Before  ['a', 'b', 99, 22, 14, 'h']
# After   ['a', 'b', 47, 11, 22, 14, 'h']

# If you leave out both the start and the end indexes when slicing,
# you end up with a copy of the original list:
b = a[:]
assert b == a and b is not a

# If you assign to a slice with no start or end indexes, you replace
# the entire contents of the list with a copy of what’s referenced
# (instead of allocating a new list):
b=a
print('Before a', a)
print('Before b', b)
a[:] = [101, 102, 103]
assert a is b         # Still the same list object
print('After a ', a)  # Now has different contents
print('After b ', b)  # Same list, so same contents as a
# Before a ['a', 'b', 47, 11, 22, 14, 'h']
# Before b ['a', 'b', 47, 11, 22, 14, 'h']
# After a  [101, 102, 103]
# After b  [101, 102, 103]

# ✦ Avoid being verbose when slicing: Don’t supply 0 for the start index
# or the length of the sequence for the end index.
# ✦ Slicing is forgiving of start or end indexes that are out of bounds,
# which means it’s easy to express slices on the front or back boundaries
# of a sequence (like a[:20] or a[-20:]).
# ✦ Assigning to a list slice replaces that range in the original sequence
# with what’s referenced even if the lengths are different.
