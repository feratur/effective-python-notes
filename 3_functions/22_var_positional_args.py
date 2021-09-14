# Item 22: Reduce Visual Noise with Variable Positional Arguments

# Accepting a variable number of positional arguments can make a function
# call clearer and reduce visual noise. (These positional arguments are
# often called varargs for short, or star args, in reference to the conventional
# name for the parameter *args.)

def log(message, values):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{message}: {values_str}')
log('My numbers are', [1, 2])
log('Hi there', [])

# Having to pass an empty list when I have no values to log is cumbersome and noisy.

# The first parameter for the log message is required, whereas any number of
# subsequent positional arguments are optional.
def log(message, *values):  # The only difference
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{message}: {values_str}')
log('My numbers are', 1, 2)
log('Hi there')  # Much better

# If I already have a sequence (like a list) and want to call a variadic function
# like log, I can do this by using the * operator. This instructs Python to pass
# items from the sequence as positional arguments to the function:
favorites = [7, 33, 99]
log('Favorite colors', *favorites)

# The first issue is that these optional positional arguments are always turned
# into a tuple before they are passed to a function. This means that if the caller
# of a function uses the * operator on a generator, it will be iterated until it’s
# exhausted
def my_generator():
    for i in range(10):
        yield i
def my_func(*args):
    print(args)
it = my_generator()
my_func(*it)
# (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

# The second issue with *args is that you can’t add new positional arguments to a
# function in the future without migrating every caller. If you try to add a
# positional argument in the front of the argument list, existing callers will
# subtly break if they aren’t updated
def log(sequence, message, *values):
    if not values:
        print(f'{sequence} - {message}')
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{sequence} - {message}: {values_str}')
log(1, 'Favorites', 7, 33)      # New with *args OK
log(1, 'Hi there')              # New message only OK
log('Favorite numbers', 7, 33)  # Old usage breaks

# To avoid this possibility entirely, you should use keyword-only arguments
# when you want to extend functions that accept *args. To be even more defensive,
# you could also consider using type annotations

# ✦ Functions can accept a variable number of positional arguments by using *args
# in the def statement.
# ✦ You can use the items from a sequence as the positional arguments for a function
# with the * operator.
# ✦ Using the * operator with a generator may cause a program to run out of memory
# and crash.
# ✦ Adding new positional parameters to functions that accept *args can introduce
# hard-to-detect bugs.
