# Item 8: Use zip to Process Iterators in Parallel

# List comprehensions make it easy to take a source list
# and get a derived list by applying an expression
names = ['Cecilia', 'Lise', 'Marie']
counts = [len(n) for n in names]
print(counts)
# [7, 4, 5]

longest_name = None
max_count = 0

# zip wraps two or more iterators with a lazy generator.
# The zip gener- ator yields tuples containing the next value
# from each iterator. These tuples can be unpacked directly within a for statement
for name, count in zip(names, counts):
    if count > max_count:
        longest_name = name
        max_count = count

# zip consumes the iterators it wraps one item at a time,
# which means it can be used with infinitely long inputs
# without risk of a program using too much memory and crashing

# beware of zip’s behavior when the input iterators are of different lengths
# zip keeps yielding tuples until any one of the wrapped iterators is exhausted.
# Its output is as long as its shortest input

# If you don’t expect the lengths of the lists passed to zip to be equal,
# consider using the zip_longest function from the itertools built-in module instead
import itertools
names.append('Rosalind')
for name, count in itertools.zip_longest(names, counts):
    print(f'{name}: {count}')
# Cecilia: 7
# Lise: 4
# Marie: 5
# Rosalind: None

# zip_longest replaces missing values — the length of the string
# 'Rosalind' in this case—with whatever fillvalue is passed to it,
# which defaults to None

# ✦ The zip built-in function can be used to iterate over
# multiple iterators in parallel.
# ✦ zip creates a lazy generator that produces tuples, so it
# can be used on infinitely long inputs.
# ✦ zip truncates its output silently to the shortest iterator
# if you supply it with iterators of different lengths.
# ✦ Use the zip_longest function from the itertools built-in module
# if you want to use zip on iterators of unequal lengths without truncation.
