# Item 27: Use Comprehensions Instead of map and filter

# list comprehensions
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = []
for x in a:
    squares.append(x**2)

assert squares == [x**2 for x in a]  # List comprehension

# Unless you’re applying a single-argument function, list comprehensions are also clearer than the map
# built-in function for simple cases. map requires the creation of a lambda function for the computation,
# which is visually noisy:
alt = map(lambda x: x ** 2, a)

# list comprehensions let you easily filter items from the input list, removing corresponding outputs from
# the result
even_squares = [x**2 for x in a if x % 2 == 0]

alt = map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))
assert even_squares == list(alt)

# Dictionaries and sets have their own equivalents of list comprehensions
even_squares_dict = {x: x**2 for x in a if x % 2 == 0}
threes_cubed_set = {x**3 for x in a if x % 3 == 0}

alt_dict = dict(map(lambda x: (x, x**2),
                filter(lambda x: x % 2 == 0, a)))
alt_set = set(map(lambda x: x**3,
              filter(lambda x: x % 3 == 0, a)))

# ✦ List comprehensions are clearer than the map and filter built-in functions because they don’t
# require lambda expressions.
# ✦ List comprehensions allow you to easily skip items from the input list, a behavior that map
# doesn’t support without help from filter.
# ✦ Dictionaries and sets may also be created using comprehensions.
