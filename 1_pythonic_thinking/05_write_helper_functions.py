# Item 5: Write Helper Functions Instead of Complex Expressions

from urllib.parse import parse_qs

my_values = parse_qs('red=5&blue=0&green=',
                     keep_blank_values=True)
print(repr(my_values))

# empty list, and zero all evaluate to False implicitly
red = my_values.get('red', [''])[0] or 0
green = my_values.get('green', [''])[0] or 0
opacity = my_values.get('opacity', [''])[0] or 0

# For parsing int
red = int(my_values.get('red', [''])[0] or 0)

# Easier to read
red_str = my_values.get('red', [''])
red = int(red_str[0]) if red_str[0] else 0

# More explicit
green_str = my_values.get('green', [''])
if green_str[0]:
    green = int(green_str[0])
else:
    green = 0

# But better to write like this
def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        return int(found[0])
    return default

green = get_first_int(my_values, 'green')

# As soon as expressions get complicated, it’s time to consider splitting
# them into smaller pieces and moving logic into helper functions. What you
# gain in readability always outweighs what brevity may have afforded you.

# ✦ Python’s syntax makes it easy to write single-line expressions that are
# overly complicated and difficult to read.
# ✦ Move complex expressions into helper functions, especially if you need
# to use the same logic repeatedly.
# ✦ An if/else expression provides a more readable alternative to using the
# Boolean operators or and and in expressions.
