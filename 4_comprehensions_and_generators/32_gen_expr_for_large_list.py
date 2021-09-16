# Item 32: Consider Generator Expressions for Large List Comprehensions

# Python provides generator expressions, which are a generalization of list comprehensions and generators.
# Generator expressions don’t materialize the whole output sequence when they’re
# run. Instead, generator expressions evaluate to an iterator that yields
# one item at a time from the expression.
it = (x for x in [1, 2, 3])
print(it)
# <generator object <genexpr> at 0x108993dd0>
print(next(it))
print(next(it))
# 1
# 2

# Another powerful outcome of generator expressions is that they can be composed together.
roots = ((x, x**0.5) for x in it)
# Each time I advance this iterator, it also advances the interior iterator, creating a domino
# effect of looping, evaluating conditional expressions, and passing around inputs and outputs,
# all while being as memory efficient as possible.
# The only gotcha is that the iterators returned by generator expressions are stateful, so you
# must be careful not to use these iterators more than once

# ✦ List comprehensions can cause problems for large inputs by using
# too much memory.
# ✦ Generator expressions avoid memory issues by producing outputs
# one at a time as iterators.
# ✦ Generator expressions can be composed by passing the iterator from
# one generator expression into the for subexpression of another.
# ✦ Generator expressions execute very quickly when chained together
# and are memory efficient.
