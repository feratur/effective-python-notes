# Item 23: Provide Optional Behavior with Keyword Arguments

def remainder(number, divisor):
    return number % divisor
assert remainder(20, 7) == 6

# All normal arguments to Python functions can also be passed by keyword,
# where the name of the argument is used in an assignment within the parentheses
# of a function call. The keyword arguments can be passed in any order as long as
# all of the required positional arguments are specified. You can mix and match
# keyword and posi- tional arguments. These calls are equivalent:
remainder(20, 7)
remainder(20, divisor=7)
remainder(number=20, divisor=7)
remainder(divisor=7, number=20)

# Positional arguments must be specified before keyword arguments:
# remainder(number=20, 7) - Error!

# Each argument can be specified only once:
# remainder(20, number=7) - Error!

# If you already have a dictionary, and you want to use its contents to call a
# function like remainder, you can do this by using the ** operator.
my_kwargs = {
    'number': 20,
    'divisor': 7,
}
assert remainder(**my_kwargs) == 6

# You can mix the ** operator with positional arguments or keyword
# arguments in the function call, as long as no argument is repeated:
my_kwargs = {
    'divisor': 7,
}
assert remainder(number=20, **my_kwargs) == 6

# You can also use the ** operator multiple times if you know that the
# dictionaries don’t contain overlapping keys:
my_kwargs = {
    'number': 20,
}
other_kwargs = {
    'divisor': 7,
}
assert remainder(**my_kwargs, **other_kwargs) == 6

# And if you’d like for a function to receive any named keyword argument,
# you can use the **kwargs catch-all parameter to collect those arguments
# into a dict that you can then process
def print_parameters(**kwargs):
    for key, value in kwargs.items():
        print(f'{key} = {value}')
print_parameters(alpha=1.5, beta=9, gamma=4)

# The first benefit is that keyword arguments make the function call clearer
# to new readers of the code.
remainder(divisor=7, number=20)

# The second benefit of keyword arguments is that they can have default values
# specified in the function definition.
def flow_rate(weight_diff, time_diff, period=1):
    return (weight_diff / time_diff) * period

weight_diff = 0.5
time_diff = 3
flow_per_second = flow_rate(weight_diff, time_diff)
flow_per_hour = flow_rate(weight_diff, time_diff, period=3600)
# it gets tricky for complex default values

# The third reason to use keyword arguments is that they provide a powerful way
# to extend a function’s parameters while remaining backward compatible with
# existing callers.
def flow_rate(weight_diff, time_diff,
              period=1, units_per_kg=1):
    return ((weight_diff * units_per_kg) / time_diff) * period

# Providing backward compatibility using optional keyword arguments like this is
# also crucial for functions that accept *args

# The only problem with this approach is that optional keyword arguments like
# period and units_per_kg may still be specified as positional arguments.
# The best practice is to always specify optional arguments using the keyword
# names and never pass them as positional arguments. As a function author, you
# can also require that all callers use this more explicit keyword style to
# minimize potential errors

# ✦ Function arguments can be specified by position or by keyword.
# ✦ Keywords make it clear what the purpose of each argument is when
# it would be confusing with only positional arguments.
# ✦ Keyword arguments with default values make it easy to add new behaviors to
# a function without needing to migrate all existing callers.
# ✦ Optional keyword arguments should always be passed by keyword instead of by
# position.
