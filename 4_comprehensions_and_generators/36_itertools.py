# Item 36: Consider itertools for Working with Iterators and Generators

import itertools

# Linking Iterators Together

# chain
# Use chain to combine multiple iterators into a single sequential
# iterator:
it = itertools.chain([1, 2, 3], [4, 5, 6])
print(list(it))
# [1, 2, 3, 4, 5, 6]

# repeat
# Use repeat to output a single value forever, or use the second parameter
# to specify a maximum number of times:
it = itertools.repeat('hello', 3)
print(list(it))
# ['hello', 'hello', 'hello']

# cycle
# Use cycle to repeat an iterator’s items forever:
it = itertools.cycle([1, 2])
result = [next(it) for _ in range (10)]
print(result)
# [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]

# tee
# Use tee to split a single iterator into the number of parallel iterators
# specified by the second parameter. The memory usage of this function will
# grow if the iterators don’t progress at the same speed since
# buffering will be required to enqueue the pending items:
it1, it2, it3 = itertools.tee(['first', 'second'], 3)
print(list(it1))
print(list(it2))
print(list(it3))
# ['first', 'second']
# ['first', 'second']
# ['first', 'second']

# zip_longest
# This variant of the zip built-in function returns a placeholder value when an
# iterator is exhausted, which may happen if iterators have different lengths:
keys = ['one', 'two', 'three']
values = [1, 2]
normal = list(zip(keys, values))
print('zip: ', normal)
it = itertools.zip_longest(keys, values, fillvalue='nope')
longest = list(it)
print('zip_longest:', longest)
# zip: [('one', 1), ('two', 2)]
# zip_longest: [('one', 1), ('two', 2), ('three', 'nope')

# Filtering Items from an Iterator

# islice
# Use islice to slice an iterator by numerical indexes without copying.
# You can specify the end, start and end, or start, end, and step sizes,
# and the behavior is similar to that of standard sequence slicing and
# striding
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
first_five = itertools.islice(values, 5)
print('First five: ', list(first_five))
middle_odds = itertools.islice(values, 2, 8, 2)
print('Middle odds:', list(middle_odds))
# First five: [1, 2, 3, 4, 5]
# Middle odds: [3, 5, 7]

# takewhile
# takewhile returns items from an iterator until a predicate function
# returns False for an item:
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
less_than_seven = lambda x: x < 7
it = itertools.takewhile(less_than_seven, values)
print(list(it))
# [1, 2, 3, 4, 5, 6]

# dropwhile
# dropwhile, which is the opposite of takewhile, skips items from an
# iterator until the predicate function returns True for the first time:
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
less_than_seven = lambda x: x < 7
it = itertools.dropwhile(less_than_seven, values)
print(list(it))
# [7, 8, 9, 10]

# filterfalse
# filterfalse, which is the opposite of the filter built-in function,
# returns all items from an iterator where a predicate function returns False:
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = lambda x: x % 2 == 0
filter_result = filter(evens, values)
print('Filter: ', list(filter_result))
filter_false_result = itertools.filterfalse(evens, values)
print('Filter false:', list(filter_false_result))
# Filter: [2, 4, 6, 8, 10]
# Filter false: [1, 3, 5, 7, 9]

# Producing Combinations of Items from Iterators

# accumulate
# accumulate folds an item from the iterator into a running value by
# applying a function that takes two parameters. It outputs the current
# accumulated result for each input value:
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
sum_reduce = itertools.accumulate(values)
print('Sum: ', list(sum_reduce))
def sum_modulo_20(first, second):
    output = first + second
    return output % 20
modulo_reduce = itertools.accumulate(values, sum_modulo_20)
print('Modulo:', list(modulo_reduce))
# Sum: [1, 3, 6, 10, 15, 21, 28, 36, 45, 55]
# Modulo: [1, 3, 6, 10, 15, 1, 8, 16, 5, 15]
# This is essentially the same as the reduce function from the functools
# built-in module, but with outputs yielded one step at a time. By default
# it sums the inputs if no binary function is specified.

# product
# product returns the Cartesian product of items from one or more iterators,
# which is a nice alternative to using deeply nested list comprehensions:
single = itertools.product([1, 2], repeat=2)
print('Single: ', list(single))
multiple = itertools.product([1, 2], ['a', 'b'])
print('Multiple:', list(multiple))
# Single: [(1, 1), (1, 2), (2, 1), (2, 2)]
# Multiple: [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]

# permutations
# permutations returns the unique ordered permutations of length N
# with items from an iterator:
it = itertools.permutations([1, 2, 3, 4], 2)
print(list(it))
# [(1, 2),
#  (1, 3),
#  (1, 4),
#  (2, 1),
#  (2, 3),
#  (2, 4),
#  (3, 1),
#  (3, 2),
#  (3, 4),
#  (4, 1),
#  (4, 2),
#  (4, 3)]

# combinations
# combinations returns the unordered combinations of length N with
# unrepeated items from an iterator:
it = itertools.combinations([1, 2, 3, 4], 2)
print(list(it))
# [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]

# combinations_with_replacement
# combinations_with_replacement is the same as combinations, but
# repeated values are allowed:
it = itertools.combinations_with_replacement([1, 2, 3, 4], 2)
print(list(it))
# [(1, 1),
#  (1, 2),
#  (1, 3),
#  (1, 4),
#  (2, 2),
#  (2, 3),
#  (2, 4),
#  (3, 3),
#  (3, 4),
#  (4, 4)]

# ✦ The itertools functions fall into three main categories for working with
# iterators and generators: linking iterators together, filtering
# items they output, and producing combinations of items.
# ✦ There are more advanced functions, additional parameters, and
# useful recipes available in the documentation at help(itertools).
