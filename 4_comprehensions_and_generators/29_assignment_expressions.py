# Item 29: Avoid Repeated Work in Comprehensions by Using Assignment Expressions

stock = {
    'nails': 125,
    'screws': 35,
    'wingnuts': 8,
    'washers': 24,
}
order = ['screws', 'wingnuts', 'clips']

def get_batches(count, size):
    return count // size

result = {}
for name in order:
  count = stock.get(name, 0)
  batches = get_batches(count, 8)
  if batches:
    result[name] = batches

print(result)
# {'screws': 4, 'wingnuts': 1}

found = {name: get_batches(stock.get(name, 0), 8)
         for name in order
         if get_batches(stock.get(name, 0), 8)}

assert found == result
# Although this code is more compact, the problem with it is that the get_batches(stock.get(name, 0), 8)
# expression is repeated.

# An easy solution to these problems is to use the walrus operator (:=), which was introduced in Python 3.8
found = {name: batches for name in order
         if (batches := get_batches(stock.get(name, 0), 8))}

# t’s valid syntax to define an assignment expression in the value expression for a comprehension.
# But if you try to reference the vari- able it defines in other parts of the comprehension, you
# might get an exception at runtime because of the order in which comprehensions are evaluated
#
# result = {name: (tenth := count // 10)
#           for name, count in stock.items() if tenth > 0}
# Traceback ...
# NameError: name 'tenth' is not defined

result = {name: tenth for name, count in stock.items()
          if (tenth := count // 10) > 0}
print(result)
# {'nails': 12, 'screws': 3, 'washers': 2}

# If a comprehension uses the walrus operator in the value part of the comprehension and doesn’t have
# a condition, it’ll leak the loop variable into the containing scope
half = [(last := count // 2) for count in stock.values()]
print(f'Last item of {half} is {last}')
# Last item of [62, 17, 4, 12] is 12

for count in stock.values():  # Leaks loop variable
    pass
print(f'Last item of {list(stock.values())} is {count}')
# Last item of [125, 35, 8, 24] is 24

# However, similar leakage doesn’t happen for the loop variables from comprehensions:
half = [count // 2 for count in stock.values()]
print(half)   # Works
# print(count)  # Exception because loop variable didn't leak

# It’s better not to leak loop variables, so I recommend using assignment expressions
# only in the condition part of a comprehension.

# Using an assignment expression also works the same way in generator expressions
found = ((name, batches) for name in order
         if (batches := get_batches(stock.get(name, 0), 8)))
print(next(found))
print(next(found))
# ('screws', 4)
# ('wingnuts', 1)

# ✦ Assignment expressions make it possible for comprehensions and generator expressions to
# reuse the value from one condition elsewhere in the same comprehension, which can improve
# readability and performance.
# ✦ Although it’s possible to use an assignment expression outside of a comprehension or
# generator expression’s condition, you should avoid doing so.
